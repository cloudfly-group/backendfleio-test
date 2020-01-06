import logging

import django_filters
from django.conf import settings
from django.db.models import Q
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from neutronclient.common.exceptions import BadRequest, Conflict, NotFound, OverQuotaClient
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from fleio.activitylog.utils.decorators import log_enduser_activity
from fleio.billing.credit_checker import check_if_enough_credit
from fleio.core.features import active_features
from fleio.core.permissions.permissions_cache import permissions_cache
from fleio.core.drf import CustomPermissions, EndUserOnly
from fleio.core.exceptions import APIBadRequest
from fleio.openstack.networking import serializers as net_serializers
from fleio.openstack.serializers.regions import RegionSerializer
from fleio.openstack.signals.signals import (user_delete_floating_ip, user_delete_network, user_delete_router,
                                             user_delete_security_group)
from fleio.openstack.views.regions import get_regions
from fleiostaff.openstack.routers.serializers import SubnetInterfaceSerializer
from fleiostaff.openstack.subnets.serializers import StaffSubnetCreateSerializer
from fleiostaff.openstack.subnets.serializers import StaffSubnetUpdateSerializer
from .filters import NetworkFilter
from ..exceptions import APIConflict, handle, ObjectNotFound
from ..models import FloatingIp, Network, Port, Router, SecurityGroup, Subnet, SubnetPool
from ..osapi import OSApi
from fleio.core.filters import CustomFilter
from fleio.core.validation_utils import validate_cloud_objects_limit

LOG = logging.getLogger(__name__)


@log_enduser_activity(
    category_name='openstack', object_name='network',
)
class NetworkViewSet(viewsets.ModelViewSet):
    serializer_class = net_serializers.NetworkSerializerExtra
    serializer_map = {'create': net_serializers.NetworkCreateSerializer,
                      'update': net_serializers.NetworkUpdateSerializer,
                      'auto_create_network': net_serializers.NetworkAutoCreateSerializer}
    permission_classes = (CustomPermissions, EndUserOnly,)
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend, CustomFilter, filters.SearchFilter)
    filter_class = NetworkFilter
    ordering_fields = ('name', 'created_at', 'region')
    search_fields = ('name', 'created_at', 'region')

    def get_queryset(self):
        client = self.request.user.clients.filter(services__openstack_project__isnull=False).first()
        if not client:
            raise APIConflict(_('No client with an OpenStack project found'))
        return Network.objects.get_networks_for_project(
            project_id=client.first_project.project_id,
            external=active_features.is_enabled('openstack.networks.display_external_networks'),
            shared=active_features.is_enabled('openstack.networks.display_shared_networks'),
        )

    def list(self, request, *args, **kwargs):
        response = super().list(request=request, *args, **kwargs)
        response.data['permissions'] = permissions_cache.get_view_permissions(request.user, self.basename)
        return response

    def get_serializer_class(self):
        return self.serializer_map.get(self.action, self.serializer_class)

    def perform_create(self, serializer):
        os_api = OSApi.from_request(request=self.request)
        try:
            network = os_api.networks.create(kwargs=serializer.validated_data)
            network = network['network']
            serializer.validated_data['id'] = network['id']
        except BadRequest as e:
            raise APIBadRequest(force_text(e))
        except Exception as e:
            LOG.error(e)
            handle(self.request, message=_('Unable to create network'))

    def perform_update(self, serializer):
        serializer.is_valid(raise_exception=True)
        os_api = OSApi.from_request(request=self.request)
        try:
            os_api.networks.update(old_values=serializer.instance, new_values=serializer.validated_data)
        except BadRequest as e:
            raise APIBadRequest(force_text(e))
        except Exception as e:
            LOG.error(e)
            handle(self.request, message=_('Unable to update network'))

    def get_network(self):
        network = self.get_object()
        os_api = OSApi.from_request(request=self.request)
        return os_api.networks.get(network=network)

    def perform_destroy(self, db_network):
        """Delete network from neutron and from db."""
        network = self.get_network()
        region = db_network.region
        try:
            network.delete(region=region)
        except NotFound:
            raise ObjectNotFound(_('Can not delete network'))
        except Exception as e:
            LOG.error(e)
            handle(self.request, message=force_text(e))
        else:
            user = self.request.user
            user_delete_network.send(sender=__name__, user=user, user_id=user.id,
                                     network_name=db_network.name, network_id=db_network.id,
                                     username=user.username, request=self.request)

    @action(detail=False, methods=['get'])
    def permissions(self, request):
        view_permissions = permissions_cache.get_view_permissions(request.user, self.basename)
        return Response(data=view_permissions)

    @action(detail=False, methods=['POST'])
    def auto_create_network(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        os_api = OSApi.from_request(request=self.request)
        client = request.user.clients.filter(services__openstack_project__isnull=False).first()
        if not client:
            raise APIConflict(_('No client with an OpenStack project found'))
        net_id = None
        try:
            net_id = os_api.networks.auto_create_network(project_id=client.first_project.project_id,
                                                         region=serializer.validated_data['region'])
        except Exception as e:
            LOG.error(e)
            handle(self.request, message=_('Unable to auto create network'))
        return Response({'id': net_id})

    @action(detail=False, methods=['get'])
    def create_options(self, request):
        selected_region, regions = get_regions(request, for_end_user=True)
        return Response({
            'regions': RegionSerializer(instance=regions, many=True).data,
            'selected_region': selected_region,
            'can_create_resource': check_if_enough_credit(
                client=self.request.user.clients.all().first(), update_uptodate_credit=False,
            )
        })

    @action(detail=False, methods=['get'])
    def get_subnet_pools(self, request):
        region = request.query_params.get('region', None)
        if not region:
            raise APIBadRequest(_('Region required in request'))
        pools = SubnetPool.objects.filter(region=region)
        return Response({'pools': net_serializers.SubnetPoolSerializer(instance=pools, many=True).data})


class FloatingIPFilters(FilterSet):
    region = django_filters.CharFilter(field_name='floating_network__region')

    class Meta:
        model = FloatingIp
        fields = ('floating_ip_address', 'floating_network', 'region')


@log_enduser_activity(
    category_name='openstack', object_name='floating ip',
)
class FloatingIpViewSet(viewsets.ModelViewSet):
    serializer_class = net_serializers.FloatingIpSerializer
    serializer_map = {'create': net_serializers.FloatingIpCreateSerializer}
    permission_classes = (CustomPermissions, EndUserOnly,)
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend, CustomFilter, filters.SearchFilter)
    filter_class = FloatingIPFilters
    ordering_fields = ('floating_ip_address', 'floating_network', 'status')
    search_fields = ('floating_ip_address',)

    def get_queryset(self):
        user_clients = self.request.user.clients.filter(services__openstack_project__isnull=False).distinct()
        return FloatingIp.objects.filter(project__service__client__in=user_clients).distinct()

    def get_serializer_class(self):
        return self.serializer_map.get(self.action, self.serializer_class)

    def list(self, request, *args, **kwargs):
        response = super().list(request=request, *args, **kwargs)
        response.data['permissions'] = permissions_cache.get_view_permissions(request.user, self.basename)
        return response

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        os_api = OSApi.from_request(request=self.request)
        try:
            floating_ip = os_api.floating_ips.create(serializer.validated_data['floating_network'].id,
                                                     serializer.validated_data['description'],
                                                     region=serializer.validated_data['floating_network'].region)
            serializer.validated_data['id'] = floating_ip['floatingip']['id']
        except BadRequest as e:
            raise APIBadRequest(force_text(e))
        except Exception as e:
            LOG.error(e)
            handle(self.request, message=_('Unable to create floating ip'))

    def get_floating_ip(self):
        floating_ip = self.get_object()
        os_api = OSApi.from_request(request=self.request)
        return os_api.floating_ips.get(floating_ip=floating_ip)

    def perform_destroy(self, db_floating_ip):
        """Delete flavor from nova and from db."""
        floating_ip = self.get_floating_ip()
        try:
            # FIXME(tomo): We just except Exception, this is not ok
            region = db_floating_ip.floating_network.region
        except Exception as e:
            LOG.error(e)
            handle(self.request, message=force_text(e))
        else:
            try:
                floating_ip.delete(region=region)
            except Exception as e:
                LOG.error(e)
                handle(self.request, message=force_text(e))
            else:
                user = self.request.user
                user_delete_floating_ip.send(sender=__name__, user=user, user_id=user.id,
                                             floating_ip=db_floating_ip.floating_ip_address,
                                             floating_ip_id=db_floating_ip.id,
                                             username=user.username, request=self.request)

    @action(detail=False, methods=['get'])
    def create_options(self, request):
        client = request.user.clients.filter(services__openstack_project__isnull=False).first()
        if client is None:
            raise APIConflict(detail=_('No client with an Openstack project found'))
        networks = Network.objects.get_external_networks(
            project_id=client.first_project.project_id,
            subnet_count=True).filter(
            subnet_count__gt=0
        )

        fnets = [{
            'id': network.id,
            'name': network.name,
            'region': network.region,
            'description': network.description
        } for network in networks]

        return Response({
            'networks': fnets,
            'can_create_resource': check_if_enough_credit(
                client=self.request.user.clients.all().first(), update_uptodate_credit=False,
            ),
        })

    @action(detail=False, methods=['get'])
    def permissions(self, request):
        view_permissions = permissions_cache.get_view_permissions(request.user, self.basename)
        return Response(data=view_permissions)


class SubnetViewSet(viewsets.ModelViewSet):
    serializer_class = net_serializers.SubnetSerializer
    serializer_map = {'create': StaffSubnetCreateSerializer,
                      'update': StaffSubnetUpdateSerializer}
    permission_classes = (EndUserOnly,)

    def get_queryset(self):
        client = self.request.user.clients.filter(services__openstack_project__disabled=False).first()
        user_networks = Network.objects.get_networks_for_project(project_id=client.first_project.project_id)
        return Subnet.objects.filter(id__in=user_networks.values_list('subnet__id'))

    def get_serializer_class(self):
        return self.serializer_map.get(self.action, self.serializer_class)

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        os_api = OSApi.from_request(request=self.request)
        try:
            subnet = os_api.subnets.create(kwargs=serializer.validated_data)
            serializer.validated_data['id'] = subnet['subnet']['id']
        except BadRequest as e:
            raise APIBadRequest(force_text(e))
        except Conflict as e:
            raise APIConflict(force_text(e))
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
        os_api = OSApi.from_request(request=self.request)
        try:
            os_api.subnets.update(old_values=serializer.instance, new_values=serializer.validated_data)
        except BadRequest as e:
            raise APIBadRequest(force_text(e))
        except Conflict as e:
            raise APIConflict(force_text(e))
        except Exception as e:
            LOG.error(e)
            handle(self.request, message=_('Unable to update subnet'))

    def get_subnet(self, subnet=None):
        subnet = subnet or self.get_object()
        os_api = OSApi.from_request(request=self.request)
        return os_api.subnets.get(subnet=subnet)

    def perform_destroy(self, db_subnet):
        """Delete subnet from neutron and from db."""
        subnet = self.get_subnet()
        region = Network.objects.filter(id=db_subnet.network_id).first().region
        try:
            subnet.delete(region=region)
        except BadRequest as e:
            raise APIBadRequest(force_text(e))
        except Conflict as e:
            raise APIConflict(force_text(e))
        except Exception as e:
            LOG.error(e)
            handle(self.request, message=force_text(e))

    @action(detail=False, methods=['get'])
    def create_options(self, request):
        network_id = request.query_params.get('network_id', None)
        if not network_id:
            raise APIBadRequest(_('Network id required in request'))
        try:
            network = Network.objects.get(id=network_id)
            user_clients = self.request.user.clients.filter(services__openstack_project__isnull=False).distinct()
            pools = SubnetPool.objects.filter(region=network.region).filter(
                Q(project_id__in=user_clients.values_list('services__openstack_project__project_id')) | Q(shared=True))
            ipv6_modes = ['slaac', 'dhcpv6-stateful', 'dhcpv6-stateless']
            return Response(
                {'pools': net_serializers.SubnetPoolSerializer(instance=pools, many=True).data,
                 'ipv6_modes': ipv6_modes})
        except Network.DoesNotExist:
            raise APIBadRequest(_('Network not found'))


@log_enduser_activity(
    category_name='openstack', object_name='router',
)
class RouterViewSet(viewsets.ModelViewSet):
    serializer_class = net_serializers.RouterSerializer
    serializer_map = {'create': net_serializers.RouterCreateSerializer,
                      'update': net_serializers.RouterUpdateSerializer,
                      'retrieve': net_serializers.RouterDetailSerializer}
    permission_classes = (CustomPermissions, EndUserOnly,)
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend, CustomFilter, filters.SearchFilter)
    ordering_fields = ('name', 'admin_state_up', 'region__id')
    search_fields = ('name', 'region__id')
    ordering = ['id']

    def get_serializer_class(self):
        return self.serializer_map.get(self.action, self.serializer_class)

    def get_queryset(self):
        user_clients = self.request.user.clients.filter(services__openstack_project__isnull=False).distinct()
        return Router.objects.filter(
            project_id__in=user_clients.values_list('services__openstack_project__project_id')
        ).distinct()

    def list(self, request, *args, **kwargs):
        response = super().list(request=request, *args, **kwargs)
        response.data['permissions'] = permissions_cache.get_view_permissions(request.user, self.basename)
        return response

    def perform_create(self, serializer):
        if not validate_cloud_objects_limit():
            raise APIBadRequest(_('Licence cloud objects limit reached. Please check your license.'))
        serializer.is_valid(raise_exception=True)
        os_api = OSApi.from_request(request=self.request)
        try:
            os_api.routers.create(kwargs=serializer.validated_data)
        except Exception as e:
            LOG.error(e)
            handle(self.request, message=_('Unable to create router'))

    def perform_update(self, serializer):
        serializer.is_valid(raise_exception=True)
        os_api = OSApi.from_request(request=self.request)
        try:
            os_api.routers.update(id=serializer.instance.id, region=serializer.instance.region,
                                  kwargs=serializer.validated_data)
        except Exception as e:
            LOG.error(e)
            handle(self.request, message=_('Unable to update router'))

    def perform_destroy(self, db_router):
        """Delete router from neutron and from db."""
        os_api = OSApi.from_request(request=self.request)
        router = os_api.routers.get(router=db_router)
        try:
            router.delete(region=db_router.region_id)
        except Exception as e:
            LOG.error(e)
            handle(self.request, message=e)
        else:
            user = self.request.user
            user_delete_router.send(sender=__name__, user=user, user_id=user.id,
                                    router_name=db_router.name, router_id=db_router.id,
                                    username=user.username, request=self.request)

    @action(detail=False, methods=['get'])
    def create_options(self, request):
        client = self.request.user.clients.filter(services__openstack_project__isnull=False).first()
        if not client:
            raise APIConflict(_('No client with an OpenStack project found'))
        selected_region, regions = get_regions(request, for_end_user=True)
        external_networks = [{'name': net.name, 'id': net.id, 'region': net.region} for net in
                             Network.objects.get_networks_for_project(project_id=client.first_project.project_id,
                                                                      external=True).filter(router_external=True)]
        return Response({
            'regions': regions,
            'external_networks': external_networks,
            'selected_region': selected_region,
            'can_create_resource': check_if_enough_credit(
                client=self.request.user.clients.all().first(), update_uptodate_credit=False,
            ),
        })

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
        subnets = Subnet.objects.filter(
            network__project=router.project_id
        ).exclude(Q(id__in=subnet_id_list) | Q(network__router_external=True) | ~Q(network__region=router.region_id))

        if not subnets:
            raise ObjectNotFound(_('No subnets available'))
        return Response({'subnets': SubnetInterfaceSerializer(instance=subnets, many=True).data})

    @action(detail=True, methods=['post'])
    def add_interface(self, request, pk):
        """Add an interface to a router"""
        db_router = self.get_object()
        os_api = OSApi.from_request(request=self.request)
        router = os_api.routers.get(router=db_router)
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
        os_api = OSApi.from_request(request=self.request)
        router = os_api.routers.get(router=db_router)
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


@log_enduser_activity(
    category_name='openstack', object_name='security group',
)
class SecurityGroupViewSet(viewsets.ModelViewSet):
    serializer_class = net_serializers.SecurityGroupSerializer
    serializer_map = {'create': net_serializers.SecurityGroupCreateSerializer,
                      'retrieve': net_serializers.SecurityGroupDetailSerializer,
                      'update': net_serializers.SecurityGroupUpdateSerializer,
                      'add_rule': net_serializers.SecurityGroupRuleCreateSerializer}
    permission_classes = (CustomPermissions, EndUserOnly,)
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend, CustomFilter, filters.SearchFilter)
    ordering_fields = ('name', 'created_at', 'region')
    search_fields = ('name',)
    ordering = ['id']

    def get_os_api(self):
        return OSApi.from_request(request=self.request)

    def get_queryset(self):
        client = self.request.user.clients.filter(services__openstack_project__isnull=False).first()
        if not client:
            raise APIConflict(_('No client with an OpenStack project found'))
        return SecurityGroup.objects.filter(project_id=client.first_project.project_id)

    def get_serializer_class(self):
        return self.serializer_map.get(self.action, self.serializer_class)

    def list(self, request, *args, **kwargs):
        response = super().list(request=request, *args, **kwargs)
        response.data['permissions'] = permissions_cache.get_view_permissions(request.user, self.basename)
        return response

    def perform_create(self, serializer):
        os_api = self.get_os_api()
        try:
            security_group = os_api.security_groups.create(**serializer.validated_data)
            security_group = security_group['security_group']
            serializer.validated_data['id'] = security_group['id']
        except BadRequest as e:
            raise APIBadRequest(force_text(e))
        except OverQuotaClient:
            raise APIConflict(_('Security groups limit reached'))
        except Exception as e:
            LOG.error(e)
            handle(self.request, message=_('Unable to create security group'))

    def perform_update(self, serializer):
        os_api = self.get_os_api()
        try:
            os_api.security_groups.update(id=serializer.instance.id, region=serializer.instance.region,
                                          kwargs=serializer.validated_data)
        except BadRequest as e:
            raise APIBadRequest(force_text(e))
        except Exception as e:
            LOG.error(e)
            handle(self.request, message=_('Unable to update security group'))

    def perform_destroy(self, db_security_group):
        """Delete security group from neutron and from db."""
        os_api = self.get_os_api()
        try:
            os_api.security_groups.get(security_group=db_security_group).delete(region=db_security_group.region.id)
        except NotFound:
            raise ObjectNotFound(_('Can not delete security group'))
        except Exception as e:
            LOG.error(e)
            handle(self.request, message=force_text(e))
        else:
            user = self.request.user
            user_delete_security_group.send(sender=__name__, user=user, user_id=user.id,
                                            secgroup_name=db_security_group.name, secgroup_id=db_security_group.id,
                                            username=user.username, request=self.request)

    @action(detail=False, methods=['get'])
    def create_options(self, request, *args, **kwargs):
        selected_region, regions = get_regions(request, for_end_user=True)
        return Response({
            'regions': regions,
            'selected_region': selected_region,
            'can_create_resource': check_if_enough_credit(
                client=self.request.user.clients.all().first(), update_uptodate_credit=False,
            ),
        })

    @action(detail=True, methods=['post'])
    def add_rule(self, request, pk):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        db_security_group = self.get_object()
        os_api = self.get_os_api()
        security_group = os_api.security_groups.get(security_group=db_security_group)
        try:
            security_group.create_rule(region=db_security_group.region.id, **serializer.validated_data)
        except OverQuotaClient:
            raise APIConflict(_('Security rules limit reached'))
        except Exception as e:
            LOG.error(e)
            handle(self.request, message=force_text(e))
        return Response({'detail': _('Rule create scheduled')}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def delete_rule(self, request, pk):
        if 'rule_id' not in request.data:
            raise APIBadRequest(_('rule_id is missing'))

        db_security_group = self.get_object()
        os_api = self.get_os_api()
        security_group = os_api.security_groups.get(security_group=db_security_group)
        try:
            security_group.delete_rule(region=db_security_group.region.id, rule_id=request.data['rule_id'])
        except Exception as e:
            LOG.error(e)
            handle(self.request, message=force_text(e))
        return Response({'detail': _('Rule delete scheduled')}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def permissions(self, request):
        view_permissions = permissions_cache.get_view_permissions(request.user, self.basename)
        return Response(data=view_permissions)
