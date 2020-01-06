import logging

from common_admin.openstack.volumes.views.volume import AdminVolumeViewSet
from fleio.activitylog.utils.decorators import log_reseller_activity
from fleio.core.drf import CustomPermissions
from fleio.core.drf import ResellerOnly
from fleio.reseller.utils import user_reseller_resources

LOG = logging.getLogger(__name__)


@log_reseller_activity(
    category_name='openstack', object_name='volume',
)
class ResellerVolumeViewSet(AdminVolumeViewSet):
    permission_classes = (CustomPermissions, ResellerOnly,)

    def get_queryset(self):
        reseller_resources = user_reseller_resources(user=self.request.user)
        queryset = super().get_queryset().filter(
            project__service__client__reseller_resources=reseller_resources,
        ).all()

        return queryset
