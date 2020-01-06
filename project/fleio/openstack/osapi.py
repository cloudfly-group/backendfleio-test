import logging

from django.utils.translation import ugettext_lazy as _

from fleio.core.exceptions import APIBadRequest
from fleio.openstack.container_infra.cluster_templates.api import ClusterTemplates
from fleio.openstack.container_infra.clusters.api import Clusters
from fleio.openstack.images.api import Images
from fleio.openstack.instances.api import Instances
from fleio.openstack.networking.api import FloatingIps, Networks, Ports, Routers, SecurityGroups, SubnetPools, Subnets
from fleio.openstack.volume_snapshots.api import VolumeSnapshots
from fleio.openstack.volumes.api import Volumes
from fleio.openstack.volume_backups.api import VolumeBackups

from .api import session
from .flavor import Flavors
from .settings import plugin_settings
from .utils import OSAuthCache
from .models import Project

LOG = logging.getLogger(__name__)


class OSApi(object):
    def __init__(self, project, domain, auth_cache=None):
        self.project = project
        self.domain = domain
        self.auth_cache = auth_cache

    @classmethod
    def from_project_id(cls, project_id, auth_cache=None):
        """
        :param project_id: is fleio.openstack.Project.project_id
        :param auth_cache: OSAuthCache class
        """
        project = Project.objects.get(project_id=project_id)
        return cls(project=project.project_id, domain=project.project_domain_id, auth_cache=auth_cache)

    @classmethod
    def from_request(cls, request):
        client = request.user.clients.first()
        try:
            project = client.first_project.project_id
        except (AttributeError, TypeError):
            LOG.error('Unable to retrieve project_id for user {}'.format(request.user))
            raise APIBadRequest(detail=_('No client with an OpenStack project found'))
        domain = client.first_project.project_domain_id
        auth_cache = OSAuthCache(request_session=request.session)
        return cls(project=project, domain=domain, auth_cache=auth_cache)

    @classmethod
    def with_admin(cls, auth_cache=None):
        return cls(project=plugin_settings.USER_PROJECT_ID,
                   domain=plugin_settings.PROJECT_DOMAIN_ID,
                   auth_cache=auth_cache)

    def get_session(self):
        return session.get_session(auth_url=plugin_settings.AUTH_URL,
                                   project_id=self.project,
                                   project_domain_id=self.domain,
                                   admin_username=plugin_settings.USERNAME,
                                   admin_password=plugin_settings.PASSWORD,
                                   admin_domain_id=plugin_settings.USER_DOMAIN_ID,
                                   cache=self.auth_cache,
                                   timeout=plugin_settings.TIMEOUT)

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

    @property
    def flavors(self):
        return Flavors(api_session=self.get_session())

    @property
    def floating_ips(self):
        return FloatingIps(api_session=self.get_session())

    @property
    def networks(self):
        return Networks(api_session=self.get_session())

    @property
    def subnets(self):
        return Subnets(api_session=self.get_session())

    @property
    def subnet_pools(self):
        return SubnetPools(api_session=self.get_session())

    @property
    def ports(self):
        return Ports(api_session=self.get_session())

    @property
    def routers(self):
        return Routers(api_session=self.get_session())

    @property
    def security_groups(self):
        return SecurityGroups(api_session=self.get_session())
