from common_admin.osbilling.pricing.views.pricing_plan import AdminPricingPlanViewSet
from fleio.core.drf import ResellerOnly
from fleio.reseller.utils import filter_queryset_for_user
from reseller.osbilling.pricing.serializers.pricing_plan import ResellerPricingPlanDeleteSerializer
from reseller.osbilling.pricing.serializers.pricing_plan import ResellerPricingPlanSerializer
from reseller.osbilling.pricing.serializers.pricing_plan import ResellerPricingPlanUpdateSerializer


class ResellerPricingPlanViewSet(AdminPricingPlanViewSet):
    permission_classes = (ResellerOnly,)
    serializer_class = ResellerPricingPlanSerializer
    serializer_map = {
        'destroy': ResellerPricingPlanDeleteSerializer,
        'update': ResellerPricingPlanUpdateSerializer,
    }

    def get_queryset(self):
        return filter_queryset_for_user(super().get_queryset(), self.request.user).all()
