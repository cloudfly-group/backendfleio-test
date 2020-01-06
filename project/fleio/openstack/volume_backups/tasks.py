import logging

from django.conf import settings
from fleio.celery import app
from fleio.openstack.models import VolumeBackup
from fleiostaff.openstack.osadminapi import OSAdminApi

LOG = logging.getLogger(__name__)


@app.task(
    bind=True,
    max_retries=settings.TASK_RETRIES,
    name='Volume backup extra details synchronization',
    resource_type='VolumeBackup',
)
def sync_volume_backup_extra_details(self, volume_backup_id, after_update=False):
    del self  # unused
    os_api = OSAdminApi()
    volume_backup = VolumeBackup.objects.filter(id=volume_backup_id).first()
    if volume_backup:
        os_volume_backup_details = os_api.volume_backups.get(volume_backup).get_details_from_os()
        if os_volume_backup_details:
            volume_backup.is_incremental = os_volume_backup_details.is_incremental
            volume_backup.name = os_volume_backup_details.name
            volume_backup.object_count = os_volume_backup_details.object_count
            volume_backup.description = os_volume_backup_details.description
            volume_backup.save()
            if volume_backup.is_incremental is True and after_update is False:
                related_full_backup = VolumeBackup.objects.filter(volume=volume_backup.volume,
                                                                  is_incremental=False).first()
                if related_full_backup:
                    os_related_full_backup_details = os_api.volume_backups.get(
                        related_full_backup).get_details_from_os()
                    if os_related_full_backup_details:
                        related_full_backup.has_dependent_backups = os_related_full_backup_details.has_dependent_backups
                        related_full_backup.object_count = os_related_full_backup_details.object_count
                        related_full_backup.save()
                    else:
                        related_full_backup.delete()
        else:
            volume_backup.delete()
