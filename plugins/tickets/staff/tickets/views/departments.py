from django.db.models import ProtectedError
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from plugins.tickets.models.department import Department, DepartmentNotificationsMap
from plugins.tickets.staff.tickets.departments_serializers import DepartmentSerializer

from rest_framework import filters
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from fleio.core.drf import StaffOnly
from fleio.core.filters import CustomFilter


class DepartmentsViewSet(viewsets.ModelViewSet):
    serializer_class = DepartmentSerializer
    permission_classes = (StaffOnly,)
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend, CustomFilter, filters.SearchFilter)
    search_fields = (
        'name',
        'email',
    )
    ordering_fields = ('name', 'email', 'created_at')
    filter_fields = ('created_at',)
    ordering = ['name']
    queryset = Department.objects.all()

    @action(detail=False, methods=['get'])
    def create_options(self, request):
        del request  # unused
        return Response(data={
            'ticket_id_default_format': getattr(settings, 'TICKET_ID_DEFAULT_FORMAT', '%n%n%n%n%n%n'),
            'notifications': DepartmentNotificationsMap.NOTIFICATIONS
        })

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, kwargs)
        except ProtectedError:
            return Response(
                {
                    'detail': _('Cannot delete departament with assigned tickets.')
                },
                status=status.HTTP_403_FORBIDDEN,
            )
