from django.db import models

from fleio.servers.models import Server

from fleio.billing.models import Product


class HypanelProductSettings(models.Model):
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='hypanel_product_settings'
    )
    hypanel_server = models.ForeignKey(
        Server,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='hypanel_server_settings'
    )
    hostname = models.CharField(max_length=255, blank=True, default="")
    configuration = models.CharField(max_length=255, null=True, blank=True)
    memory = models.IntegerField(null=True)
    disk_size = models.IntegerField(null=True)
    ip_count = models.IntegerField(default=1)
    traffic = models.IntegerField(null=True)
    machine_type = models.CharField(max_length=10, default='openvz')
    server_group = models.CharField(max_length=255, null=True, blank=True)
    send_welcome_email = models.BooleanField(default=False)
