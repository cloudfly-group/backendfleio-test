from typing import Optional

from django.db import models
from django.db.models import QuerySet

from fleio.billing.models import Product
from fleio.billing.models import Service
from fleio.billing.settings import PricingModel, PublicStatuses
from fleio.core.models import Currency


class ProductUtils:
    @staticmethod
    def available_for_order(currency=None):
        return Product.objects.available_for_order(currency=currency)

    @staticmethod
    def service_upgrade_products(service: Service) -> QuerySet:
        """Filter public packages with public cycles"""
        public_pkg = service.product.upgrades.filter(status=PublicStatuses.public)
        cycle_filter = models.Q(cycles__status=PublicStatuses.public, cycles__currency=service.cycle.currency)
        with_pub_cycles = public_pkg.filter(cycle_filter |
                                            models.Q(price_model=PricingModel.free))
        return with_pub_cycles.filter(models.Q(has_quantity=True, available_quantity__gt=0) |
                                      models.Q(has_quantity=False)).distinct()

    @staticmethod
    def product_cycles_available_for_upgrade(product: Product, currency: Optional[Currency] = None) -> QuerySet:
        if currency:
            return product.cycles.public().filter(currency=currency)
        else:
            return product.cycles.public()
