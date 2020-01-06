from typing import Optional

from django.db import models
from django.utils.translation import ugettext_lazy as _

from fleio.billing.settings import PricingModel
from fleio.billing.settings import ProductAutoSetup
from fleio.billing.settings import ProductType
from fleio.billing.settings import PublicStatuses
from fleio.core.models import Currency
from fleio.core.utils import RandomId
from .configurable_option import ConfigurableOption
from .product_group import ProductGroup
from .product_module import ProductModule


class ProductQueryset(models.QuerySet):
    def available_for_order(self, currency=None):
        """Public products with public cycles or free and with quantity if defined"""
        public_pkg = self.filter(status=PublicStatuses.public)
        if currency:
            cycle_filter = models.Q(cycles__status=PublicStatuses.public, cycles__currency=currency)
        else:
            cycle_filter = models.Q(cycles__status=PublicStatuses.public)
        with_pub_cycles = public_pkg.filter(cycle_filter |
                                            models.Q(price_model=PricingModel.free))
        return with_pub_cycles.filter(models.Q(has_quantity=True, available_quantity__gt=0) |
                                      models.Q(has_quantity=False)).distinct()

    def free(self):
        return self.filter(price_model=PricingModel.free)

    def get_by_natural_key(self, code):
        return self.get(code=code)


class Product(models.Model):
    """
    Defines billable service product. It includes web hosting products, but also domain registration pricing and
    cloud services with utility priced model.
    """
    id = models.BigIntegerField(_('Random id'), default=RandomId('billing.Product'), primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=1024, blank=True, null=True)
    code = models.CharField(max_length=255, db_index=True, unique=True, help_text='Human readable id')
    group = models.ForeignKey(ProductGroup, on_delete=models.PROTECT, related_name='products')
    module = models.ForeignKey(ProductModule, on_delete=models.PROTECT, related_name='products')
    product_type = models.CharField(max_length=16, choices=ProductType.choices)
    status = models.CharField(max_length=12, choices=PublicStatuses.choices, db_index=True,
                              default=PublicStatuses.private)
    price_model = models.CharField(max_length=32, choices=PricingModel.choices, db_index=True)
    auto_setup = models.CharField(max_length=16, choices=ProductAutoSetup.choices, db_index=True,
                                  default=ProductAutoSetup.disabled)
    has_quantity = models.BooleanField(default=False)
    available_quantity = models.PositiveIntegerField(default=0)
    taxable = models.BooleanField(default=False, help_text='Add level 1 and 2 tax rates if applicable')
    configurable_options = models.ManyToManyField(ConfigurableOption,
                                                  through='billing.ProductConfigurableOption',
                                                  through_fields=('product', 'configurable_option'),
                                                  related_name='products', blank=True)
    upgrades = models.ManyToManyField('self', blank=True)
    requires_domain = models.BooleanField(default=False)
    hide_services = models.BooleanField(default=False)

    objects = ProductQueryset.as_manager()

    class Meta:
        ordering = ['name']

    def upgrades_with_cycles(self, currency: Optional[Currency] = None):
        if currency:
            return self.upgrades.filter(cycles__isnull=False, cycles__currency=currency).distinct()
        else:
            return self.upgrades.filter(cycles__isnull=False).distinct()

    def get_natural_key(self):
        return self.code

    @property
    def is_free(self):
        return self.price_model == PricingModel.free

    def __str__(self):
        return self.name
