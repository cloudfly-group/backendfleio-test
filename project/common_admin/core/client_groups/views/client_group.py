from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet

from fleio.core.drf import SuperUserOnly
from fleio.core.filters import CustomFilter
from fleio.core.models import ClientGroup
from fleiostaff.core.clientgroups.serializers import ClientGroupSerializer


class AdminClientGroupViewSet(ModelViewSet):
    permission_classes = (SuperUserOnly,)
    model = ClientGroup
    search_fields = ('name',)
    filter_fields = ('name',)
    ordering_fields = ('name', 'id', 'created_at',)
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend, CustomFilter, filters.SearchFilter)
    queryset = ClientGroup.objects.all()
    serializer_map = {}
    serializer_class = ClientGroupSerializer

    def get_serializer_class(self):
        return self.serializer_map.get(self.action, self.serializer_class)
