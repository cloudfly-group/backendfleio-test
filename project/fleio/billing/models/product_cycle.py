import datetime
import decimal

from django.db import models
from django.utils.translation import ugettext_lazy as _

from fleio.billing.settings import CyclePeriods, PublicStatuses
from fleio.billing.utils import DATETIME_MAX
from fleio.core.models import Currency, get_default_currency

from .product import Product


class ProductCycleQuerySet(models.QuerySet):
    def public(self):
        return self.filter(status=PublicStatuses.public)

    def available_for_order(self, currency=None):
        """Cycles available for new orders only"""
        pub_filter = self.filter(status=PublicStatuses.public)
        if currency:
            return pub_filter.filter(currency=currency)
        return pub_filter

    def available_to_clients(self):
        """Cycles already present in client services, public or retired usually"""
        return self.filter(status__in=(PublicStatuses.public, PublicStatuses.private, PublicStatuses.retired))


class ProductCycle(models.Model):
    """Product's pricing details."""
    product = models.ForeignKey(Product, related_name='cycles', on_delete=models.PROTECT)
    cycle = models.CharField(max_length=8, choices=CyclePeriods.choices)
    cycle_multiplier = models.IntegerField(default=1)
    fixed_price = models.DecimalField(max_digits=14, decimal_places=2, default=decimal.Decimal('0.00'))
    setup_fee = models.DecimalField(max_digits=14, decimal_places=2, default=decimal.Decimal('0.00'))
    setup_fee_entire_quantity = models.BooleanField(default=True, help_text=_('Apply to each or all items on order'))
    # Allows to have Product pricing in multiple currencies
    currency = models.ForeignKey(Currency, null=True, blank=True, default=get_default_currency,
                                 on_delete=models.SET_DEFAULT)
    # when False the price does not change automatically based on exchange rates
    # when True the price will update automatically (when cron runs) based on Plan.currency exchange rate
    # to self.currency (when actually Plan.currency != BillingCycle.currency)
    is_relative_price = models.BooleanField(default=True)
    status = models.CharField(max_length=12, choices=PublicStatuses.choices, db_index=True,
                              default=PublicStatuses.public)

    objects = ProductCycleQuerySet.as_manager()

    class Meta:
        unique_together = ('product', 'cycle', 'cycle_multiplier', 'currency')

    def __str__(self):
        return "{0} @ {1} x {2} {3}".format(self.product.name, self.cycle_multiplier, self.cycle, self.currency)

    @property
    def display_name(self):
        return CyclePeriods.display_name(cycle=self.cycle, multiplier=self.cycle_multiplier)

    @property
    def name(self):
        return "{0}".format(self.cycle)

    @staticmethod
    def get_next_due_date(start_date, quantity, unit):
        """
        Returns the next due date by adding
        :param quantity: int, multiplied by unit
        :param unit: int, possible values are defined in CyclePeriods.choices.
        :param start_date: datetime
        """
        if unit == CyclePeriods.onetime:
            return DATETIME_MAX
        elif unit == CyclePeriods.hour:
            return start_date + datetime.timedelta(hours=float(quantity))
        # elif unit == CyclePeriods.day:
        #    return start_date + datetime.timedelta(days=quantity)
        # elif unit == CyclePeriods.week:
        #    return start_date + datetime.timedelta(weeks=quantity)
        elif unit == CyclePeriods.month:
            new_year = start_date.year + int(start_date.month + quantity - 1) // 12
            new_month = (int(start_date.month + quantity - 1) % 12) + 1
            try:
                return start_date.replace(year=new_year, month=new_month)
            except ValueError:
                # It means that the new month was shorter than the current causing to have an invalid day.
                # Skip to the first day of the following month.
                # (i.e. Jan 31 + 1 month = Feb 31, invalid day so skip to Mar 1)
                return start_date.replace(year=new_year, month=new_month + 1, day=1)
        elif unit == CyclePeriods.year:
            try:
                return start_date.replace(year=start_date.year + quantity)
            except ValueError:
                return start_date + (datetime.datetime(start_date.year + quantity, 1, 1) -
                                     datetime.datetime(start_date.year, 1, 1))
        else:
            raise ValueError('Unknown cycle unit')
