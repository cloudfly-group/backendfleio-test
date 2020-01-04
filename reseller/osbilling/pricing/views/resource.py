from rest_framework import filters
from rest_framework import viewsets

from fleio.core.drf import ResellerOnly
from fleio.osbilling.models import BillingResource
from reseller.osbilling.pricing.serializers.resource import ResellerResourceSerializer


class ResellerResourceViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (ResellerOnly,)
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('type', 'name')

    serializer_class = ResellerResourceSerializer
    queryset = BillingResource.objects.all()
