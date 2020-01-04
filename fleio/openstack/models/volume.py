from django.db import models, transaction
from django.utils.encoding import python_2_unicode_compatible
from jsonfield import JSONField

from fleio.openstack.models.instance import Instance
from fleio.openstack.models.project import Project
from fleio.openstack.models.region import OpenstackRegion


@python_2_unicode_compatible
class Volume(models.Model):
    id = models.CharField(max_length=36, unique=True, primary_key=True)
    region = models.CharField(max_length=128)
    project = models.ForeignKey('openstack.Project', db_constraint=False, null=True, blank=True,
                                on_delete=models.DO_NOTHING, to_field='project_id')
    user_id = models.CharField(max_length=36, null=True, blank=True, db_index=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=32, blank=True)
    attach_status = models.CharField(max_length=255, blank=True, null=True)
    size = models.IntegerField()
    type = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    consistencygroup_id = models.CharField(max_length=36, null=True, blank=True, db_index=True)
    source_volid = models.CharField(max_length=36, null=True, blank=True, db_index=True)
    snapshot_id = models.CharField(max_length=36, null=True, blank=True, db_index=True)
    bootable = models.BooleanField(default=False)
    multiattach = models.BooleanField(default=False)
    availability_zone = models.CharField(max_length=255, null=True, blank=True)
    migration_status = models.CharField(max_length=255, null=True, blank=True)
    replication_status = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    sync_version = models.BigIntegerField(default=0)
    extra = JSONField(default=dict())

    class Meta:
        ordering = ['-created_at']

    def delete(self, using=None, keep_parents=False):
        with transaction.atomic():
            VolumeAttachments.objects.filter(volume_id=self.id).delete()
            return super(Volume, self).delete(using, keep_parents)

    @property
    def display_name(self):
        return self.name or self.id

    @property
    def attachments(self):
        return VolumeAttachments.objects.filter(volume_id=self.id)

    def __str__(self):
        return "{} - {}".format(self.name, self.id)


class VolumeBackup(models.Model):
    id = models.CharField(max_length=36, unique=True, primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=32, blank=True)
    object_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    has_dependent_backups = models.BooleanField(default=False)
    size = models.IntegerField()
    is_incremental = models.BooleanField(default=False)
    project = models.ForeignKey(
        Project, db_constraint=False, null=True, blank=True, on_delete=models.DO_NOTHING,
        to_field='project_id'
    )
    volume = models.ForeignKey(
        Volume, null=True, blank=True, db_index=True, db_constraint=False, on_delete=models.DO_NOTHING
    )
    snapshot_id = models.CharField(max_length=36, null=True, blank=True, default=None)
    sync_version = models.BigIntegerField(default=0)
    region = models.ForeignKey(OpenstackRegion, on_delete=models.SET_NULL, null=True, blank=False, default=None)

    objects = models.Manager


@python_2_unicode_compatible
class VolumeAttachments(models.Model):
    id = models.CharField(max_length=36, unique=True, primary_key=True)
    volume_id = models.CharField(max_length=36, db_index=True)
    server_id = models.CharField(max_length=36, null=True, blank=True, db_index=True)
    sync_version = models.BigIntegerField(default=0)
    extra = JSONField(default=dict())

    @property
    def instance(self):
        if self.server_id:
            return Instance.objects.get(id=self.server_id)
        else:
            return None

    @property
    def volume(self):
        return Volume.objects.get(id=self.volume_id)

    def __str__(self):
        return "{} - {} - {}".format(self.id, self.volume_id, self.server_id)
