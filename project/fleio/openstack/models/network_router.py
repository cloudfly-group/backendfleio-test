from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from jsonfield import JSONField

from .network import Network


@python_2_unicode_compatible
class Router(models.Model):
    id = models.CharField(max_length=36, db_index=True, primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    region = models.ForeignKey('openstack.OpenstackRegion', db_constraint=False, null=True, blank=True,
                               on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=16, blank=True, null=True)
    admin_state_up = models.BooleanField(default=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    project_id = models.CharField(max_length=36, null=True, blank=True, db_index=True)
    external_network_id = models.CharField(max_length=36, null=True, blank=True, db_index=True)
    external_fixed_ips = JSONField(default=list())
    enable_snat = models.BooleanField(default=True)
    availability_zones = JSONField(default=list())
    availability_hints = JSONField(default=list())
    distributed = models.BooleanField(default=False)
    ha = models.BooleanField(verbose_name='High availability', default=False)
    routes = JSONField(default=list())

    sync_version = models.BigIntegerField(default=0)

    def __str__(self):
        return "{}".format(self.name)

    def network_name(self):
        try:
            network = Network.objects.get(id=self.external_network_id)
            return network.name
        except Network.DoesNotExist:
            return '-'
