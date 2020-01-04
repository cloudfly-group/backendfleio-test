import logging

from django.conf import settings
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from fleio.activitylog.utils.decorators import log_staff_activity
from fleio.core.permissions.permissions_cache import permissions_cache
from fleio.core.drf import CustomPermissions, StaffOnly
from fleio.core.validation_utils import validate_cloud_objects_limit
from fleio.openstack.api.identity import IdentityAdminApi
from fleio.openstack.exceptions import APIBadRequest, handle
from fleio.openstack.models import Network, Port, Router, Subnet
from fleio.openstack.networking.api import Routers
from fleio.openstack.views.regions import get_regions
from .serializers import StaffRouterCreateSerializer, StaffRouterDetailSerializer, StaffRouterSerializer, \
    StaffRouterUpdateSerializer, SubnetInterfaceSerializer
from fleio.core.filters import CustomFilter

LOG = logging.getLogger(__name__)


@log_staff_activity(
    category_name='openstack', object_name='router',
)
class StaffRouterViewSet(viewsets.ModelViewSet):
    serializer_class = StaffRouterSerializer
    serializer_map = {'create': StaffRouterCreateSerializer,
                      'update': StaffRouterUpdateSerializer,
                      'retrieve': StaffRouterDetailSerializer}
    permission_classes = (CustomPermissions, StaffOnly,)
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend, CustomFilter, filters.SearchFilter)
    ordering_fields = ('name', 'admin_state_up', 'region__id')
    search_fields = ('name', 'region__id')
    ordering = ['id']

    @property
    def identity_admin_api(self):
        if hasattr(self, 'request'):
            return IdentityAdminApi(request_session=self.request.session)
        else:
            return IdentityAdminApi()

    def get_queryset(self):
        return Router.objects.all()

    def list(self, request, *args, **kwargs):
        response = super().list(request=request, *args, **kwargs)
        response.data['permissions'] = permissions_cache.get_view_permissions(request.user, self.basename)
        return response

    def get_serializer_class(self):
        return self.serializer_map.get(self.action, self.serializer_class)

    def perform_create(self, serializer):
        if not validate_cloud_objects_limit():
            raise APIBadRequest(_('Licence cloud objects limit reached. Please check your license.'))
        serializer.is_valid(raise_exception=True)
        router_admin_api = Routers(api_session=self.identity_admin_api.session)
        try:
            router_admin_api.create(kwargs=serializer.validated_data)
        except Exception as e:
            LOG.error(e)
            handle(self.request, message=_('Unable to create router'))

    def perform_update(self, serializer):
        serializer.is_valid(raise_exception=True)
        router_admin_api = Routers(api_session=self.identity_admin_api.session)
        try:
            router_admin_api.update(id=serializer.instance.id, region=serializer.instance.region,
                                    kwargs=serializer.validated_data)
        except Exception as e:
            LOG.error(e)
            handle(self.request, message=_('Unable to update router'))

    def perform_destroy(self, db_router):
        """Delete router from neutron and from db."""
        router_admin_api = Routers(api_session=self.identity_admin_api.session)
        router = router_admin_api.get(router=db_router)
        try:
            router.delete(region=db_router.region_id)
        except Exception as e:
            LOG.error(e)
            handle(self.request, message=e)

    @action(detail=False, methods=['get'])
    def create_options(self, request):
        selected_region, regions = get_regions(request)
        external_networks = [{'name': net.name, 'id': net.id, 'region': net.region} for net in
                             Network.objects.filter(router_external=True)]
        return Response(
            {'regions': regions, 'external_networks': external_networks, 'selected_region': selected_region})

    @action(detail=True, methods=['get'])
    def create_add_interface_options(self, request, pk):
        """Get subnets which are from internal networks and not added to this router and in the router's region"""
        router = self.get_object()
        router_interfaces = Port.objects.filter(
            device_id=pk,
            device_owner=getattr(settings, 'ROUTER_PORT_DEVICE_OWNER', 'network:router_interface'),
        )
        subnet_id_list = list()
        for interface in router_interfaces:
            if interface.fixed_ips:
                for fixed_ip in interface.fixed_ips:
                    subnet_id_list.append(fixed_ip['subnet_id'])
        subnets = Subnet.objects.exclude(Q(id__in=subnet_id_list) | Q(network__router_external=True) |
                                         ~Q(network__region=router.region_id))

        if not subnets:
            raise NotFound(_('No subnets available'))
        return Response({'subnets': SubnetInterfaceSerializer(instance=subnets, many=True).data})

    @action(detail=True, methods=['post'])
    def add_interface(self, request, pk):
        """Add an interface to a router"""
        db_router = self.get_object()
        router_admin_api = Routers(api_session=self.identity_admin_api.session)
        router = router_admin_api.get(router=db_router)
        if 'subnet' not in request.data:
            raise APIBadRequest(_('Parameter subnet is missing'))

        try:
            router.add_interface(region=db_router.region.id, subnet=request.data['subnet'],
                                 ip=request.data.get('ip', None))
        except Exception as e:
            LOG.error(e)
            handle(self.request, message=_('Unable to add interface'))
        return Response({'detail': _('Adding interface in progress')})

    @action(detail=True, methods=['post'])
    def remove_interface(self, request, pk):
        """Remove an interface from a router"""
        db_router = self.get_object()
        router_admin_api = Routers(api_session=self.identity_admin_api.session)
        router = router_admin_api.get(router=db_router)
        if 'interface_id' not in request.data:
            raise APIBadRequest(_('Parameter interface_id is missing'))

        try:
            router.remove_interface(region=db_router.region.id, interface_id=request.data['interface_id'])
        except Exception as e:
            LOG.error(e)
            handle(self.request, message=_('Unable to remove interface'))
        return Response({'detail': _('Removing interface in progress')})

    @action(detail=False, methods=['get'])
    def permissions(self, request):
        view_permissions = permissions_cache.get_view_permissions(request.user, self.basename)
        return Response(data=view_permissions)
