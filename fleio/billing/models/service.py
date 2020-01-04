import datetime
import decimal
from typing import Optional

from django.db import models
from django.utils.timezone import now as utcnow
from django.utils.translation import ugettext_lazy as _
from jsonfield import JSONField

from fleio.billing import utils
from fleio.billing.settings import CyclePeriods
from fleio.billing.settings import PricingModel
from fleio.billing.settings import ServiceStatus
from fleio.billing.settings import ServiceTask
from fleio.core.models import Client
from fleio.core.utils import RandomId
from .calcelation_request import CancellationRequest
from .product import Product
from .product_cycle import ProductCycle


class ServiceQuerySet(models.QuerySet):
    def active(self):
        return self.filter(status=ServiceStatus.active)

    def suspended(self, suspend_type: str = None):
        if suspend_type is None:
            return self.filter(status=ServiceStatus.suspended)
        else:
            return self.filter(status=ServiceStatus.suspended, suspend_type=suspend_type)

    def pending(self):
        return self.filter(status=ServiceStatus.pending)

    def terminated(self):
        return self.filter(status=ServiceStatus.terminated)

    def recurring(self):
        """
        Return recurring services only.
        A service is recurring if it has the fixed and/or dynamic price and the cycle is not one time.
        """
        return self.filter(product__price_model__in=[PricingModel.fixed_and_dynamic, PricingModel.dynamic_or_fixed],
                           cycle__cycle__in=[CyclePeriods.hour, CyclePeriods.month, CyclePeriods.year])

    def non_free(self):
        return self.exclude(product__price_model=PricingModel.free)

    def in_due(self, date=None, due_days_delay=0, passed_suspend_override=False):
        """
        Return active services that are or have passed the due date and optionally
        the override date for suspension.
        The service due date is compared to date if defined or to now()
        """
        # TODO(tomo): Really take into account datetimes or just dates ?
        if date is None:
            date = utils.ceil_datetime(utcnow())
        suspend_date = date + datetime.timedelta(days=due_days_delay)
        in_due = self.filter(next_due_date__lt=suspend_date)
        if passed_suspend_override:
            return in_due.filter(models.Q(override_suspend_until__lt=suspend_date) |
                                 models.Q(override_suspend_until__isnull=True))
        else:
            return in_due

    def in_invoice_due(self, date=None):
        """
        Return services in next_invoice_due compared to date if defined or now()
        """
        if date is None:
            date = utils.ceil_datetime(utcnow())
        return self.filter(models.Q(next_invoice_date__lte=date) | models.Q(next_invoice_date__isnull=True))

    def product_type(self, product_type):
        return self.filter(product__product_type=product_type)

    def with_internal_id(self):
        return self.exclude(internal_id__isnull=True).exclude(internal_id__exact='')

    def available_to_user(self, user, service_type=None):
        qs_filter = {'client__users': user}
        if service_type:
            qs_filter['product__product_type'] = service_type
        return self.filter(**qs_filter)


class Service(models.Model):
    id = models.BigIntegerField(_('Random id'), default=RandomId('billing.Service'), primary_key=True)
    internal_id = models.CharField(max_length=255, null=True, blank=True, db_index=True,
                                   help_text='Internal ID for the product module')
    external_billing_id = models.CharField(null=True, blank=True, max_length=38)
    display_name = models.CharField(max_length=128, default=_('Service'))
    client = models.ForeignKey(Client, related_name='services', db_index=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='services', db_index=True, on_delete=models.PROTECT)
    cycle = models.ForeignKey(ProductCycle, related_name='services', null=True, blank=True, db_index=True,
                              on_delete=models.PROTECT)
    override_price = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True, default=None)
    status = models.CharField(max_length=16, choices=ServiceStatus.choices, db_index=True)
    task = models.CharField(max_length=16, choices=ServiceTask.choices, null=True, blank=True, db_index=True)
    notes = models.TextField(max_length=4096, blank=True)
    override_suspend_until = models.DateTimeField(null=True, blank=True, db_index=True)
    suspend_reason = models.CharField(max_length=255, null=True, blank=True)
    suspend_type = models.CharField(max_length=12, null=True, blank=True, db_index=True)
    created_at = models.DateTimeField(default=utcnow, db_index=True)
    activated_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(default=utcnow, db_index=True)
    suspended_at = models.DateTimeField(null=True, blank=True)
    terminated_at = models.DateTimeField(null=True, blank=True)
    auto_terminate_date = models.DateTimeField(null=True, blank=True, help_text='Auto terminate on this date')
    auto_terminate_reason = models.CharField(max_length=255, null=True, blank=True)
    next_due_date = models.DateTimeField(null=True, blank=True, db_index=True)
    next_expiration_date = models.DateTimeField(null=True, blank=True, db_index=True,
                                                help_text='Used for services that expire outside of Fleio,'
                                                          ' like domains. Next due and invoice due are usually set'
                                                          ' ahead of this date')
    next_invoice_date = models.DateTimeField(null=True, blank=True, db_index=True)
    cancellation_request = models.OneToOneField(CancellationRequest,
                                                related_name='service',
                                                null=True, blank=True,
                                                on_delete=models.SET_NULL)
    plugin_data = JSONField(default={})
    domain_name = models.CharField(max_length=256, null=True, blank=True)

    objects = ServiceQuerySet.as_manager()

    class Meta:
        ordering = ('-created_at', )

    @property
    def is_price_overridden(self):
        return self.override_price not in ('', None)

    def is_active(self) -> bool:
        if self.status == ServiceStatus.active:
            return True
        return False

    def set_active(self, activated_at=None):
        utc_now = utcnow()
        self.status = ServiceStatus.active
        self.activated_at = activated_at or utc_now
        if not self.next_due_date:
            self.next_due_date = self.activated_at
        self.updated_at = utc_now
        if self.auto_terminate_date:
            self.auto_terminate_date = None

        try:
            if self.cancellation_request:
                # delete cancellation request if exists
                self.cancellation_request.delete()
                self.cancellation_request = None
        except CancellationRequest.DoesNotExist:
            pass

        self.save(update_fields=[
            'status', 'activated_at', 'updated_at', 'next_due_date', 'cancellation_request', 'auto_terminate_date'
        ])

    def set_suspended(self, reason, suspend_type=None, suspended_at=None):
        utc_now = utcnow()
        self.status = ServiceStatus.suspended
        self.suspended_at = suspended_at or utc_now
        self.suspend_type = suspend_type
        self.suspend_reason = reason
        self.updated_at = utc_now
        self.save(update_fields=['status', 'suspended_at', 'suspend_type', 'suspend_reason', 'updated_at'])

    def set_terminated(self, cancellation_request_id=None):
        self.status = ServiceStatus.terminated
        self.terminated_at = utcnow()
        self.updated_at = self.terminated_at
        self.save(update_fields=['status', 'updated_at', 'terminated_at'])
        if cancellation_request_id:
            try:
                cr = CancellationRequest.objects.get(id=cancellation_request_id)
            except CancellationRequest.DoesNotExist:
                pass
            else:
                cr.completed_at = utcnow()
                cr.save(update_fields=['completed_at'])

    def set_status(self, new_status):
        self.status = new_status
        self.updated_at = utcnow()
        self.save(update_fields=['status', 'updated_at'])

    def get_next_due_date(self, previous_due_date: Optional[datetime.date] = None) -> datetime.date:
        if previous_due_date is None:
            if self.activated_at:
                return self.activated_at
            else:
                return utils.DATETIME_MAX
        else:
            if self.cycle:
                return self.cycle.get_next_due_date(
                    start_date=previous_due_date,
                    quantity=self.cycle.cycle_multiplier,
                    unit=self.cycle.cycle
                )
            else:
                return utils.DATETIME_MAX

    def update_next_due_date(self, previous_due_date=None, save_to_database=True):
        utc_now = utcnow()
        next_due_date = previous_due_date or self.next_due_date
        self.next_due_date = self.get_next_due_date(next_due_date)
        self.updated_at = utc_now
        if save_to_database:
            self.save(update_fields=['next_due_date', 'updated_at'])

    def update_next_invoice_date(self, previous_due_date=None, save_to_database=True, manual_invoice=False):
        """Get the next invoice date given self.due_date and self.cycle"""
        utc_now = utcnow()
        next_due_date = previous_due_date or self.next_due_date
        if next_due_date is None:
            next_due_date = utc_now
        if self.cycle:
            if manual_invoice:
                while True:
                    prev_due_date = next_due_date
                    next_due_date = self.cycle.get_next_due_date(
                        start_date=next_due_date, quantity=self.cycle.cycle_multiplier, unit=self.cycle.cycle,
                    )
                    next_invoice_date = next_due_date
                    if self.cycle.cycle in [
                        CyclePeriods.month, CyclePeriods.year,
                    ] and self.client.billing_settings.issue_invoice_before_next_due_date:
                        next_invoice_date = next_invoice_date - datetime.timedelta(
                            days=self.client.billing_settings.next_invoice_date_offset
                        )
                    if not self.next_invoice_date or prev_due_date >= self.next_invoice_date:
                        break
            else:
                next_invoice_date = self.cycle.get_next_due_date(
                    start_date=next_due_date, quantity=self.cycle.cycle_multiplier, unit=self.cycle.cycle,
                )
                if self.cycle.cycle in [
                    CyclePeriods.month, CyclePeriods.year,
                ] and self.client.billing_settings.issue_invoice_before_next_due_date:
                    next_invoice_date = next_invoice_date - datetime.timedelta(
                        days=self.client.billing_settings.next_invoice_date_offset
                    )

            self.next_invoice_date = next_invoice_date
        else:
            self.next_invoice_date = utils.DATETIME_MAX
        self.updated_at = utc_now
        if save_to_database:
            self.save(update_fields=['next_invoice_date', 'updated_at'])

    def get_fixed_price(self, currency=None) -> decimal.Decimal:
        """Returns a tuple of price and currency"""
        if not self.cycle:
            return decimal.Decimal('0.00')
        if self.is_price_overridden:
            fixed_price = self.override_price
        else:
            configurable_options_price = self.configurable_options.total_price()
            fixed_price = self.cycle.fixed_price + configurable_options_price
        if currency:
            return utils.convert_currency(fixed_price, to_currency=currency, from_currency=self.cycle.currency)
        else:
            return utils.convert_currency(fixed_price,
                                          to_currency=self.cycle.currency,
                                          from_currency=self.cycle.currency)

    def get_fixed_price_without_configurable_options(self, currency=None):
        if not self.cycle:
            return decimal.Decimal('0.00')
        if self.is_price_overridden:
            fixed_price = self.override_price
        else:
            fixed_price = self.cycle.fixed_price
        if currency:
            return utils.convert_currency(fixed_price, to_currency=currency, from_currency=self.cycle.currency)
        else:
            return utils.convert_currency(fixed_price,
                                          to_currency=self.cycle.currency,
                                          from_currency=self.cycle.currency)

    def get_previous_due_date(self, next_due_date=None):
        """
        Get previous due date based on current assigned cycle.
        DO NOTE: this does not work correctly if the cycle is changed before the next due date.
        """
        if not self.cycle:
            # FIXME(tomo): Free product
            return utcnow()
        elif self.cycle.cycle == CyclePeriods.onetime:
            return self.next_due_date
        elif self.cycle.cycle == CyclePeriods.hour:
            return self.next_due_date - datetime.timedelta(hours=float(self.cycle.cycle_multiplier))
        elif self.cycle.cycle == CyclePeriods.year:
            try:
                return self.next_due_date.replace(year=(self.next_due_date.year - self.cycle.cycle_multiplier))
            except ValueError:
                years_diff = (datetime.datetime(self.next_due_date.year - self.cycle.cycle_multiplier, 1, 1) -
                              datetime.datetime(self.next_due_date.year, 1, 1))
                return self.next_due_date - years_diff
        elif self.cycle.cycle == CyclePeriods.month:
            if next_due_date:
                nd = next_due_date
            else:
                nd = self.next_due_date
            if not nd:
                # FIXME(tomo): next_due_date may be None
                nd = utcnow()
            quantity = self.cycle.cycle_multiplier
            new_year = nd.year + int(nd.month - quantity - 1) // 12
            # (int(start_date.month + quantity - 1) % 12) + 1
            if nd.month > quantity:
                new_month = nd.month - quantity
            else:
                new_month = (int(nd.month - quantity - 1) % 12) + 1
            try:
                return nd.replace(year=new_year, month=new_month)
            except ValueError:
                # It means that the new month was shorter than the current causing to have an invalid day.
                # Skip to the first day of the following month.
                # (i.e. Jan 31 + 1 month = Feb 31, invalid day so skip to Mar 1)
                return nd.replace(year=new_year, month=new_month + 1, day=1)
        else:
            return self.next_due_date

    def is_suspend_overridden(self) -> bool:
        if self.override_suspend_until is None:
            return False
        else:
            current_date = utcnow()
            return self.override_suspend_until > current_date

    def __str__(self):
        return '{} {} {} {}'.format(self.client, self.id, self.cycle, self.status)
