from django.db import models
from django.utils.translation import ugettext_lazy as _

from fleio.openstack.models import OpenstackRegion, Project, Volume


class VolumeSnapshot(models.Model):
    id = models.CharField(max_length=36, unique=True, primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=32, blank=True)
    progress = models.IntegerField(null=True)
    description = models.CharField(max_length=1024, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    volume = models.ForeignKey(
        Volume, null=True, blank=True, db_index=True, db_constraint=False, on_delete=models.SET_NULL
    )
    project = models.ForeignKey(
        Project, db_constraint=False, null=True, blank=True, on_delete=models.SET_NULL,
        to_field='project_id'
    )
    size = models.IntegerField()
    metadata = models.CharField(max_length=1024, null=True, blank=True)
    sync_version = models.BigIntegerField(default=0)
    region = models.ForeignKey(OpenstackRegion, on_delete=models.SET_NULL, null=True, blank=False, default=None)

    objects = models.Manager


class VolumeSnapshotStatus:
    CREATING = 'creating'
    AVAILABLE = 'available'
    BACKING_UP = 'backing-up'
    DELETED = 'deleted'
    DELETING = 'deleting'
    ERROR = 'error'
    RESTORING = 'restoring'
    ERROR_DELETING = 'error_deleting'
    UNMANAGING = 'unmanaging'

    status_map = {
        CREATING: _('Creating'),
        AVAILABLE: _('Available'),
        BACKING_UP: _('Backing up'),
        DELETED: _('Deleted'),
        DELETING: _('Deleting'),
        ERROR: _('Error'),
        RESTORING: _('Restoring'),
        ERROR_DELETING: _('Error deleting'),
        UNMANAGING: _('Unmanaging'),
    }
