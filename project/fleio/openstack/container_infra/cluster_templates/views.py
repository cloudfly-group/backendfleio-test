import logging

from django.db.models import Q

from fleio.activitylog.utils.decorators import log_enduser_activity
from fleio.core.drf import CustomPermissions, EndUserOnly
from fleio.openstack.common.cluster_template_base_viewset import ClusterTemplateBaseViewSet
from fleio.openstack.models import (ClusterTemplate, Image, Network, OpenstackInstanceFlavor, OpenstackRegion, Project,
                                    Subnet)
from fleio.openstack.osapi import OSApi
from fleio.openstack.settings import plugin_settings
from fleio.pkm.models import PublicKey

LOG = logging.getLogger(__name__)


@log_enduser_activity(
    category_name='openstack', object_name='cluster template'
)
class EndUserClusterTemplateViewSet(ClusterTemplateBaseViewSet):
    permission_classes = (CustomPermissions, EndUserOnly,)
    search_fields = ('name', 'id')
    filter_fields = ('project_id',)

    def get_queryset(self):
        return ClusterTemplate.objects.filter(
            Q(project__service__client__in=self.request.user.clients.all()) |
            (Q(public=True) & Q(project__project_id=plugin_settings.user_project_id))
        )

    @staticmethod
    def get_keypairs_qs(request=None):
        return PublicKey.objects.filter(user=request.user)

    def get_images_for_coe_qs(self, region=None, request=None):
        return Image.objects.get_images_for_project(
            project_id=self.get_project_id(request=request)
        ).filter(region__id=region)

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

    def get_networks_qs(self, region=None, request=None):
        return Network.objects.get_networks_for_project(
            project_id=self.get_project_id(request=request),
        ).filter(region=region)

    def get_subnets_qs(self, region=None, request=None):
        return Subnet.objects.filter(network__region=region, network__project=self.get_project_id(request=request))

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

    def get_os_api(self, request):
        project_id = self.get_project_id(request=request)
        project = Project.objects.filter(project_id=project_id).first()
        return OSApi(project=project_id, domain=project.project_domain_id)
