from fleio.openstack.container_infra.cluster_templates.api import ClusterTemplates
from fleio.openstack.container_infra.clusters.api import Clusters
from fleio.openstack.instances.api import Instances
from fleio.openstack.volume_snapshots.api import VolumeSnapshots
from fleio.openstack.volumes.api import Volumes
from fleio.openstack.volume_backups.api import VolumeBackups
from fleio.openstack.images.api import Images

from fleio.openstack.api.identity import IdentityAdminApi


class OSAdminApi(object):

    @staticmethod
    def get_session():
        return IdentityAdminApi().session

    @property
    def volumes(self):
        return Volumes(api_session=self.get_session())

    @property
    def volume_backups(self):
        return VolumeBackups(api_session=self.get_session())

    @property
    def volume_snapshots(self):
        return VolumeSnapshots(api_session=self.get_session())

    @property
    def cluster_templates(self):
        return ClusterTemplates(api_session=self.get_session())

    @property
    def clusters(self):
        return Clusters(api_session=self.get_session())

    @property
    def images(self):
        return Images(api_session=self.get_session())

    @property
    def instances(self):
        return Instances(api_session=self.get_session())
