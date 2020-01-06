import logging

from fleio.activitylog.utils.activity_helper import activity_helper
from fleio.openstack.api.identity import IdentityAdminApi
from fleio.openstack.models import OpenstackRegion
from fleio.openstack.models import Volume
from fleio.openstack.models import VolumeBackup
from fleio.openstack.sync.handler import BaseHandler
from fleio.openstack.volume_backups.serializers import VolumeBackupSyncSerializer
from fleio.openstack.volume_backups.tasks import sync_volume_backup_extra_details

LOG = logging.getLogger(__name__)


class VolumeBackupSyncHandler(BaseHandler):
    serializer_class = VolumeBackupSyncSerializer
    version_field = 'sync_version'

    def serialize(self, data, region, timestamp):
        serialized = data.to_dict()
        serialized[self.version_field] = self.get_version(timestamp)
        if 'os-backup-project-attr:project_id' in serialized:
            serialized['project_id'] = serialized.get('os-backup-project-attr:project_id')
        else:
            serialized['project_id'] = None
        volume_id = serialized.get('volume_id')
        # check if related volume still exists in fleio in order to associate the backup with it
        related_volume = None
        if volume_id:
            related_volume = Volume.objects.filter(id=volume_id).first()
        if related_volume:
            serialized['volume'] = volume_id
        else:
            serialized['volume'] = None
        serialized['region'] = OpenstackRegion.objects.filter(id=region).first()
        return serialized


class VolumeBackupHandler(BaseHandler):
    serializer_class = VolumeBackupSyncSerializer
    model_class = VolumeBackup

    def __init__(self, api_session=None):
        self.api_session = api_session or IdentityAdminApi().session
        self.event_handlers = {
            'backup.delete.start': self.create_or_update_on_deletion_start,
            'backup.create.start': self.create_or_update,
            'backup.createprogress': self.create_or_update,
            'backup.restore.start': self.create_or_update,
            'backup.restore.end': self.create_or_update,
            'backup.exists': self.create_or_update,
            'backup.delete.end': self.delete,
            'backup.create.end': self.create_or_update_end,
        }

    def create_or_update_on_deletion_start(self, data, region, timestamp):
        create_or_update = super().create_or_update(data=data, region=region, timestamp=timestamp)
        potential_fail_reason = data.get('fail_reason')
        if isinstance(potential_fail_reason, str) and potential_fail_reason.endswith('could not be found.'):
            db_volume_backup = VolumeBackup.objects.filter(id=data.get('backup_id')).first()
            if db_volume_backup:
                db_volume_backup.delete()
        return create_or_update

    def create_or_update_end(self, data, region, timestamp):
        create_or_update = super().create_or_update(data=data, region=region, timestamp=timestamp)
        if 'backup_id' in data:
            volume_backup_id = data['backup_id']
        else:
            volume_backup_id = data['id']
        # sync incremental status of backup as soon as it is created because incremental flag is not received in
        # notifications
        activity_helper.start_generic_activity(
            category_name='volume_backup', activity_class='volume backup extra details synchronization',
            backup_id=volume_backup_id
        )
        sync_volume_backup_extra_details.delay(volume_backup_id=volume_backup_id)
        activity_helper.end_activity()
        return create_or_update

    def serialize(self, data, region, timestamp):
        data[self.version_field] = self.get_version(timestamp)
        if 'os-backup-project-attr:project_id' in data:
            data['project_id'] = data.pop('os-backup-project-attr:project_id')
        elif 'tenant_id' in data:
            data['project_id'] = data['tenant_id']
        else:
            data['project_id'] = None
        volume_id = data.get('volume_id')
        # handling progress
        # TODO: maybe add a new field with progress percent?
        if 'display_name' in data:
            data['name'] = data.get('display_name')
        if 'backup_id' in data:
            data['id'] = data['backup_id']
        # check if related volume still exists in fleio in order to associate the backup with it
        related_volume = None
        if volume_id:
            related_volume = Volume.objects.filter(id=volume_id).first()
        if related_volume:
            data['volume'] = volume_id
        else:
            data['volume'] = None
        data['region'] = OpenstackRegion.objects.filter(id=region).first()
        return data

    def delete(self, payload, region=None, timestamp=None):
        volume_backup_id = payload.get('backup_id', None)
        if not volume_backup_id:
            LOG.warning('Unable to delete volume without id: {}'.format(payload))
            return
        return super().delete(obj_id=volume_backup_id, region=region, timestamp=timestamp)
