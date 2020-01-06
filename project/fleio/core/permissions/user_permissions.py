from rest_framework.permissions import BasePermission

from django.utils.translation import ugettext_lazy as _

from fleio.core.drf import CustomPermissions
from fleio.core.models import AppUser

from fleio.core.permissions.permissions_cache import permissions_cache


class UserPermissions(BasePermission):
    message = _('You do not have permissions to perform the requested action')

    @staticmethod
    def user_has_permission(user: AppUser, view) -> bool:
        permission_name = '{}.{}'.format(view.basename, view.action)
        user_permissions = permissions_cache.get_user_permissions(user)
        return user_permissions.has_permission(permission_name=permission_name)

    def has_permission(self, request, view):
        # check permission
        return UserPermissions.user_has_permission(request.user, view)


CustomPermissions.register(UserPermissions())
