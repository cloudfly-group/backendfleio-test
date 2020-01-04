import logging

from fleio.activitylog.utils.decorators import log_enduser_activity
from fleio.core.drf import CustomPermissions, StaffOnly
from fleio.openstack.common.cluster_template_base_viewset import ClusterTemplateBaseViewSet
from fleio.openstack.models import ClusterTemplate, Image, Network, OpenstackInstanceFlavor, OpenstackRegion, Subnet
from fleio.openstack.settings import plugin_settings
from fleio.pkm.models import PublicKey
from fleiostaff.openstack.osadminapi import OSAdminApi

LOG = logging.getLogger(__name__)


@log_enduser_activity(
    category_name='openstack', object_name='cluster template'
)
class StaffClusterTemplateViewSet(ClusterTemplateBaseViewSet):

    permission_classes = (CustomPermissions, StaffOnly,)
    search_fields = ('name', 'id')
    filter_fields = ('project_id', 'project', )

    def get_queryset(self):
        return ClusterTemplate.objects.all()

    @staticmethod
    def get_keypairs_qs(request=None):
        return PublicKey.objects.all()

    @staticmethod
    def get_project_id(request=None):
        return plugin_settings.user_project_id

    def get_images_for_coe_qs(self, region=None, request=None):
        return Image.objects.filter(region__id=region)

    def get_flavors_qs(self, region=None, request=None):
        return OpenstackInstanceFlavor.objects.filter(region__id=region)

    @staticmethod
    def get_regions_qs():
        return OpenstackRegion.objects.enabled()

    def get_networks_qs(self, region=None, request=None):
        return Network.objects.filter(region=region)

    def get_subnets_qs(self, region=None, request=None):
        return Subnet.objects.filter(network__region=region)

    def get_os_api(self, request):
        del request  # unused
        return OSAdminApi()
