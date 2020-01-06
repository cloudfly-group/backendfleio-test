import logging

from common_admin.openstack.flavors.views.flavor import AdminFlavorViewSet
from fleio.core.drf import CustomPermissions
from fleio.core.drf import StaffOnly

LOG = logging.getLogger(__name__)


class FlavorViewSet(AdminFlavorViewSet):
    permission_classes = (CustomPermissions, StaffOnly,)
