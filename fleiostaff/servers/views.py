from django_filters.rest_framework import DjangoFilterBackend
from fleio.core.filters import CustomFilter
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from fleio.core.plugins.plugin_utils import PluginUtils
from fleio.servers.models import Server, ServerGroup
from fleio.core.drf import StaffOnly
from fleio.servers.models.server import ServerStatus
from .serializers import ServerDetailSerializer, ServerListSerializer
from .serializers import ServerSerializer
from .serializers import ServerGroupSerializer


class StaffServerViewSet(viewsets.ModelViewSet):
    permission_classes = (StaffOnly, )
    queryset = Server.objects.all()
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend, CustomFilter, filters.SearchFilter)
    filter_fields = ('plugin',)

    def get_serializer_class(self):
        if self.action == 'list':
            return ServerListSerializer
        elif self.action == 'retrieve':
            return ServerDetailSerializer
        return ServerSerializer

    @action(methods=['GET'], detail=False)
    def create_options(self, request):
        groups = ServerGroup.objects.values('id', 'name')
        server_plugins = PluginUtils.get_server_plugins()
        return Response({'statusList': ServerStatus.CHOICES,
                         'plugins': server_plugins,
                         'groups': groups})


class StaffServerGroupViewSet(viewsets.ModelViewSet):
    permission_classes = (StaffOnly,)
    queryset = ServerGroup.objects.all()
    serializer_class = ServerGroupSerializer
