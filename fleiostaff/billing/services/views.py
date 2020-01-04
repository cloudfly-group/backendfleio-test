import logging

from django.utils.translation import ugettext_lazy as _

from common_admin.billing.services.views.service import AdminServiceViewSet
from fleio.activitylog.utils.decorators import log_staff_activity

from fleio.core.drf import CustomPermissions, StaffOnly

LOG = logging.getLogger(__name__)


@log_staff_activity(
    category_name='billing', object_name='service',
    additional_activities={
        'activate': _('Staff user {username} ({user_id}) activated service ({object_id}).'),
        'resume': _('Staff user {username} ({user_id}) resumed service ({object_id}).'),
        'suspend': _('Staff user {username} ({user_id}) suspended service ({object_id}).'),
        'terminate': _('Staff user {username} ({user_id}) terminated service ({object_id}).'),
        'update_billing_plan': _(
            'Staff user {username} ({user_id}) updated billing plan for service ({object_id}).'
        ),
    }
)
class StaffServiceViewSet(AdminServiceViewSet):
    permission_classes = (CustomPermissions, StaffOnly,)
