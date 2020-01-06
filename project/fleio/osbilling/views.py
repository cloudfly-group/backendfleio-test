import logging

from rest_framework import viewsets

from fleio.billing.models import Service
from fleio.core.drf import EndUserOnly
from fleio.osbilling.models import ServiceDynamicUsage, ServiceDynamicUsageHistory
from fleio.osbilling.serializers import ServiceDynamicUsageHistoryListSerializer, ServiceDynamicUsageSerializer
from fleio.osbilling.serializers import ServiceDynamicUsageHistorySerializer

LOG = logging.getLogger(__name__)


class ServiceDynamicUsageViewset(viewsets.ReadOnlyModelViewSet):
    permission_classes = (EndUserOnly,)
    serializer_class = ServiceDynamicUsageSerializer

    def get_queryset(self):
        services = Service.objects.filter(client__in=self.request.user.clients.all())
        return ServiceDynamicUsage.objects.filter(service__in=services).order_by('service__status')


class ServiceDynamicUsageHistoryViewset(viewsets.ReadOnlyModelViewSet):
    permission_classes = (EndUserOnly,)
    serializer_class = ServiceDynamicUsageHistoryListSerializer

    serializer_map = {'list': ServiceDynamicUsageHistoryListSerializer,
                      'retrieve': ServiceDynamicUsageHistorySerializer
                      }

    def get_serializer_class(self):
        return self.serializer_map.get(self.action, self.serializer_class)

    def get_queryset(self):
        return ServiceDynamicUsageHistory.objects.filter(
            service_dynamic_usage__service__client__in=self.request.user.clients.all()
        )
