from fleio.billing.models import ProductCycle
from fleio.core.drf import ResellerOnly
from fleio.reseller.utils import user_reseller_resources
from fleiostaff.billing.productcycles.views import StaffProductCycleViewSet  # TODO: create common admin viewset


class ResellerProductCycleViewSet(StaffProductCycleViewSet):
    permission_classes = (ResellerOnly,)

    def get_queryset(self):
        reseller_resources = user_reseller_resources(user=self.request.user)
        return ProductCycle.objects.filter(product__reseller_resources=reseller_resources).order_by('pk')
