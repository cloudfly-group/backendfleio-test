import logging

from common_admin.openstack.volumes.views.volume import AdminVolumeViewSet
from fleio.activitylog.utils.decorators import log_staff_activity
from fleio.core.drf import CustomPermissions, StaffOnly

LOG = logging.getLogger(__name__)


@log_staff_activity(
    category_name='openstack', object_name='volume',
)
class StaffVolumeViewSet(AdminVolumeViewSet):
    permission_classes = (CustomPermissions, StaffOnly,)
