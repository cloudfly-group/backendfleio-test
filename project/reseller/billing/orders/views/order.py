from django.utils.translation import ugettext_lazy as _

from common_admin.billing.orders.views.order import AdminOrderViewSet
from fleio.activitylog.utils.decorators import log_reseller_activity
from fleio.core.drf import ResellerOnly
from fleio.reseller.utils import user_reseller_resources


@log_reseller_activity(
    category_name='billing', object_name='order',
    additional_activities={
        'accept': _('Reseller user {username} ({user_id}) accepted order ({object_id}).'),
    }
)
class ResellerOrderViewSet(AdminOrderViewSet):
    permission_classes = (ResellerOnly,)

    def get_queryset(self):
        reseller_resources = user_reseller_resources(user=self.request.user)
        queryset = super().get_queryset().filter(
            client__reseller_resources=reseller_resources
        )

        return queryset
