import logging

from django.utils.translation import ugettext_lazy as _

from fleio.openstack.api.cinder import cinder_client
from fleio.openstack.models import Volume as VolumeModel
from fleio.openstack.models import VolumeBackup as VolumeBackupModel
from fleio.openstack.settings import plugin_settings

from cinderclient.api_versions import APIVersion
from cinderclient import exceptions as cinder_exceptions

from fleio.core.exceptions import APIBadRequest

LOG = logging.getLogger(__name__)


class VolumeBackups:
    def __init__(self, api_session):
        """
        :type api_session: keystoneauth1.session.Session
        """
        self.api_session = api_session

    def get(self, volume_backup):
        return VolumeBackup(volume_backup, api_session=self.api_session)

    def create(self, volume_id, region_id, container=None, name=None, description=None, incremental=False,
               force=False):
        cc = cinder_client(api_session=self.api_session, region_name=region_id)
        return cc.backups.create(
            volume_id=volume_id,
            container=container,
            name=name,
            description=description,
            incremental=incremental,
            force=force,
        )


class VolumeBackup:
    def __init__(self, volume_backup: VolumeBackupModel, api_session=None):
        self.api_session = api_session
        self.volume_backup = volume_backup

    @property
    def cinder_api(self):
        assert self.api_session is not None, 'Unable to use cinder_api without a Keystoneauth session'
        params = {
            'api_session': self.api_session
        }
        try:
            if self.volume_backup.region:
                params['region_name'] = self.volume_backup.region.id
            else:
                backup_related_volume = self.volume_backup.volume
                if backup_related_volume:
                    params['region_name'] = backup_related_volume.region
            return cinder_client(**params)
        except VolumeModel.DoesNotExist:
            return cinder_client(**params)

    @property
    def status(self):
        return self.volume_backup.status

    @property
    def size(self):
        return self.volume_backup.size

    def get_details_from_os(self):
        try:
            return self.cinder_api.backups.get(backup_id=self.volume_backup.id)
        except cinder_exceptions.NotFound:
            return None

    def delete(self, force=False):
        try:
            self.cinder_api.backups.delete(backup=self.volume_backup.id, force=force)
        except cinder_exceptions.NotFound:
            self.volume_backup.delete()
        except cinder_exceptions.BadRequest as e:
            raise e

    def restore(self, name=None, volume_id=None):
        return self.cinder_api.restores.restore(
            backup_id=self.volume_backup.id,
            volume_id=volume_id,
            name=name,
        )

    def update(self, name=None, description=None):
        if APIVersion(plugin_settings.VOLUME_API_VERSION) < APIVersion('3.9'):
            raise APIBadRequest(_('Volume update is not found in this volume api version'))
        return self.cinder_api.backups.update(
            backup=self.volume_backup,
            description=description,
            name=name
        )
