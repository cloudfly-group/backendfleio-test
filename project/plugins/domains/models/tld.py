from typing import List

from django.db.models import QuerySet
from jsonfield import JSONField

from django.db import models
from django.db import transaction
from django.utils.translation import ugettext_lazy as _

from fleio.billing.models import ConfigurableOption, ProductConfigurableOption
from fleio.billing.models import Product
from fleio.billing.models import ProductGroup
from fleio.billing.models import ProductModule
from fleio.billing.models.configurable_option import ConfigurableOptionStatus
from fleio.billing.models.configurable_option import ConfigurableOptionWidget

from fleio.billing.settings import CyclePeriods
from fleio.billing.settings import PricingModel
from fleio.billing.settings import ProductType
from fleio.billing.settings import PublicStatuses

from fleio.core.models import Currency
from plugins.domains.settings import BILLING_MODULE_NAME

from .registrar import Registrar


class PriceType:
    register = 'register'
    transfer = 'transfer'
    renew = 'renew'

    price_type_map = {
        register: _('Register'),
        transfer: _('Transfer'),
        renew: _('Renew'),
    }


class AddonPriceType:
    dns = 'dns'
    email = 'email'
    id = 'id'

    price_type_map = {
        dns: _('DNS management'),
        email: _('Email forwarding'),
        id: _('ID protection'),
    }


class WhoisServerType:
    tcp = 'tcp'
    http = 'http'

    whois_server_type_map = {
        tcp: _('TCP'),
        http: _('HTTP'),
    }


class PriceCycles:
    def __init__(
            self,
            price_type: str,
            prices_per_years: List[int] = None,
            currency: Currency = None,
            currency_code: str = None,
            relative_prices: bool = None,
            **kwargs):
        del kwargs  # unused
        self.currency = currency
        self.currency_code = currency_code if currency_code else currency.code if currency else None
        if self.currency is None:
            self.currency = Currency.objects.get(code=self.currency_code)
        self.price_type = price_type
        if prices_per_years:
            self.prices_per_years = prices_per_years
        else:
            self.prices_per_years = [None] * 10

        self.relative_prices = relative_prices if relative_prices else False

    def save(self, product: Product):
        with transaction.atomic():
            for (index, price) in enumerate(self.prices_per_years):
                years = index + 1
                cycle = product.cycles.filter(
                    currency=self.currency,
                    cycle_multiplier=years,
                    cycle=CyclePeriods.year
                ).first()

                if price is None or price < 0:
                    if cycle:
                        cycle.delete()
                else:
                    if not cycle:
                        cycle = product.cycles.create()

                    cycle.fixed_price = price
                    cycle.currency = self.currency
                    cycle.cycle_multiplier = years
                    cycle.cycle = CyclePeriods.year
                    cycle.is_relative_price = self.relative_prices

                    cycle.save()

    def load(self, product: Product):
        cycles = product.cycles.filter(
            currency=self.currency,
            cycle=CyclePeriods.year
        ).all()

        self.prices_per_years = [None] * 10
        self.relative_prices = cycles.count() > 0

        for cycle in cycles:
            self.prices_per_years[int(cycle.cycle_multiplier - 1)] = cycle.fixed_price
            self.relative_prices = self.relative_prices and cycle.is_relative_price


class AddonPriceCycles:
    def __init__(
            self,
            price_type: str,
            prices_per_years: List[int] = None,
            currency: Currency = None,
            currency_code: str = None,
            relative_prices: bool = None,
            **kwargs):
        del kwargs  # unused
        self.currency = currency
        self.currency_code = currency_code if currency_code else currency.code if currency else None
        if self.currency is None:
            self.currency = Currency.objects.get(code=self.currency_code)
        self.price_type = price_type
        if prices_per_years:
            self.prices_per_years = prices_per_years
        else:
            self.prices_per_years = [None] * 10

        self.relative_prices = relative_prices if relative_prices else False

    def save(self, configurable_option: ConfigurableOption):
        with transaction.atomic():
            for (index, price) in enumerate(self.prices_per_years):
                years = index + 1
                cycle = configurable_option.cycles.filter(
                    currency=self.currency,
                    cycle_multiplier=years,
                    cycle=CyclePeriods.year
                ).first()

                if price is None or price < 0:
                    if cycle:
                        cycle.delete()
                else:
                    if not cycle:
                        cycle = configurable_option.cycles.create()

                    cycle.price = price
                    cycle.currency = self.currency
                    cycle.cycle_multiplier = years
                    cycle.cycle = CyclePeriods.year
                    cycle.is_relative_price = self.relative_prices

                    cycle.save()

    def load(self, configurable_option: ConfigurableOption):
        cycles = configurable_option.cycles.filter(
            currency=self.currency,
            cycle=CyclePeriods.year
        ).all()

        self.prices_per_years = [None] * 10
        self.relative_prices = cycles.count() > 0

        for cycle in cycles:
            self.prices_per_years[int(cycle.cycle_multiplier - 1)] = cycle.price
            self.relative_prices = self.relative_prices and cycle.is_relative_price


def default_edit_options():
    return {}


class TLD(models.Model):
    name = models.CharField(max_length=128, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    premium_domains_available = models.BooleanField(default=False)
    edit_options = JSONField(default=default_edit_options())
    register_product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='+', null=True, blank=True)
    transfer_product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='+', null=True, blank=True)
    renew_product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='+', null=True, blank=True)
    dns_option = models.ForeignKey(
        ConfigurableOption,
        on_delete=models.PROTECT,
        related_name='+',
        null=True,
        blank=True,
    )
    email_option = models.ForeignKey(
        ConfigurableOption,
        on_delete=models.PROTECT,
        related_name='+',
        null=True,
        blank=True,
    )
    id_option = models.ForeignKey(
        ConfigurableOption,
        on_delete=models.PROTECT,
        related_name='+',
        null=True,
        blank=True,
    )
    registrars = models.ManyToManyField(Registrar, related_name='tlds', blank=True)
    default_registrar = models.ForeignKey(
        Registrar,
        related_name='default_for_tlds',
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    requires_epp_for_transfer = models.BooleanField(default=True, null=False, blank=True)

    def get_price_cycles_list(self):
        self.initialize_products()

        price_cycles_list = []
        for currency in Currency.objects.all():
            for price_type in PriceType.price_type_map:
                price_cycles = PriceCycles(
                    price_type=price_type,
                    currency=currency,
                )

                if price_type == PriceType.register:
                    price_cycles.load(self.register_product)

                if price_type == PriceType.transfer:
                    price_cycles.load(self.transfer_product)

                if price_type == PriceType.renew:
                    price_cycles.load(self.renew_product)

                price_cycles_list.append(price_cycles)

        return price_cycles_list

    def get_addon_price_cycles_list(self):
        self.initialize_configurable_options()

        price_cycles_list = []
        for currency in Currency.objects.all():
            for price_type in AddonPriceType.price_type_map:
                price_cycles = AddonPriceCycles(
                    price_type=price_type,
                    currency=currency,
                )

                if price_type == AddonPriceType.dns:
                    price_cycles.load(configurable_option=self.dns_option)

                if price_type == AddonPriceType.email:
                    price_cycles.load(configurable_option=self.email_option)

                if price_type == AddonPriceType.id:
                    price_cycles.load(configurable_option=self.id_option)

                price_cycles_list.append(price_cycles)

        return price_cycles_list

    def get_prices_for_type_and_currency(self, price_type: str, currency: Currency) -> PriceCycles:
        self.initialize_products()

        price_cycles = PriceCycles(
            price_type=price_type,
            currency=currency,
        )

        if price_type == PriceType.register:
            price_cycles.load(self.register_product)

        if price_type == PriceType.transfer:
            price_cycles.load(self.transfer_product)

        if price_type == PriceType.renew:
            price_cycles.load(self.renew_product)

        return price_cycles

    def get_addon_prices_for_type_and_currency(self, price_type: str, currency: Currency) -> AddonPriceCycles:
        self.initialize_configurable_options()

        price_cycles = AddonPriceCycles(
            price_type=price_type,
            currency=currency,
        )

        if price_type == AddonPriceType.dns:
            price_cycles.load(self.dns_option)

        if price_type == AddonPriceType.email:
            price_cycles.load(self.email_option)

        if price_type == AddonPriceType.id:
            price_cycles.load(self.id_option)

        return price_cycles

    def initialize_configurable_options(self):
        self.initialize_products()

        with transaction.atomic():
            # create configurable options
            if self.dns_option is None:
                option_name = '{}_dns_management'.format(self.name)
                self.dns_option = ConfigurableOption.objects.filter(name=option_name).first()
                if self.dns_option is None:
                    self.dns_option = ConfigurableOption.objects.create(
                        description='{} DNS management'.format(self.name),
                        name=option_name,
                        widget=ConfigurableOptionWidget.yesno,
                        status=ConfigurableOptionStatus.public,
                        visible=False,
                    )

            if self.email_option is None:
                option_name = '{}_email_forwarding'.format(self.name)
                self.email_option = ConfigurableOption.objects.filter(name=option_name).first()
                if self.email_option is None:
                    self.email_option = ConfigurableOption.objects.create(
                        description='{} email forwarding'.format(self.name),
                        name=option_name,
                        widget=ConfigurableOptionWidget.yesno,
                        status=ConfigurableOptionStatus.public,
                        visible=False,
                    )

            if self.id_option is None:
                option_name = '{}_id_protection'.format(self.name)
                self.id_option = ConfigurableOption.objects.filter(name=option_name).first()
                if self.id_option is None:
                    self.id_option = ConfigurableOption.objects.create(
                        description='{} ID protection'.format(self.name),
                        name=option_name,
                        widget=ConfigurableOptionWidget.yesno,
                        status=ConfigurableOptionStatus.public,
                        visible=False,
                    )

            self.save()

            configurable_options = ConfigurableOption.objects.filter(
                id__in=[self.dns_option.id, self.email_option.id, self.id_option.id],
            ).all()

            TLD.check_and_associate_configurable_options(product=self.register_product, options=configurable_options)
            TLD.check_and_associate_configurable_options(product=self.renew_product, options=configurable_options)
            TLD.check_and_associate_configurable_options(product=self.transfer_product, options=configurable_options)

    @staticmethod
    def check_and_associate_configurable_options(product: Product, options: QuerySet):
        with transaction.atomic():
            # associate options with product
            if ProductConfigurableOption.objects.filter(
                    product=product,
                    configurable_option__in=options,
            ).count() < 3:
                ProductConfigurableOption.objects.filter(product=product).delete()
                for configurable_option in options.all():
                    ProductConfigurableOption.objects.create(
                        product=product,
                        configurable_option=configurable_option
                    )
                    product.save()

    def initialize_products(self):
        with transaction.atomic():
            domains_group = ProductGroup.objects.filter(name='Domains').first()
            if domains_group is None:
                domains_group = ProductGroup.objects.create(
                    name='Domains',
                    description='Used internally by domains plugin for domain related products',
                    visible=False,
                )
            else:
                if domains_group.visible:
                    # ensure domains group is not visible
                    domains_group.visible = False
                    domains_group.save(update_fields=['visible'])

            if self.register_product is None:
                product_code = 'register_{}_domain'.format(self.name)
                self.register_product = domains_group.products.filter(code=product_code).first()
                if self.register_product is None:
                    self.register_product = Product.objects.create(
                        name='Register {} domain'.format(self.name),
                        code=product_code,
                        group=domains_group,
                        module=ProductModule.objects.get(name=BILLING_MODULE_NAME),
                        price_model=PricingModel.fixed_and_dynamic,
                        product_type=ProductType.domain,
                        status=PublicStatuses.public,
                    )

            if self.transfer_product is None:
                product_code = 'transfer_{}_domain'.format(self.name)
                self.transfer_product = domains_group.products.filter(code=product_code).first()
                if self.transfer_product is None:
                    self.transfer_product = Product.objects.create(
                        name='Transfer {} domain'.format(self.name),
                        code=product_code,
                        group=domains_group,
                        module=ProductModule.objects.get(name=BILLING_MODULE_NAME),
                        price_model=PricingModel.fixed_and_dynamic,
                        product_type=ProductType.domain,
                        status=PublicStatuses.public,
                    )

            if self.renew_product is None:
                product_code = 'renew_{}_domain'.format(self.name)
                self.renew_product = domains_group.products.filter(code=product_code).first()
                if self.renew_product is None:
                    self.renew_product = Product.objects.create(
                        name='Renew {} domain'.format(self.name),
                        code=product_code,
                        group=domains_group,
                        module=ProductModule.objects.get(name=BILLING_MODULE_NAME),
                        price_model=PricingModel.fixed_and_dynamic,
                        product_type=ProductType.domain,
                        status=PublicStatuses.public,
                    )

            self.save()

    @property
    def stripped_name(self):
        return self.name.lstrip('.')

    def save_prices(self, price_cycles_object_list: List[PriceCycles]):
        self.initialize_products()

        for price_cycles in price_cycles_object_list:
            if price_cycles.price_type == PriceType.register:
                price_cycles.save(product=self.register_product)

            if price_cycles.price_type == PriceType.transfer:
                price_cycles.save(product=self.transfer_product)

            if price_cycles.price_type == PriceType.renew:
                price_cycles.save(product=self.renew_product)

    def save_addon_prices(self, price_cycles_object_list: List[AddonPriceCycles]):
        self.initialize_configurable_options()

        for price_cycles in price_cycles_object_list:
            if price_cycles.price_type == AddonPriceType.dns:
                price_cycles.save(configurable_option=self.dns_option)

            if price_cycles.price_type == AddonPriceType.email:
                price_cycles.save(configurable_option=self.email_option)

            if price_cycles.price_type == AddonPriceType.id:
                price_cycles.save(configurable_option=self.id_option)

    def __str__(self):
        return self.name
