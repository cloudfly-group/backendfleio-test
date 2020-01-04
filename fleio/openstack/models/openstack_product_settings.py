from django.db import models

from fleio.billing.models import Product

from .region import OpenstackRegion


class OpenstackProductSettings(models.Model):
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='openstack_product_settings'
    )
    run_get_me_a_network_on_auto_setup = models.BooleanField(default=False)
    network_auto_allocated_topology_regions = models.ManyToManyField(
        OpenstackRegion,
        blank=True,
        related_name='os_product_settings',
    )
