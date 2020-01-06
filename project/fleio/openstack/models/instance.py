from jsonfield import JSONField

from django.db import models
from django.utils.functional import cached_property

from fleio.openstack.instances.instance_status import INSTANCE_STATE_MAP
from fleio.openstack.models import OpenstackInstanceFlavor
from fleio.openstack.models.project import Project
from fleio.openstack.models.region import OpenstackRegion
from fleio.openstack.models.network_port import Port
from fleio.openstack.models.image import Image


class Instance(models.Model):
    id = models.CharField(max_length=36, unique=True, db_index=True, primary_key=True)
    region = models.CharField(max_length=128, db_index=True)
    user_id = models.CharField(max_length=36, null=True, blank=True, db_index=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    addresses = JSONField(default=dict())
    accessIPv4 = models.GenericIPAddressField(null=True, blank=True)
    accessIPv6 = models.GenericIPAddressField(null=True, blank=True)
    flavor = models.ForeignKey(OpenstackInstanceFlavor, null=True, blank=True, db_index=True, db_constraint=False,
                               on_delete=models.DO_NOTHING)
    hostId = models.CharField(max_length=255, null=True, blank=True)
    host_name = models.CharField(max_length=255, null=True, blank=True)
    image = models.ForeignKey(Image, null=True, blank=True, db_index=True, db_constraint=False,
                              on_delete=models.DO_NOTHING)
    key_name = models.CharField(max_length=255, null=True, blank=True)
    config_drive = models.BooleanField(default=False)
    availability_zone = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    auto_disk_config = models.BooleanField(default=False)
    power_state = models.SmallIntegerField(default=0)
    task_state = models.CharField(max_length=255, null=True, blank=True)
    vm_state = models.CharField(max_length=255, null=True, blank=True)
    volumes_attached = JSONField(default=list())
    created = models.DateTimeField(blank=True, null=True)
    launched_at = models.DateTimeField(null=True, blank=True, db_index=True)
    updated = models.DateTimeField(null=True, blank=True, db_index=True)
    terminated_at = models.DateTimeField(null=True, blank=True)
    security_groups = JSONField(default=list())
    status = models.CharField(max_length=255, default='UNKNOWN', db_index=True)
    host_status = models.CharField(max_length=255, null=True, blank=True)
    fault = JSONField(null=True, blank=True)
    extra = JSONField(null=True, blank=True)
    locked = models.BooleanField(default=False)
    sync_version = models.BigIntegerField(default=0)

    project = models.ForeignKey(Project, db_constraint=False, null=True, blank=True,
                                on_delete=models.DO_NOTHING, to_field='project_id')

    booted_from_iso = models.BooleanField(default=False, blank=True, null=False)
    current_month_traffic = models.BigIntegerField(default=0)
    current_cycle_traffic = models.BigIntegerField(default=0)
    stopped_by_fleio = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Instances'
        ordering = ['-created']

    def access_ip(self):
        for port in self.ports:
            for fixed_ip in port.fixed_ips:
                return fixed_ip.get('ip_address')
        return None

    def update_status(self, status, task_state=None):
        # FIXME(tomo): status may not be null ?
        if self.status != status:
            self.status = status
        if self.task_state != task_state:
            self.task_state = task_state
        self.save()

    def display_status(self):
        status_dict = INSTANCE_STATE_MAP.get(self.status, None) or INSTANCE_STATE_MAP.get('unknown')
        return status_dict.get(self.task_state, None) or status_dict.get('default', None)

    def display_task(self):
        if self.task_state:
            return self.task_state.replace('_', ' ')
        else:
            return None

    @property
    def ports(self):
        return Port.objects.filter(device_id=self.id)

    @cached_property
    def region_obj(self) -> OpenstackRegion:
        return OpenstackRegion.objects.filter(id=self.region).first()

    def __str__(self):
        return '{} {}'.format(self.name, self.id)
