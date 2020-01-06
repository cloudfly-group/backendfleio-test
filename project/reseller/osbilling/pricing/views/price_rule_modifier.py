from rest_framework import filters
from rest_framework import viewsets

from fleio.core.drf import ResellerOnly
from fleio.osbilling.models import PricingRuleModifier
from fleio.reseller.utils import user_reseller_resources
from fleiostaff.osbilling.serializers import PriceRuleModifierSerializer


class ResellerPriceRuleModifiersViewSet(viewsets.ModelViewSet):
    permission_classes = (ResellerOnly,)
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('name',)

    serializer_class = PriceRuleModifierSerializer

    def get_queryset(self):
        reseller_resources = user_reseller_resources(user=self.request.user)
        return PricingRuleModifier.objects.filter(
            price_rule_id=self.kwargs['pricerule_pk'],
            price_rule__plan__reseller_resources=reseller_resources,
        )

    def perform_create(self, serializer):
        serializer.save(price_rule_id=self.kwargs['pricerule_pk'])
