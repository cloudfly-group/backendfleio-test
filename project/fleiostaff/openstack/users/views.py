import logging
from common_admin.openstack.users.views.user import AdminOpenStackUsersViewSet
from fleio.core.drf import CustomPermissions, StaffOnly


LOG = logging.getLogger(__name__)


class StaffOpenStackUsersViewSet(AdminOpenStackUsersViewSet):
    permission_classes = (CustomPermissions, StaffOnly, )
