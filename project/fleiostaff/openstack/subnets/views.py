from __future__ import unicode_literals

import logging

from django.utils.translation import ugettext_lazy as _
from neutronclient.common.exceptions import BadRequest
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from fleio.core.drf import StaffOnly
from fleio.core.exceptions import APIBadRequest

from fleio.openstack.api.identity import IdentityAdminApi
from fleio.openstack.exceptions import handle
from fleio.openstack.models import Network, Subnet, SubnetPool
from fleio.openstack.networking.api import Subnets
from fleio.openstack.networking.serializers import SubnetPoolSerializer
from .serializers import StaffSubnetCreateSerializer, StaffSubnetSerializer, StaffSubnetUpdateSerializer

LOG = logging.getLogger(__name__)


class StaffSubnetViewSet(viewsets.ModelViewSet):
    serializer_class = StaffSubnetSerializer
    serializer_map = {'create': StaffSubnetCreateSerializer,
                      'update': StaffSubnetUpdateSerializer}
    permission_classes = (StaffOnly,)

    @property
    def identity_admin_api(self):
        if hasattr(self, 'request'):
            return IdentityAdminApi(request_session=self.request.session)
        else:
            return IdentityAdminApi()

    def get_queryset(self):
        return Subnet.objects.all()

    def get_serializer_class(self):
        return self.serializer_map.get(self.action, self.serializer_class)

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        os_api = Subnets(api_session=self.identity_admin_api.session)
        serializer.validated_data['tenant_id'] = serializer.validated_data['network'].project
        try:
            subnet = os_api.create(kwargs=serializer.validated_data)
            serializer.validated_data['id'] = subnet['subnet']['id']
        except Exception as e:
            LOG.error(e)
            handle(self.request, message=_('Unable to create subnet'))

    def perform_update(self, serializer):
        db_subnet = self.get_object()
        serializer.is_valid(raise_exception=True)
        # do not send allocation pools to openstack if they were not changed
        existing_allocation_pools = db_subnet.allocation_pools
        provided_allocation_pools = serializer.validated_data.get('allocation_pools')
        if len(existing_allocation_pools) == len(provided_allocation_pools):
            allocation_pools_matched = 0
            for e_ap in existing_allocation_pools:
                for p_ap in provided_allocation_pools:
                    if p_ap.get('start') == e_ap.get('start') and p_ap.get('end') == e_ap.get('end'):
                        allocation_pools_matched += 1
            if allocation_pools_matched == len(existing_allocation_pools):
                del serializer.validated_data['allocation_pools']
        os_api = Subnets(api_session=self.identity_admin_api.session)
        try:
            os_api.update(old_values=serializer.instance, new_values=serializer.validated_data)
        except BadRequest as e:
            raise APIBadRequest(e)
        except Exception as e:
            LOG.error(e)
            handle(self.request, message=_('Unable to update subnet'))

    def get_subnet(self, subnet=None):
        subnet = subnet or self.get_object()
        subnet_admin_api = Subnets(api_session=self.identity_admin_api.session)
        return subnet_admin_api.get(subnet=subnet)

    def perform_destroy(self, db_subnet):
        """Delete subnet from neutron and from db."""
        subnet = self.get_subnet()
        region = Network.objects.filter(id=db_subnet.network_id).first().region
        try:
            subnet.delete(region=region)
        except Exception as e:
            LOG.error(e)
            handle(self.request, message=e)

    @action(detail=False, methods=['get'])
    def create_options(self, request):
        network_id = request.query_params.get('network_id', None)
        if not network_id:
            raise APIBadRequest(_('Network id required in request'))
        try:
            network = Network.objects.get(id=network_id)
            pools = SubnetPool.objects.filter(region=network.region)
            ipv6_modes = ['slaac', 'dhcpv6-stateful', 'dhcpv6-stateless']
            return Response({'pools': SubnetPoolSerializer(instance=pools, many=True).data, 'ipv6_modes': ipv6_modes})
        except Network.DoesNotExist:
            raise APIBadRequest(_('Network not found'))
