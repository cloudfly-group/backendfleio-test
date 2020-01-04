from cinderclient import exceptions as cinder_exceptions

from django.utils.translation import ugettext_lazy as _

from fleio.core.exceptions import APIBadRequest
from fleio.openstack.api.cinder import cinder_client
from fleio.openstack.models import VolumeSnapshot as VolumeSnapshotModel
from fleio.openstack.models import Volume as VolumeModel


class VolumeSnapshots:
    def __init__(self, api_session):
        """
        :type api_session: keystoneauth1.session.Session
        """
        self.api_session = api_session

    def get(self, volume_snapshot):
        return VolumeSnapshot(volume_snapshot, api_session=self.api_session)

    def create(self, volume_id, name, force=False, description=None, region_name=None, metadata=None):
        if not region_name:
            volume = VolumeModel.objects.filter(id=volume_id).first()
            if not volume:
                raise APIBadRequest(_('Volume to create snapshot for does not exist.'))
            region_name = volume.region
        cc = cinder_client(api_session=self.api_session, region_name=region_name)
        return cc.volume_snapshots.create(
            volume_id=volume_id,
            force=force,
            name=name,
            description=description,
            metadata=metadata,
        )


class VolumeSnapshot:
    def __init__(self, volume_snapshot: VolumeSnapshotModel, api_session=None):
        self.api_session = api_session
        self.volume_snapshot = volume_snapshot

    @property
    def cinder_api(self):
        assert self.api_session is not None, 'Unable to use cinder_api without a Keystoneauth session'
        params = {
            'api_session': self.api_session
        }
        try:
            if self.volume_snapshot.region:
                params['region_name'] = self.volume_snapshot.region.id
            else:
                snapshot_related_volume = self.volume_snapshot.volume
                if snapshot_related_volume:
                    params['region_name'] = snapshot_related_volume.region
            return cinder_client(**params)
        except VolumeModel.DoesNotExist:
            return cinder_client(**params)

    @property
    def status(self):
        return self.volume_snapshot.status

    @property
    def size(self):
        return self.volume_snapshot.size

    def update(self, name=None, description=None):
        self.cinder_api.volume_snapshots.update(
            snapshot=self.volume_snapshot.id, **{'name': name, 'description': description}
        )

    def delete(self, force=False):
        try:
            self.cinder_api.volume_snapshots.delete(snapshot=self.volume_snapshot.id, force=force)
        except cinder_exceptions.NotFound:
            self.volume_snapshot.delete()
        except cinder_exceptions.BadRequest as e:
            raise e

    def reset_state(self, state):
        self.cinder_api.volume_snapshots.reset_state(snapshot=self.volume_snapshot.id, state=state)
