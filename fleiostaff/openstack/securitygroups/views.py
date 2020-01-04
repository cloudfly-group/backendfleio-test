from rest_framework.decorators import action
from rest_framework.response import Response

from fleio.activitylog.utils.decorators import log_staff_activity
from fleio.core.drf import CustomPermissions, StaffOnly
from fleio.core.permissions.permissions_cache import permissions_cache
from fleio.openstack.views.regions import get_regions
from fleio.openstack.models import SecurityGroup
from fleio.openstack.networking.serializers import SecurityGroupRuleCreateSerializer
from fleio.openstack.networking.serializers import SecurityGroupUpdateSerializer
from fleio.openstack.networking.views import SecurityGroupViewSet
from fleio.openstack.osapi import OSApi
from fleiostaff.openstack.securitygroups.serializers import StaffSecurityGroupSerializer
from fleiostaff.openstack.securitygroups.serializers import StaffSecurityGroupCreateSerializer
from fleiostaff.openstack.securitygroups.serializers import StaffSecurityGroupDetailSerializer


@log_staff_activity(
    category_name='openstack', object_name='security group',
)
class StaffSecurityGroupViewSet(SecurityGroupViewSet):
    serializer_class = StaffSecurityGroupSerializer
    serializer_map = {'create': StaffSecurityGroupCreateSerializer,
                      'retrieve': StaffSecurityGroupDetailSerializer,
                      'update': SecurityGroupUpdateSerializer,
                      'add_rule': SecurityGroupRuleCreateSerializer}
    search_fields = ('name', 'project__project_id', 'region__id')
    permission_classes = (CustomPermissions, StaffOnly,)

    def get_queryset(self):
        return SecurityGroup.objects.all()

    def list(self, request, *args, **kwargs):
        response = super().list(request=request, *args, **kwargs)
        response.data['permissions'] = permissions_cache.get_view_permissions(request.user, self.basename)
        return response

    def get_os_api(self):
        return OSApi.with_admin()

    @action(detail=False, methods=['get'])
    def create_options(self, request, *args, **kwargs):
        selected_region, regions = get_regions(request)
        return Response({
            'regions': regions,
            'selected_region': selected_region,
        })

    @action(detail=False, methods=['GET'])
    def get_security_groups_for_project(self, request):
        if not request.query_params.get('project_id', None):
            return Response({'security_groups': []})
        sec_groups = SecurityGroup.objects.filter(project_id=request.query_params['project_id'])
        return Response({'security_groups': [{'id': s.id, 'name': s.name} for s in sec_groups]})

    @action(detail=False, methods=['get'])
    def permissions(self, request):
        view_permissions = permissions_cache.get_view_permissions(request.user, self.basename)
        return Response(data=view_permissions)
