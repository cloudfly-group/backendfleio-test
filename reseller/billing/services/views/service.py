import logging

from django.utils.translation import ugettext_lazy as _

from common_admin.billing.services.views.service import AdminServiceViewSet
from fleio.activitylog.utils.decorators import log_reseller_activity
from fleio.core.drf import CustomPermissions
from fleio.core.drf import ResellerOnly
from fleio.reseller.utils import user_reseller_resources

LOG = logging.getLogger(__name__)


@log_reseller_activity(
    category_name='billing', object_name='service',
    additional_activities={
        'activate': _('Reseller user {username} ({user_id}) activated service ({object_id}).'),
        'resume': _('Reseller user {username} ({user_id}) resumed service ({object_id}).'),
        'suspend': _('Reseller user {username} ({user_id}) suspended service ({object_id}).'),
        'terminate': _('Reseller user {username} ({user_id}) terminated service ({object_id}).'),
        'update_billing_plan': _(
            'Reseller user {username} ({user_id}) updated billing plan for service ({object_id}).'
        ),
    }
)
class ResellerServiceViewSet(AdminServiceViewSet):
    permission_classes = (CustomPermissions, ResellerOnly,)

    def get_queryset(self):
        reseller_resources = user_reseller_resources(user=self.request.user)
        queryset = super().get_queryset().filter(
            client__reseller_resources=reseller_resources
        )

        return queryset
