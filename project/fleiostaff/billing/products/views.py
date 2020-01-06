from common_admin.billing.products.views.product import AdminProductViewSet
from fleio.core.drf import StaffOnly


class StaffProductViewSet(AdminProductViewSet):
    permission_classes = (StaffOnly,)
