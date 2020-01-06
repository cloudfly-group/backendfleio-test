import logging

from django.utils.translation import ugettext_lazy as _
from neutronclient.common.exceptions import BadRequest
from rest_framework.decorators import action
from rest_framework.response import Response

from fleio.activitylog.utils.decorators import log_staff_activity
from fleio.core.clients.serializers import ClientMinSerializer
from fleio.core.drf import CustomPermissions, StaffOnly
from fleio.core.exceptions import APIBadRequest
from fleio.core.models import Client
from fleio.core.permissions.permissions_cache import permissions_cache
from fleio.openstack.api.identity import IdentityAdminApi
from fleio.openstack.exceptions import handle
from fleio.openstack.models import FloatingIp, Network
from fleio.openstack.networking.api import FloatingIps
from fleio.openstack.networking.views import FloatingIpViewSet
from .serializers import StaffFloatingIpCreateSerializer, StaffFloatingIpSerializer

LOG = logging.getLogger(__name__)


@log_staff_activity(
    category_name='openstack', object_name='floating ip',
)
class StaffFloatingIpViewSet(FloatingIpViewSet):
    permission_classes = (CustomPermissions, StaffOnly,)
    serializer_class = StaffFloatingIpSerializer
    serializer_map = {'create': StaffFloatingIpCreateSerializer}

    def list(self, request, *args, **kwargs):
        response = super().list(request=request, *args, **kwargs)
        response.data['permissions'] = permissions_cache.get_view_permissions(request.user, self.basename)
        return response

    @property
    def identity_admin_api(self):
        if hasattr(self, 'request'):
            return IdentityAdminApi(request_session=self.request.session)
        else:
            return IdentityAdminApi()

    def get_queryset(self):
        return FloatingIp.objects.all()

    def get_floating_ip(self):
        floating_ip = self.get_object()
        floating_ip_admin_api = FloatingIps(api_session=self.identity_admin_api.session)
        return floating_ip_admin_api.get(floating_ip=floating_ip)

    def get_serializer_class(self):
        return self.serializer_map.get(self.action, self.serializer_class)

    def perform_create(self, serializer):
        floating_ip_admin_api = FloatingIps(api_session=self.identity_admin_api.session)
        try:
            floating_ip = floating_ip_admin_api.create(serializer.validated_data['floating_network'].id,
                                                       serializer.validated_data['description'],
                                                       region=serializer.validated_data['floating_network'].region,
                                                       project_id=serializer.validated_data['project'].project_id)
            serializer.validated_data['id'] = floating_ip['floatingip']['id']
        except BadRequest as e:
            raise APIBadRequest(e)
        except Exception as e:
            LOG.error(e)
            handle(self.request, message=_('Unable to create floating ip'))

    @action(detail=False, methods=['get'])
    def create_options(self, request):
        client_id = self.request.query_params.get('client_id', None)
        if not client_id:
            return Response({'client': {}, 'networks': []})
        try:
            client = Client.objects.get(id=client_id)
        except Client.DoesNotExist:
            return Response({'client': {}, 'networks': []})

        try:
            project_id = client.first_project.project_id
        except (Exception, AttributeError):
            # NOTE: most likely code won't reach this branch because clients with project are filtered on frontend
            raise APIBadRequest(_('Client has no project'))

        networks = Network.objects.get_external_networks(project_id=project_id,
                                                         subnet_count=True)
        fnets = [{'id': network.id, 'name': network.name, 'description': network.description, 'region': network.region}
                 for network in networks.filter(subnet_count__gt=0)]

        return Response({'client': ClientMinSerializer(client).data, 'networks': fnets})

    @action(detail=False, methods=['get'])
    def permissions(self, request):
        view_permissions = permissions_cache.get_view_permissions(request.user, self.basename)
        return Response(data=view_permissions)
