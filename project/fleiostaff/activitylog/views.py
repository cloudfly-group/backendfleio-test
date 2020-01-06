from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from fleio.activitylog.models import Log, LogCategory, LogClass
from fleio.core.drf import StaffOnly
from fleio.core.filters import CustomFilter
from .serializers import ActivityLogSerializer


class ActivityLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ActivityLogSerializer
    permission_classes = (StaffOnly,)
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend, filters.SearchFilter, CustomFilter)
    search_fields = ('ip', 'parameters', 'user__username', 'user__first_name', 'user__last_name', 'log_class__name',
                     'log_class__category__name',)
    ordering_fields = ('id', 'created_at', 'ip', 'user')

    def get_queryset(self):
        return Log.objects.get_queryset().order_by('id')

    @action(detail=False, methods=['GET'])
    def filter_options(self, request, *args, **kwargs):
        del args, kwargs, request  # unused
        filter_options = {
            'actions': LogClass.objects.all().values('name'),
            'categories': LogCategory.objects.all().values('name'),
        }
        return Response(filter_options)
