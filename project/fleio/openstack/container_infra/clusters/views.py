import logging

from fleio.activitylog.utils.decorators import log_enduser_activity
from fleio.core.drf import CustomPermissions, EndUserOnly
from fleio.openstack.common.cluster_base_viewset import ClusterBaseViewSet
from fleio.openstack.models import Cluster, OpenstackInstanceFlavor, OpenstackRegion, Project
from fleio.openstack.osapi import OSApi
from fleio.pkm.models import PublicKey

LOG = logging.getLogger(__name__)


@log_enduser_activity(
    category_name='openstack', object_name='cluster'
)
class EndUserClusterViewSet(ClusterBaseViewSet):
    permission_classes = (CustomPermissions, EndUserOnly,)
    search_fields = ('name', 'status', 'id')
    filter_fields = ('cluster_template',)

    @staticmethod
    def get_keypairs_qs(request=None):
        user = request.user
        return PublicKey.objects.filter(user=user)

    def get_flavors_qs(self, region=None, request=None):
        return OpenstackInstanceFlavor.objects.get_for_project(
            project_id=self.get_project_id(request=request),
            disabled=False,
            region=region,
            deleted=False,
            is_public=True,
            show_in_fleio=True
        )

    @staticmethod
    def get_regions_qs():
        return OpenstackRegion.objects.enabled_for_enduser()

    def get_os_api(self, request):
        project_id = self.get_project_id(request=request)
        project = Project.objects.filter(project_id=project_id).first()
        return OSApi(project=project_id, domain=project.project_domain_id)

    @staticmethod
    def get_project_id(request=None):
        user = request.user
        user_clients = user.clients.filter(services__openstack_project__isnull=False)
        client = user_clients.first()
        if client:
            project = client.first_project
            if not project:
                return None
            return project.project_id
        return None

    def get_queryset(self):
        return Cluster.objects.filter(project__service__client__in=self.request.user.clients.all())
