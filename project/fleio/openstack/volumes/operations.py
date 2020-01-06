import json

from fleio.core.operations_base.operation_base import OperationBase
from django.utils.timezone import now as utcnow
from fleio.openstack.models.volume import Volume, VolumeBackup
from fleio.openstack.volume_backups.notification_handler import VolumeBackupSyncHandler
from fleio.openstack.volumes.notification_handler import VolumeSyncHandler
from fleio.openstack.volumes.volume_status import VolumeBackupStatus, VolumeStatus
from fleiostaff.openstack.osadminapi import OSAdminApi


class VolumeRestoration(OperationBase):
    name = 'volume_restoration'

    def run(self, *args, **kwargs):
        backup_id = kwargs.get('backup_id')
        volume_id = kwargs.get('volume_id')
        if not backup_id or not volume_id:
            return self.abort_operation()
        os_api = OSAdminApi()
        if not kwargs.get('volume_was_synced', False):
            # sync the volume when ready
            db_volume = Volume.objects.filter(id=volume_id).first()
            if db_volume:
                os_volume = os_api.volumes.get(volume=db_volume)
                os_volume_details = os_volume.get_os_details()
                if not os_volume_details:
                    return self.abort_operation()
                db_volume.status = os_volume_details.status
                db_volume.save()  # ensure it is up to date
                if (os_volume_details.status != VolumeStatus.CREATING and
                        os_volume_details.status != VolumeStatus.RESTORING_BACKUP):
                    # volume is not creating anymore, we can sync it
                    timestamp = utcnow().isoformat()
                    vh = VolumeSyncHandler()
                    vh.create_or_update(volume=os_volume_details, region=db_volume.region, timestamp=timestamp)
                    operation_params = {
                        'backup_id': backup_id,
                        'volume_id': volume_id,
                        'volume_was_synced': True,
                        'volume_backup_was_synced': kwargs.get('volume_backup_was_synced', False),
                    }
                    self.db_operation.params = json.dumps(operation_params)
                    self.db_operation.save()
        if not kwargs.get('volume_backup_was_synced', False):
            # sync the volume backup when ready
            db_volume_backup = VolumeBackup.objects.filter(id=backup_id).first()
            if not db_volume_backup:
                return self.abort_operation()
            os_volume_backup = os_api.volume_backups.get(volume_backup=db_volume_backup)
            os_volume_backup_details = os_volume_backup.get_details_from_os()
            if not os_volume_backup_details:
                return self.abort_operation()
            db_volume_backup.status = os_volume_backup_details.status
            db_volume_backup.save()  # ensure it is up to date
            if os_volume_backup_details.status != VolumeBackupStatus.RESTORING:
                # volume backup is not restoring anymore, we can sync it
                timestamp = utcnow().isoformat()
                vbh = VolumeBackupSyncHandler()
                vbh.create_or_update(data=os_volume_backup_details, region=db_volume_backup.region, timestamp=timestamp)
                operation_params = {
                    'backup_id': backup_id,
                    'volume_id': volume_id,
                    'volume_backup_was_synced': True,
                    'volume_was_synced': kwargs.get('volume_was_synced', False),
                }
                self.db_operation.params = json.dumps(operation_params)
                self.db_operation.save()
        if kwargs.get('volume_backup_was_synced', False) and kwargs.get('volume_was_synced', False):
            return self.abort_operation()
