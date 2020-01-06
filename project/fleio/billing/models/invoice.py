import logging
import decimal
import pycountry

from django.db import models, transaction
from django.db.models.functions import Coalesce
from django.template import Context, Template
from django.template.exceptions import TemplateSyntaxError
from django.utils.timezone import now as utcnow
from django.utils.translation import ugettext_lazy as _

from fleio.billing.settings import BillingItemTypes
from fleio.core.models import Client, Currency, get_default_currency
from fleio.core.utils import RandomId

from .journal_sources import JournalSources

LOG = logging.getLogger(__name__)


class InvoiceStatus(object):
    ST_CANCELLED = 'cancelled'
    ST_PAID = 'paid'
    ST_REFUNDED = 'refunded'
    ST_UNPAID = 'unpaid'

    PAYMENT_STATUSES = (
        (ST_UNPAID, _('Unpaid')),
        (ST_PAID, _('Paid')),
        (ST_CANCELLED, _('Cancelled')),
        (ST_REFUNDED, _('Refunded')),
    )

    STATUSES_LIST = [st[0] for st in PAYMENT_STATUSES]


class InvoiceQueryset(models.QuerySet):
    def for_service(self, service):
        return self.filter(items__service=service)

    def unpaid(self):
        return self.filter(status=InvoiceStatus.ST_UNPAID)

    def paid(self):
        return self.filter(status=InvoiceStatus.ST_PAID)

    def canceled(self):
        return self.filter(status=InvoiceStatus.ST_CANCELLED)

    def refunded(self):
        return self.filter(status=InvoiceStatus.ST_REFUNDED)

    def for_credit(self):
        return self.filter(items__item_type=BillingItemTypes.credit)


class Invoice(models.Model):
    """All prices include taxes."""
    INVOICE_STATUS = InvoiceStatus
    # Hardcoded maximum of 14 digits, out of which two are decimals
    MAX_TOTAL = decimal.Decimal('999999999999.99')
    # Random ID is shown to users (in URL, API responses etc.) in order to hide the primary key auto number
    id = models.BigIntegerField(unique=True, default=RandomId('billing.Invoice'), primary_key=True)
    number = models.CharField(max_length=32, db_index=True, null=True, blank=True)
    is_fiscal = models.BooleanField(default=False)
    fiscal_date = models.DateTimeField(null=True, blank=True)
    fiscal_due_date = models.DateTimeField(null=True, blank=True)
    issue_date = models.DateTimeField(db_index=True, default=utcnow)
    due_date = models.DateTimeField(default=utcnow)
    processed_at = models.DateTimeField(null=True, blank=True)
    subtotal = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    currency = models.ForeignKey(Currency, default=get_default_currency, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=InvoiceStatus.PAYMENT_STATUSES,
                              default=InvoiceStatus.ST_UNPAID, db_index=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    # these fields will be used instead of the client's model fields for invoicing
    first_name = models.CharField(max_length=127)
    last_name = models.CharField(max_length=127)
    company = models.CharField(max_length=127, blank=True, null=True)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=127)
    country = models.CharField(max_length=2, db_index=True, choices=[(country.alpha_2, country.name)
                                                                     for country in pycountry.countries])
    state = models.CharField(max_length=127, blank=True, null=True)
    zip_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=64)
    fax = models.CharField(max_length=64, blank=True, null=True)
    email = models.EmailField(max_length=127)

    objects = InvoiceQueryset.as_manager()

    def __str__(self):
        return "#%s" % self.id

    def make_fiscal(self):
        if self.is_fiscal:
            # invoice is already fiscal - do nothing
            return

        billing_settings = self.client.billing_settings
        with transaction.atomic():
            invoice_number = billing_settings.select_for_update('next_paid_invoice_number')
            billing_settings.next_paid_invoice_number += 1
            billing_settings.save(update_fields=['next_paid_invoice_number'])

            date_time_now = utcnow()
            self.is_fiscal = True
            self.fiscal_date = date_time_now
            self.fiscal_due_date = date_time_now

            number_context = {
                'number': invoice_number,
                'year': date_time_now.year,
                'month': date_time_now.month,
                'day': date_time_now.day
            }

            try:
                self.number = Template(billing_settings.next_paid_invoice_number_format).render(Context(number_context))
            except TemplateSyntaxError as e:
                LOG.error('ERROR settings invoice {} number: {}'.format(self.id, e))
            return self.save(update_fields=['is_fiscal', 'fiscal_date', 'fiscal_due_date', 'number'])

    def update_totals(self):
        zero = decimal.Decimal('0.00')
        subtotal = self.items.aggregate(items_total=models.Sum(models.F('amount')))['items_total']
        subtotal = subtotal or zero
        self.subtotal = subtotal
        # FIXME(tomo): Support tax over taxed (tax applied to already taxed item).
        taxed_items = self.items.filter(taxed=True)
        taxes_total = taxed_items.aggregate(taxes_total=models.Sum(models.F('taxes__amount'))).get('taxes_total')
        taxes_total = taxes_total or decimal.Decimal('0.00')
        self.total = self.subtotal + taxes_total
        self.save(update_fields=['total', 'subtotal'])

    @property
    def journal(self):
        return self.journalentries

    @property
    def display_number(self):
        return str(self.number or self.id)

    @property
    def name(self):
        if self.is_fiscal:
            return _('Invoice {}').format(self.number)
        else:
            return _('Proforma {}').format(self.id)

    def set_status(self, new_status: str):
        self.status = new_status
        return self.save(update_fields=['status'])

    def set_paid(self):
        self.status = InvoiceStatus.ST_PAID
        result = self.save(update_fields=['status'])
        billing_settings = self.client.billing_settings
        if billing_settings.invoicing_option == 'fiscal_on_paid':
            self.make_fiscal()

        return result

    def is_paid(self):
        return self.status == InvoiceStatus.ST_PAID

    def is_unpaid(self):
        return self.status == InvoiceStatus.ST_UNPAID

    def is_credit_invoice(self):
        return self.items.filter(item_type=BillingItemTypes.credit).count() > 0

    def get_already_paid_price(self):
        invoice_in = self.journalentries.filter(destination=JournalSources.invoice)
        invoice_out = self.journalentries.filter(source=JournalSources.invoice)
        if self.is_credit_invoice():
            invoice_out = invoice_out.exclude(destination=JournalSources.credit)
            invoice_in = invoice_in.exclude(source=JournalSources.credit)
        total_in = invoice_in.aggregate(amount__sum=models.Sum('destination_amount')).get('amount__sum')
        total_out = invoice_out.aggregate(amount__sum=models.Sum('source_amount')).get('amount__sum')
        total_in = total_in or decimal.Decimal('0.0')
        total_out = total_out or decimal.Decimal('0.0')
        return total_in - total_out

    @property
    def balance(self):
        return self.total - self.get_already_paid_price()

    def get_company_info(self):
        return self.client.billing_settings.company_info

    @property
    def taxes(self):
        tax_items = self.items.filter(taxed=True).annotate(name=models.F('taxes__name')).exclude(name__isnull=True)
        items_taxes = tax_items.values('name').order_by('name')
        return items_taxes.annotate(amount=Coalesce(models.Sum('taxes__amount'), 0))

    @property
    def already_paid_credit_tax(self):
        credit_tax_journals = self.journalentries.filter(
            destination=JournalSources.invoice,
            source=JournalSources.credit_tax
        )
        total = credit_tax_journals.aggregate(amount__sum=models.Sum('destination_amount')).get('amount__sum')
        return total or decimal.Decimal('0.0')

    @property
    def taxes_total(self):
        taxed_items = self.items.filter(taxed=True)
        taxes_total = taxed_items.aggregate(taxes_total=models.Sum(models.F('taxes__amount'))).get('taxes_total')
        taxes_total = taxes_total or decimal.Decimal('0.00')
        return taxes_total

    def items_with_taxes_amount(self) -> models.QuerySet:
        """Return all items with taxes amount and total with taxes annotated"""
        return self.items.annotate(taxes_amount=Coalesce(models.Sum('taxes__amount'), 0))
