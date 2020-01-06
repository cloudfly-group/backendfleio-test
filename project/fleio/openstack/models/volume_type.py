from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from jsonfield import JSONField


@python_2_unicode_compatible
class QoSSpec(models.Model):
    qos_specs_id = models.CharField(max_length=36, primary_key=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    sync_version = models.BigIntegerField(default=0)

    name = models.CharField(max_length=255)
    consumer = models.CharField(max_length=255, blank=True, null=True)
    specs = JSONField(default=dict())

    def __str__(self):
        return self.name


class VolumeTypeQueryset(models.QuerySet):
    def public(self):
        return self.filter(is_public=True)


@python_2_unicode_compatible
class VolumeType(models.Model):
    volume_type_id = models.CharField(max_length=36, primary_key=True)
    region = models.ForeignKey('openstack.OpenstackRegion', db_constraint=False, null=True, blank=True,
                               on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    sync_version = models.BigIntegerField(default=0)

    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    is_public = models.BooleanField(default=True)
    qos_specs = models.ForeignKey(QoSSpec, db_constraint=False, null=True, blank=True, on_delete=models.DO_NOTHING)

    objects = VolumeTypeQueryset.as_manager()

    def __str__(self):
        if self.name:
            return self.name
        else:
            return self.volume_type_id


@python_2_unicode_compatible
class VolumeTypeToProject(models.Model):
    id = models.CharField(max_length=72, primary_key=True)
    sync_version = models.BigIntegerField(default=0)

    project_id = models.CharField(max_length=36)
    volume_type_id = models.CharField(max_length=36)

    class Meta:
        unique_together = ('project_id', 'volume_type_id')

    def __str__(self):
        return '{} - {}'.format(self.project_id, self.volume_type_id)


@python_2_unicode_compatible
class VolumeTypeExtraSpec(models.Model):
    id = models.CharField(max_length=72, primary_key=True)
    sync_version = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    volume_type = models.ForeignKey(VolumeType, db_constraint=False, null=True, blank=True, on_delete=models.DO_NOTHING)
    key = models.CharField(max_length=255)
    value = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        if self.volume_type_id:
            try:
                VolumeType.objects.get(volume_type_id=self.volume_type_id)
                return '{} - {}'.format(self.volume_type.volume_type_id, self.key)
            except VolumeType.DoesNotExist:
                pass
        return self.key
