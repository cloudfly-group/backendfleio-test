import logging

from django.utils.translation import ugettext_lazy as _

from common_admin.openstack.images.views.image import AdminImageViewSet
from fleio.activitylog.utils.decorators import log_staff_activity
from fleio.core.drf import CustomPermissions
from fleio.core.drf import StaffOnly

LOG = logging.getLogger(__name__)


@log_staff_activity(
    category_name='openstack', object_name='image',
    additional_activities={
        'deactivate': _('Staff user {username} ({user_id}) deactivated {object_name} {object_id}.'),
        'reactivate': _('Staff user {username} ({user_id}) reactivated {object_name} {object_id}.'),
    }
)
class StaffImageViewSet(AdminImageViewSet):
    permission_classes = (CustomPermissions, StaffOnly,)
