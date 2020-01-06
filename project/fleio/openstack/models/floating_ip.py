from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from fleio.openstack.models.instance import Instance
from fleio.openstack.models.network_port import Port


@python_2_unicode_compatible
class FloatingIp(models.Model):
    id = models.CharField(_('Floating Ip UUID'), max_length=36, unique=True, primary_key=True)
    floating_ip_address = models.GenericIPAddressField()
    floating_network = models.ForeignKey('openstack.Network', db_constraint=False, on_delete=models.DO_NOTHING,
                                         null=True, blank=True)
    status = models.CharField(_('Status'), max_length=10)
    router = models.ForeignKey('openstack.Router', db_constraint=False, null=True, blank=True,
                               on_delete=models.DO_NOTHING)
    description = models.CharField(max_length=200, null=True, blank=True)
    project = models.ForeignKey('openstack.Project', db_constraint=False, null=True, blank=True,
                                on_delete=models.DO_NOTHING, to_field='project_id')
    fixed_ip_address = models.GenericIPAddressField(null=True, blank=True)
    port = models.ForeignKey('openstack.Port', db_constraint=False, null=True, blank=True, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    revision_number = models.IntegerField(blank=True, null=True)
    sync_version = models.BigIntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

    @property
    def instance(self):
        return Instance.objects.filter(id=Port.objects.filter(id=self.port_id,
                                                              device_owner__startswith='compute:').values_list(
            'device_id').first()).first()

    def __str__(self):
        return self.floating_ip_address
