from __future__ import unicode_literals

import logging

from django.conf import settings
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from neutronclient.common.exceptions import BadRequest, NotFound
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from fleio.activitylog.utils.decorators import log_staff_activity
from fleio.core.permissions.permissions_cache import permissions_cache
from fleio.core.drf import CustomPermissions, StaffOnly
from fleio.core.exceptions import APIBadRequest

from fleio.openstack.api.identity import IdentityAdminApi
from fleio.openstack.exceptions import handle, ObjectNotFound
from fleio.openstack.models import Network, SubnetPool
from fleio.openstack.networking.api import Networks, SubnetPools
from fleio.openstack.networking.serializers import SubnetPoolSerializer
from fleio.openstack.networking.views import NetworkViewSet
from fleio.openstack.osapi import OSApi
from fleio.openstack.serializers.regions import RegionSerializer
from fleio.openstack.views.regions import get_regions
from fleiostaff.openstack.networks import constants
from fleiostaff.openstack.signals import staff_delete_network
from .serializers import StaffNetworkAutoCreateSerializer, StaffNetworkCreateSerializer, StaffNetworkSerializerExtra, \
    StaffNetworkUpdateSerializer
from fleio.core.filters import CustomFilter

LOG = logging.getLogger(__name__)


@log_staff_activity(
    category_name='openstack', object_name='network',
)
class StaffNetworkViewSet(NetworkViewSet):
    serializer_class = StaffNetworkSerializerExtra
    serializer_map = {'create': StaffNetworkCreateSerializer,
                      'update': StaffNetworkUpdateSerializer,
                      'auto_create_network': StaffNetworkAutoCreateSerializer}
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend, CustomFilter, filters.SearchFilter)
    permission_classes = (CustomPermissions, StaffOnly,)

    @property
    def identity_admin_api(self):
        if hasattr(self, 'request'):
            return IdentityAdminApi(request_session=self.request.session)
        else:
            return IdentityAdminApi()

    def get_queryset(self):
        return Network.objects.all()

    def list(self, request, *args, **kwargs):
        response = super().list(request=request, *args, **kwargs)
        response.data['permissions'] = permissions_cache.get_view_permissions(request.user, self.basename)
        return response

    def perform_create(self, serializer):
        network_admin_api = Networks(api_session=self.identity_admin_api.session)
        try:
            network = network_admin_api.create(kwargs=serializer.validated_data)
            network = network['network']
            serializer.validated_data['id'] = network['id']
        except Exception as e:
            LOG.error(e)
            handle(self.request, message=_('Unable to create network'))

    def perform_destroy(self, db_network):
        """Delete network from neutron and from db."""
        network = self.get_network()
        region = db_network.region
        try:
            network.delete(region=region)
            user = self.request.user
            staff_delete_network.send(sender=__name__, user=user, user_id=user.id,
                                      network_name=db_network.name, network_id=db_network.id,
                                      username=user.username, request=self.request)
        except NotFound:
            raise ObjectNotFound(_('Object in fleio but not in openstack'))
        except Exception as e:
            LOG.error(e)
            handle(self.request, message=force_text(e))

    def perform_update(self, serializer):
        serializer.is_valid(raise_exception=True)
        network_admin_api = Networks(api_session=self.identity_admin_api.session)
        try:
            network_admin_api.update(old_values=serializer.instance, new_values=serializer.validated_data)
        except BadRequest as e:
            raise APIBadRequest(e)
        except Exception as e:
            LOG.error(e)
            handle(self.request, message=_('Unable to update network'))

    def get_network(self):
        network = self.get_object()
        network_admin_api = Networks(api_session=self.identity_admin_api.session)
        return network_admin_api.get(network=network)

    @action(detail=False, methods=['POST'])
    def auto_create_network(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project_id = serializer.validated_data['project'].project_id

        os_api = OSApi.from_project_id(project_id=project_id)
        net_id = None
        try:
            net_id = os_api.networks.auto_create_network(project_id=project_id,
                                                         region=serializer.validated_data['region'])
        except Exception as e:
            LOG.error(e)
            handle(self.request, message=_('Unable to auto create network'))
        return Response({'id': net_id})

    @action(detail=False, methods=['GET'])
    def config_auto_create_network_options(self, request):
        if 'region' not in request.query_params:
            raise APIBadRequest(_('Must be called with region parameter'))

        network_admin_api = Networks(api_session=self.identity_admin_api.session)
        options = network_admin_api.config_auto_create_network_options(region=request.query_params['region'])
        options['config'] = network_admin_api.get_current_auto_create_config(region=request.query_params['region'])

        return Response({'options': options})

    @action(detail=False, methods=['POST'])
    def save_auto_create_network_options(self, request):
        if 'region' not in request.data:
            raise APIBadRequest(_('Must be called with region parameter'))

        network_admin_api = Networks(api_session=self.identity_admin_api.session)
        subnetpool_admin_api = SubnetPools(api_session=self.identity_admin_api.session)
        options = network_admin_api.config_auto_create_network_options(region=request.data['region'])
        options['config'] = dict()

        if 'network_id' in request.data:
            network = network_admin_api.set_network_as_default(request.data['region'], request.data['network_id'])
            if network:
                options['config']['network'] = network

        if 'ipv4_subnetpool' in request.data:
            ipv4_subnetpool = subnetpool_admin_api.set_subnetpool_as_default(request.data['region'],
                                                                             request.data['ipv4_subnetpool'],
                                                                             ip_version=4)
            if ipv4_subnetpool:
                options['config']['ipv4_subnetpool'] = ipv4_subnetpool

        if 'ipv6_subnetpool' in request.data:
            ipv6_subnetpool = subnetpool_admin_api.set_subnetpool_as_default(request.data['region'],
                                                                             request.data['ipv6_subnetpool'],
                                                                             ip_version=6)
            if ipv6_subnetpool:
                options['config']['ipv6_subnetpool'] = ipv6_subnetpool

        return Response({'options': options})

    @action(detail=False, methods=['get'])
    def create_options(self, request):
        provider_types = dict()
        for provider_type in settings.OPENSTACK_NETWORK_PROVIDER_TYPES:
            try:
                provider_types[provider_type] = constants.PROVIDER_TYPES[provider_type]
            except KeyError:
                LOG.error('Undefined network provider type found: {}'.format(provider_type))
        selected_region, regions = get_regions(request)
        return Response(
            {'regions': RegionSerializer(instance=regions, many=True).data, 'provider_types': provider_types,
             'segmentation_id_range': constants.SEGMENTATION_ID_RANGE, 'selected_region': selected_region})

    @action(detail=False, methods=['get'])
    def get_subnet_pools(self, request):
        region = request.query_params.get('region', None)
        if not region:
            raise APIBadRequest(_('Region required in request'))
        pools = SubnetPool.objects.filter(region=region)
        return Response({'pools': SubnetPoolSerializer(instance=pools, many=True).data})

    @action(detail=False, methods=['get'])
    def permissions(self, request):
        view_permissions = permissions_cache.get_view_permissions(request.user, self.basename)
        return Response(data=view_permissions)
