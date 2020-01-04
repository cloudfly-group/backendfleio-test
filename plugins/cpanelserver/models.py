from django.db import models

from fleio.billing.models import Product
from fleio.servers.models import ServerGroup


class CpanelServerProductSettings(models.Model):
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='cpanelserver_product_settings'
    )
    default_plan = models.CharField(max_length=255, null=True, blank=True)
    server_group = models.ForeignKey(ServerGroup, on_delete=models.SET_NULL, null=True)
