from rest_framework import viewsets

from fleio.core.drf import ResellerOnly
from fleio.osbilling.models import ServiceDynamicUsageHistory
from fleio.reseller.utils import user_reseller_resources
from reseller.osbilling.service_dynamic_history.serializers.service_dynamic_usage_history import \
    ServiceDynamicUsageHistorySerializer


class ResellerServiceDynamicUsageHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (ResellerOnly,)
    serializer_class = ServiceDynamicUsageHistorySerializer

    def get_queryset(self):
        reseller_resources = user_reseller_resources(user=self.request.user)
        return ServiceDynamicUsageHistory.objects.filter(
            service_dynamic_usage__service__client__reseller_resources=reseller_resources
        )
