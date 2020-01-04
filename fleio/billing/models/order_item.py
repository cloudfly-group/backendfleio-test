import logging
import decimal
from django.db import models
from django.db.models import F, Sum
from django.db.models.functions import Coalesce
from django.utils.translation import ugettext_lazy as _
from jsonfield import JSONField

from fleio.billing.settings import CyclePeriods
from .service import Service
from .cart import FleioCart
from .order import Order
from .product import Product
from .product_cycle import ProductCycle

LOG = logging.getLogger(__name__)


class OrderItemTypes(object):
    service = 'service'
    serviceUpgrade = 'serviceUpgrade'
    credit = 'credit'
    other = 'other'

    CHOICES = ((service, _('Service')),
               (serviceUpgrade, _('Service Upgrade')),
               (credit, _('Credit Balance')),
               (other, _('Other')))

    def __contains__(self, item):
        return item in [c[0] for c in self.CHOICES]


class OrderItemQuerySet(models.QuerySet):
    def total_price(self):
        """Total price for items with config options and taxes"""
        with_opts = self.annotate(config_options_total=Sum('configurable_options__price') +
                                  Sum('configurable_options__setup_fee'))
        return with_opts.aggregate(total=Sum(F('fixed_price') + F('setup_fee')) +
                                   Coalesce(Sum('config_options_total'), 0) +
                                   Coalesce(Sum('taxes__amount'), 0))['total']


class OrderItem(models.Model):
    cart = models.ForeignKey(FleioCart, related_name='items', null=True, blank=True, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, related_name='items', null=True, blank=True, on_delete=models.CASCADE)
    item_type = models.CharField(choices=OrderItemTypes.CHOICES, db_index=True, max_length=16)
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE)
    cycle = models.ForeignKey(ProductCycle, null=True, blank=True, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, related_name='order_item', null=True, blank=True, db_index=True,
                                on_delete=models.SET_NULL)
    taxable = models.BooleanField(default=False)
    setup_fee = models.DecimalField(max_digits=12, decimal_places=2, default='0.00')
    fixed_price = models.DecimalField(max_digits=12, decimal_places=2, default='0.00')
    name = models.CharField(max_length=128, default='Product')
    description = models.CharField(max_length=255, default='')
    cycle_display = models.CharField(max_length=128, null=True, blank=True)
    plugin_data = JSONField(default={}, max_length=4096)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    domain_name = models.CharField(max_length=256, null=True, blank=True)
    domain_action = models.CharField(max_length=64, null=True, blank=True)

    objects = OrderItemQuerySet.as_manager()

    class Meta:
        ordering = ['-created_at']

    @property
    def currency(self):
        if self.cart:
            return self.cart.currency
        elif self.order:
            return self.order.currency
        else:
            return None

    @property
    def tax_amount(self):
        return self.taxes.aggregate(total=Sum('amount'))['total'] or decimal.Decimal('0.00')

    @property
    def setup_fees_total(self):
        return self.setup_fee + self.configurable_options_setup_fees

    @property
    def configurable_options_price(self):
        return self.configurable_options.aggregate(total=Sum('price'))['total'] or decimal.Decimal('0.00')

    @property
    def configurable_options_setup_fees(self):
        return self.configurable_options.aggregate(total=Coalesce(Sum('setup_fee'), 0))['total']

    @property
    def amount_without_taxes(self):
        return (self.fixed_price +
                self.setup_fee +
                self.configurable_options_price +
                self.configurable_options_setup_fees)

    @property
    def amount(self):
        amount = self.fixed_price + self.configurable_options_price
        amount += self.tax_amount
        if self.cycle and self.cycle.cycle == CyclePeriods.onetime:
            amount += self.setup_fee + self.configurable_options_setup_fees
        return amount

    def __str__(self):
        return '{} {}'.format(self.name, self.description or '')


class OrderItemTax(models.Model):
    cart_item = models.ForeignKey(OrderItem, related_name='taxes', on_delete=models.CASCADE)
    name = models.CharField(max_length=32, db_index=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=128, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
