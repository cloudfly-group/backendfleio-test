from django.utils.translation import ugettext_lazy as _

from fleio.core.drf import ResellerOnly
from fleio.core.exceptions import ForbiddenException
from fleiostaff.core.views import StaffUserProfileViewSet


class ResellerUserProfileViewSet(StaffUserProfileViewSet):
    permission_classes = (ResellerOnly,)

    @staticmethod
    def allowed_to_update(user):
        if user.is_superuser is True or user.is_staff is True or not user.is_reseller:
            raise ForbiddenException(detail=_('Cannot update own staff or reseller status.'))
