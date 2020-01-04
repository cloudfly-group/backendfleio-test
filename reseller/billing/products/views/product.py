from common_admin.billing.products.views.product import AdminProductViewSet
from fleio.core.drf import ResellerOnly
from fleio.reseller.utils import user_reseller_resources


class ResellerProductViewSet(AdminProductViewSet):
    permission_classes = (ResellerOnly,)

    def get_queryset(self):
        reseller_resources = user_reseller_resources(user=self.request.user)
        return super().get_queryset().filter(reseller_resources=reseller_resources).all()

    def perform_create(self, serializer):
        serializer.validated_data['reseller'] = self.request.user
        serializer.save()
