import decimal

from django.db import models, transaction
from django.utils.functional import cached_property
from django.utils.timezone import now as utcnow
from django.utils.translation import ugettext_lazy as _

from fleio.billing.models.client_credit import ClientCredit
from fleio.billing.models.invoice import Invoice
from fleio.billing.models.journal_sources import JournalSources
from fleio.billing.models.journal_sources import SOURCE_CHOICES
from fleio.billing.models.transaction import Transaction

from fleio.core.models import AppUser
from fleio.core.models import Currency
from fleio.core.models import get_default_currency


class Journal(models.Model):
    """Accounting journal"""

    date_added = models.DateTimeField(default=utcnow)
    client_credit = models.ForeignKey(ClientCredit, null=True, blank=True, related_name='journalentries',
                                      on_delete=models.CASCADE)
    invoice = models.ForeignKey(Invoice, null=True, blank=True, related_name='journalentries', on_delete=models.CASCADE)
    transaction = models.ForeignKey(Transaction, null=True, blank=True, on_delete=models.CASCADE)
    source = models.CharField(max_length=2, db_index=True, choices=SOURCE_CHOICES)
    destination = models.CharField(max_length=2, db_index=True, choices=SOURCE_CHOICES)
    source_amount = models.DecimalField(default=decimal.Decimal('0.00'), max_digits=14, decimal_places=2)
    source_currency = models.ForeignKey(Currency, default=get_default_currency,
                                        related_name='journal_source_currencies', on_delete=models.CASCADE)
    destination_amount = models.DecimalField(default=decimal.Decimal('0.00'), max_digits=14, decimal_places=2)
    destination_currency = models.ForeignKey(Currency, default=get_default_currency,
                                             related_name='journal_destination_currencies', on_delete=models.CASCADE)
    partial = models.BooleanField(default=False, help_text='Transaction has multiple journal entries ?')
    exchange_rate = models.DecimalField(max_digits=8, decimal_places=5, default=1)
    user = models.ForeignKey(AppUser, null=True, blank=True, on_delete=models.SET_NULL)
    client_credit_left = models.DecimalField(
        default=None, max_digits=14, decimal_places=2, null=True
    )  # client_credit_left saves the last credit in default currency that the client had at the moment
    client_credit_left_currency = models.ForeignKey(
        Currency, default=get_default_currency,
        null=True,
        related_name='journal_credit_left_currencies',
        on_delete=models.SET_NULL
    )
    # TODO(adrian): handle case when invoice is deleted: journal entry should be deleted indeed, but
    # a new journal entry should be added and amount put into client credit

    objects = models.Manager

    class Meta:
        verbose_name_plural = _('journal entries')
        ordering = ('-date_added', )

    def __str__(self):
        return '{}'.format(self.pk)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.client_credit_left is None:
            with transaction.atomic():
                # update client_credit_left only on create (default is None)
                if self.client_credit is None:
                    # we find client from invoice, then determine client credit
                    try:
                        client = self.invoice.client
                    except self.invoice.client.DoesNotExist:
                        pass
                    else:
                        if client:
                            try:
                                related_client_credit = ClientCredit.objects.select_for_update().get(
                                    client=client, currency=self.destination_currency
                                )
                            except ClientCredit.DoesNotExist:
                                pass
                            else:
                                self.client_credit_left = related_client_credit.amount
                                self.client_credit_left_currency = related_client_credit.currency
                else:
                    # self.client_credit exists, update client_credit_left based on it
                    self.client_credit_left = self.client_credit.amount
                    self.client_credit_left_currency = self.client_credit.currency
        return super().save(force_insert=force_insert, force_update=force_update, using=using,
                            update_fields=update_fields)

    @cached_property
    def is_refund(self):
        if self.source == JournalSources.invoice:
            if self.invoice.is_credit_invoice():
                if self.destination == JournalSources.transaction:
                    return True
                else:
                    return False
            else:
                # all entries with invoice as a source where we do not have an add credit invoice are refunds
                return True

        if self.source == JournalSources.credit and self.destination == JournalSources.transaction:
            # transfer from credit to transaction is refund
            return True

        # all other entries are not refunds
        return False
