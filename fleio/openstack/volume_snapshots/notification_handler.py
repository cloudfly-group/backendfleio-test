import json
import logging

from fleio.openstack.api.identity import IdentityAdminApi
from fleio.openstack.sync.handler import BaseHandler
from fleio.openstack.models import OpenstackRegion, Volume, VolumeSnapshot
from fleio.openstack.volume_snapshots.serializers import VolumeSnapshotSyncSerializer


LOG = logging.getLogger(__name__)


class VolumeSnapshotSyncHandler(BaseHandler):
    serializer_class = VolumeSnapshotSyncSerializer
    version_field = 'sync_version'

    def serialize(self, data, region, timestamp):
        serialized = data.to_dict()
        serialized[self.version_field] = self.get_version(timestamp)
        if 'os-extended-snapshot-attributes:project_id' in serialized:
            serialized['project_id'] = serialized.get('os-extended-snapshot-attributes:project_id')
        else:
            serialized['project_id'] = None
        volume_id = serialized.get('volume_id')
        # check if related volume still exists in fleio in order to associate the snapshot with it
        related_volume = None
        if volume_id:
            related_volume = Volume.objects.filter(id=volume_id).first()
        if related_volume:
            serialized['volume'] = volume_id
        else:
            serialized['volume'] = None
        serialized['region'] = OpenstackRegion.objects.filter(id=region).first()
        serialized['metadata'] = json.dumps(serialized.get('metadata', {}))
        return serialized


class VolumeSnapshotHandler(BaseHandler):
    serializer_class = VolumeSnapshotSyncSerializer
    model_class = VolumeSnapshot

    def __init__(self, api_session=None):
        self.api_session = api_session or IdentityAdminApi().session
        # TODO: these need to be checked and updated
        self.event_handlers = {
            'snapshot.delete.start': self.create_or_update,
            'snapshot.create.start': self.create_or_update,
            'snapshot.createprogress': self.create_or_update,
            'snapshot.exists': self.create_or_update,
            'snapshot.update.start': self.create_or_update,
            'snapshot.update.end': self.create_or_update,
            'snapshot.revert.start': self.create_or_update,
            'snapshot.revert.end': self.create_or_update,
            'snapshot.delete.end': self.delete,
            'snapshot.create.end': self.create_or_update,
            'snapshots.reset_status.start': self.reset_status,
            'snapshots.reset_status.end': self.reset_status,
        }

    @staticmethod
    def reset_status(data, region, timestamp):
        del region, timestamp  # unused
        vs = VolumeSnapshot.objects.filter(id=data['id']).first()
        if vs:
            if 'update' in data:
                if 'status' in data['update']:
                    vs.status = data['update']['status']
                    vs.save()

    def serialize(self, data, region, timestamp):
        data[self.version_field] = self.get_version(timestamp)
        if 'os-extended-snapshot-attributes:project_id' in data:
            data['project_id'] = data.pop('os-extended-snapshot-attributes:project_id')
        elif 'tenant_id' in data:
            data['project_id'] = data['tenant_id']
        else:
            data['project_id'] = None
        if 'display_name' in data:
            data['name'] = data.get('display_name')
        volume_id = data.get('volume_id')
        data['size'] = data.get('volume_size')
        if 'snapshot_id' in data:
            data['id'] = data['snapshot_id']
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
        volume_snapshot_id = payload.get('snapshot_id', None)
        if not volume_snapshot_id:
            LOG.warning('Unable to delete volume snapshot without id: {}'.format(payload))
            return
        return super().delete(obj_id=volume_snapshot_id, region=region, timestamp=timestamp)
