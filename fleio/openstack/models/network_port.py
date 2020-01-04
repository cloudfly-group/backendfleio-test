import ipaddress

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from jsonfield import JSONField

from .network import Network


@python_2_unicode_compatible
class Port(models.Model):
    id = models.CharField(max_length=36, unique=True, db_index=True, primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    admin_state_up = models.BooleanField(default=True)
    device_id = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    device_owner = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    fixed_ips = JSONField(default=dict())
    mac_address = models.CharField(max_length=32, null=True, blank=True)
    network = models.ForeignKey('openstack.Network', db_constraint=False, on_delete=models.DO_NOTHING,
                                null=True, blank=True, related_name='ports')
    project = models.ForeignKey('openstack.Project', db_constraint=False, null=True, blank=True,
                                on_delete=models.DO_NOTHING, to_field='project_id')
    security_groups = JSONField(default=list())
    sync_version = models.BigIntegerField(default=0)
    extra = JSONField(default=dict())

    class Meta:
        ordering = ['-sync_version']

    def network_name(self):
        try:
            if self.network:
                return self.network.name
            else:
                return _('Network')
        except Network.DoesNotExist:
            return _('Network')

    def ip_addresses(self):
        return [fip['ip_address'] for fip in self.fixed_ips]

    def is_private(self):
        is_private = True
        for ip_address in self.ip_addresses():
            try:
                is_private = is_private and ipaddress.IPv4Address(ip_address).is_private
            except Exception as v4e:
                del v4e  # we are not interested in exception here
                try:
                    is_private = is_private and ipaddress.IPv6Address(ip_address).is_private
                except Exception as v6e:
                    del v6e  # we are not interested in exception here

            if not is_private:
                break

        return is_private

    def __str__(self):
        return "{} - {} - {} - {}".format(self.id, self.device_id, self.name, self.description)
