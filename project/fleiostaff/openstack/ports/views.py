import logging

from django.utils.translation import ugettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from neutronclient.common.exceptions import BadRequest
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from fleio.activitylog.utils.activity_helper import activity_helper
from fleio.activitylog.utils.decorators import log_staff_activity
from fleio.core.permissions.permissions_cache import permissions_cache
from fleio.core.drf import CustomPermissions, StaffOnly
from fleio.core.exceptions import APIBadRequest
from fleio.openstack.api.identity import IdentityAdminApi
from fleio.openstack.exceptions import handle
from fleio.openstack.models import Port
from fleio.openstack.networking.api import Ports
from fleio.openstack.signals.signals import instance_attach_ips, instance_delete_port, instance_detach_ips
from fleio.openstack.views.regions import get_regions
from fleiostaff.openstack.ports.filters import PortFilters
from .serializers import StaffPortCreateSerializer, StaffPortSerializer, StaffPortUpdateSerializer

LOG = logging.getLogger(__name__)


@log_staff_activity(
    category_name='openstack', object_name='port',
)
class StaffPortViewSet(viewsets.ModelViewSet):
    serializer_class = StaffPortSerializer
    serializer_map = {'create': StaffPortCreateSerializer,
                      'update': StaffPortUpdateSerializer,
                      'add_ip': StaffPortUpdateSerializer,
                      'automatic_add_ips': StaffPortUpdateSerializer,
                      'remove_ip': StaffPortUpdateSerializer}
    permission_classes = (CustomPermissions, StaffOnly,)
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend, filters.SearchFilter)
    filter_class = PortFilters
    ordering_fields = ('name', 'fixed_ips', 'network')
    search_fields = ('fixed_ips', 'name')

    def get_queryset(self):
        return Port.objects.all()

    @property
    def openstack_admin_session(self):
        if self.request and self.request.session:
            return IdentityAdminApi(request_session=self.request.session).session
        else:
            return IdentityAdminApi().session

    def get_serializer_class(self):
        return self.serializer_map.get(self.action, self.serializer_class)

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        port_admin_api = Ports(api_session=self.openstack_admin_session)
        try:
            port = port_admin_api.create(kwargs=serializer.validated_data)['port']
            activity_helper.add_current_activity_params(object_id=port['id'])
            user = self.request.user
            instance_attach_ips.send(sender=__name__, user=user, user_id=user.id,
                                     port_id=port['id'], instance_id=serializer.validated_data['device_id'],
                                     ips=', '.join([f_ip['ip_address'] for f_ip in port['fixed_ips']]),
                                     network_id=port['network_id'], username=user.username, request=self.request)
        except Exception as e:
            LOG.error(e)
            handle(self.request, message=_('Unable to create port'))

    def perform_update(self, serializer):
        serializer.is_valid(raise_exception=True)
        port_admin_api = Ports(api_session=self.openstack_admin_session)
        try:
            port = port_admin_api.update(old_data=serializer.instance, kwargs=serializer.validated_data)
            serializer.validated_data.update(port['port'])
        except BadRequest as e:
            raise APIBadRequest(e)
        except Exception as e:
            LOG.error(e)
            handle(self.request, message=_('Unable to update port'))

    @action(detail=True, methods=['POST'])
    def add_ip(self, request, pk):
        del pk  # unused
        port = self.get_port()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            port = port.add_ip(kwargs=serializer.validated_data)
            user = self.request.user
            instance_attach_ips.send(sender=__name__, user=user, user_id=user.id,
                                     port_id=port['port']['id'], instance_id=port['port']['device_id'],
                                     ips=', '.join(
                                         [f_ip['ip_address'] for f_ip in serializer.validated_data['fixed_ips']]),
                                     network_id=port['port']['network_id'], username=user.username,
                                     request=self.request)
            serializer.validated_data.update(port['port'])
        except BadRequest as e:
            raise APIBadRequest(e)
        except Exception as e:
            LOG.error(e)
            handle(self.request, message=_('Unable to add ip'))
        return Response({'detail': _('IP added')})

    @action(detail=True, methods=['POST'])
    def automatic_add_ips(self, request, pk):
        del pk  # unused
        port = self.get_port()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            openstack_port = port.add_ips(kwargs=serializer.validated_data)['port']
            user = self.request.user
            instance_attach_ips.send(sender=__name__, user=user, user_id=user.id,
                                     port_id=openstack_port['id'],
                                     instance_id=openstack_port['device_id'],
                                     ips=', '.join(
                                         [f_ip['ip_address'] for f_ip in openstack_port['fixed_ips'] if
                                          f_ip not in port.port.fixed_ips]),
                                     network_id=openstack_port['network_id'], username=user.username,
                                     request=self.request)
            serializer.validated_data.update(openstack_port)
        except BadRequest as e:
            raise APIBadRequest(e)
        except Exception as e:
            LOG.error(e)
            handle(self.request, message=_('Unable to add IP(s)'))
        return Response({'detail': _('IP(s) added')})

    @action(detail=True, methods=['POST'])
    def remove_ip(self, request, pk):
        del pk  # unused
        port = self.get_port()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            port = port.remove_ip(kwargs=serializer.validated_data)
            user = self.request.user
            instance_detach_ips.send(sender=__name__, user=user, user_id=user.id,
                                     port_id=port['port']['id'], instance_id=port['port']['device_id'],
                                     ips=', '.join(
                                         [f_ip['ip_address'] for f_ip in serializer.validated_data['fixed_ips']]),
                                     network_id=port['port']['network_id'], username=user.username,
                                     request=self.request)
            serializer.validated_data.update(port['port'])
        except BadRequest as e:
            raise APIBadRequest(e)
        except Exception as e:
            LOG.error(e)
            handle(self.request, message=_('Unable to remove ip'))
        return Response({'detail': _('IP removed')})

    def get_port(self, port=None):
        port = port or self.get_object()
        port_admin_api = Ports(api_session=self.openstack_admin_session)
        return port_admin_api.get(port=port)

    def perform_destroy(self, db_port):
        """Delete port from neutron and from db."""
        port = self.get_port()
        try:
            port.delete(region=db_port.network.region)
            user = self.request.user
            instance_delete_port.send(sender=__name__, user=user, user_id=user.id,
                                      port_id=db_port.id, instance_id=db_port.device_id,
                                      ips=', '.join([f_ip['ip_address'] for f_ip in db_port.fixed_ips]),
                                      network_id=db_port.network_id, username=user.username, request=self.request)
        except Exception as e:
            LOG.error(e)
            handle(self.request, message=e)

    @action(detail=False, methods=['get'])
    def create_options(self, request):
        regions = get_regions(request)
        return Response({'regions': regions})

    @action(detail=False, methods=['get'])
    def permissions(self, request):
        view_permissions = permissions_cache.get_view_permissions(request.user, self.basename)
        return Response(data=view_permissions)
