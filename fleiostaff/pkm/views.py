from common_admin.pkm.views.public_key import AdminPublicKeyViewSet
from fleio.core.drf import CustomPermissions
from fleio.core.drf import StaffOnly


class StaffPublicKeyViewSet(AdminPublicKeyViewSet):
    permission_classes = (CustomPermissions, StaffOnly,)
