from plugins.tickets.models.department import Department
from plugins.tickets.enduser.tickets.departments_serializers import DepartmentSerializer

from rest_framework import viewsets
from rest_framework import filters

from django_filters.rest_framework import DjangoFilterBackend

from fleio.core.drf import EndUserOnly
from fleio.core.filters import CustomFilter


class DepartmentsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DepartmentSerializer
    permission_classes = (EndUserOnly,)
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend, CustomFilter, filters.SearchFilter)
    search_fields = (
        'name',
        'email',
    )
    ordering_fields = ('name', 'email', 'created_at')
    filter_fields = ('created_at',)
    queryset = Department.objects.all()
