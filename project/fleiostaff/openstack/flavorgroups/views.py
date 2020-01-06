from common_admin.openstack.flavorgroups.views.flavor_group import AdminFlavorGroupViewSet
from fleio.activitylog.utils.decorators import log_staff_activity
from fleio.core.drf import StaffOnly


@log_staff_activity(category_name='openstack', object_name='flavor group')
class FlavorGroupViewSet(AdminFlavorGroupViewSet):
    permission_classes = (StaffOnly, )
