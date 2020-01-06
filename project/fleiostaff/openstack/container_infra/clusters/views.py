import logging

from django.utils.translation import ugettext_lazy as _

from rest_framework.decorators import action

from fleio.activitylog.utils.decorators import log_staff_activity
from fleio.core.drf import CustomPermissions, StaffOnly
from fleio.core.exceptions import APIBadRequest
from fleio.openstack.common.cluster_base_viewset import ClusterBaseViewSet
from fleio.openstack.models import Cluster, OpenstackInstanceFlavor, OpenstackRegion
from fleio.openstack.settings import plugin_settings
from fleio.pkm.models import PublicKey
from fleiostaff.openstack.osadminapi import OSAdminApi

LOG = logging.getLogger(__name__)


@log_staff_activity(
    category_name='openstack', object_name='cluster'
)
class StaffClusterViewSet(ClusterBaseViewSet):
    permission_classes = (CustomPermissions, StaffOnly,)
    search_fields = ('name', 'status', 'id')
    filter_fields = ('cluster_template',)

    def get_queryset(self):
        return Cluster.objects.all()

    @staticmethod
    def get_keypairs_qs(request=None):
        return PublicKey.objects.all()

    def get_flavors_qs(self, region=None, request=None):
        return OpenstackInstanceFlavor.objects.filter(region__id=region)

    @staticmethod
    def get_regions_qs():
        return OpenstackRegion.objects.enabled()

    @staticmethod
    def get_os_api(request):
        del request  # unused
        return OSAdminApi()

    @staticmethod
    def get_project_id(request=None):
        return plugin_settings.user_project_id

    @action(detail=True, methods=['post'])
    def resize_cluster(self, request, pk):
        cluster = self.get_object()
        if cluster.project.project_id != self.get_project_id():
            raise APIBadRequest(_('If you want to resize cluster, impersonate the owner.'))
        return super().resize_cluster(request=request, pk=pk)

    @action(detail=True, methods=['get'])
    def get_certificate(self, request, pk):
        cluster = self.get_object()
        if cluster.project.project_id != self.get_project_id():
            raise APIBadRequest(_('If you want to get certificate for cluster, impersonate the owner.'))
        return super().get_certificate(request=request, pk=pk)
