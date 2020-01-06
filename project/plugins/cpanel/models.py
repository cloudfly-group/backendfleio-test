from django.db import models

from fleio.billing.models import Product


class CpanelProductSettings(models.Model):
    product = models.OneToOneField(Product,
                                   related_name='cpanel_product_settings',
                                   on_delete=models.CASCADE)
    cpanel_package_id = models.IntegerField()
    cpanel_group_id = models.IntegerField()
