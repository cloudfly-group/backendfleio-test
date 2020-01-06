from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from jsonfield import JSONField


@python_2_unicode_compatible
class Subnet(models.Model):
    IPV_CHOICES = ((4, 'IPv4'), (6, 'IPv6'))
    id = models.CharField(max_length=36, unique=True, db_index=True, primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    network = models.ForeignKey('openstack.Network', db_constraint=False, on_delete=models.DO_NOTHING, null=True,
                                blank=True)
    project_id = models.CharField(max_length=36, null=True, blank=True, db_index=True)
    subnetpool_id = models.CharField(max_length=36, null=True, blank=True, db_index=True)
    ip_version = models.SmallIntegerField(choices=IPV_CHOICES)
    gateway_ip = models.GenericIPAddressField(null=True, blank=True)
    cidr = models.CharField(max_length=64)
    enable_dhcp = models.BooleanField(default=False)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    sync_version = models.BigIntegerField(default=0)
    extra = JSONField(default=dict())
    allocation_pools = JSONField(default=list())

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return "{} - {}".format(self.name, self.description)
