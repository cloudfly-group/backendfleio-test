from django.db import models
from django.utils.translation import ugettext_lazy as _

from fleio.core.exceptions import APIBadRequest
from ..utils import config_option_cycles_match_product
from .product import Product
from .configurable_option import ConfigurableOption


class ProductConfigurableOption(models.Model):
    """Product to Configurable option through model"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_index=True)
    configurable_option = models.ForeignKey(ConfigurableOption, on_delete=models.CASCADE, db_index=True)

    class Meta:
        unique_together = ('product', 'configurable_option')

    def cycles_match(self):
        """Checks if all product cycles are present in configurable option"""
        return config_option_cycles_match_product(configurable_option=self.configurable_option,
                                                  product=self.product)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if ProductConfigurableOption.objects.filter(
            product=self.product, configurable_option__name=self.configurable_option.name
        ).count() > 0:
            raise APIBadRequest(
                detail=_('Cannot add configurable option as a configurable option with the same internal name was '
                         'already used on this product')
            )
        return super().save(
            force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields
        )

    def __str__(self):
        return '{} {}'.format(self.product.name, self.configurable_option.name)
