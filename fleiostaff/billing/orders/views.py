from django.utils.translation import ugettext_lazy as _

from common_admin.billing.orders.views.order import AdminOrderViewSet
from fleio.activitylog.utils.decorators import log_staff_activity
from fleio.core.drf import StaffOnly


@log_staff_activity(
    category_name='billing', object_name='order',
    additional_activities={
        'accept': _('Staff user {username} ({user_id}) accepted order ({object_id}).'),
    }
)
class StaffOrderViewset(AdminOrderViewSet):
    permission_classes = (StaffOnly,)
