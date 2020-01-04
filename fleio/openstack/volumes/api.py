import logging

from cinderclient import exceptions as cinder_exceptions

from fleio.openstack.api.cinder import cinder_client
from fleio.openstack.models import VolumeSnapshot

LOG = logging.getLogger(__name__)


def retry_if_result_is_falsy(result):
    return not result


class Volumes(object):
    def __init__(self, api_session):
        """
        :type api_session: keystoneauth1.session.Session
        """
        self.api_session = api_session

    def get(self, volume):
        """
        :type volume: fleio.openstack.models.Volume
        :rtype: Volume
        """
        return Volume(volume, api_session=self.api_session)

    def create(self, name, size, region_name, type=None, source_type=None, source_id=None):
        """
        :type region_name: str or unicode
        :param size: Size of volume in GB
        :param name: Name of the volume
        :param type: Type of volume
        :param source_type: the source type to create volume from
        :param source_id: the source id/uuid (volume or image / snapshot)
        :rtype: :class:`cinderclient.v2.volumes.Volume`
        """
        extra_params = {}
        if source_type and source_id:
            if source_type == 'image':
                extra_params['imageRef'] = source_id
            elif source_type == 'volume':
                extra_params['source_volid'] = source_id
        if type:
            extra_params['volume_type'] = type
        cc = cinder_client(api_session=self.api_session, region_name=region_name)
        return cc.volumes.create(size=size, name=name, **extra_params)


class Volume(object):
    def __init__(self, volume, api_session=None):
        """
        :type api_session: keystoneauth1.session.Session
        :type volume: fleio.openstack.models.OpenStackVolume
        """
        self.api_session = api_session
        self.volume = volume

    @property
    def cinder_api(self):
        assert self.api_session is not None, 'Unable to use cinder_api without a Keystoneauth session'

        return cinder_client(api_session=self.api_session, region_name=self.volume.region)

    @property
    def status(self):
        return self.volume.status

    @property
    def size(self):
        return self.volume.size

    def delete(self, cascade=True):
        try:
            self.cinder_api.volumes.delete(volume=self.volume.id, cascade=cascade)
        except cinder_exceptions.NotFound:
            self.volume.delete()

    def get_os_details(self):
        try:
            return self.cinder_api.volumes.get(volume_id=self.volume.id)
        except cinder_exceptions.NotFound:
            return None

    def change_bootable_status(self, new_status: bool):
        return self.cinder_api.volumes.set_bootable(volume=self.volume, flag=new_status)

    def rename(self, name):
        return self.cinder_api.volumes.update(volume=self.volume.id, name=name)

    def extend(self, size):
        return self.cinder_api.volumes.extend(volume=self.volume.id, new_size=size)

    def snapshots_delete(self, snapshot_id):
        try:
            return self.cinder_api.volume_snapshots.delete(snapshot=snapshot_id)
        except cinder_exceptions.NotFound:
            pass

    def snapshots_list(self, detailed=False):
        return self.cinder_api.volume_snapshots.list(detailed=detailed, search_opts={'volume_id': self.volume.id})

    def revert_to_snapshot(self, snapshot_id):
        snapshot = VolumeSnapshot.objects.get(id=snapshot_id)
        return self.cinder_api.volumes.revert_to_snapshot(volume=self.volume, snapshot=snapshot)
