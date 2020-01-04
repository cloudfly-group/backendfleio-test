from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets
from rest_framework import filters
from rest_framework.response import Response

from fleiostaff.openstack.hypervisors.serializers import HypervisorsSerializer

from fleio.openstack.models import Hypervisor

from fleio.core.drf import StaffOnly


class HypervisorsListRetrieveViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (StaffOnly,)
    serializer_class = HypervisorsSerializer
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend, filters.SearchFilter)
    filter_fields = ('host_name', 'host_ip', 'region',)
    ordering_fields = ('host_name', 'host_ip', 'region',)
    search_fields = ('host_name',)
    queryset = Hypervisor.objects.all()

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if pk:
            filtering = Q(id=pk) | Q(host_name=pk)
            instance = Hypervisor.objects.filter(filtering).first()
            if instance:
                serializer = self.get_serializer(instance)
                return Response(serializer.data)
            return super().retrieve(request=request, *args, **kwargs)
        return super().retrieve(request=request, *args, **kwargs)
