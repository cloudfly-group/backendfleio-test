from datetime import datetime
from typing import Dict

from django.utils.timezone import now
from django.utils.timezone import utc

from fleio.core.models import PermissionNames
from fleio.core.models import PermissionSet


class Permissions(object):
    def __init__(
            self,
            permission_set: PermissionSet = None,
            permissions: Dict[str, bool] = None,
            implicitly_granted: bool = False,
            created_at: datetime = None):
        if permission_set:
            self.permissions = {
                permission_name: permission_set.permission_granted(permission_name)
                for permission_name in PermissionNames.permissions_map
            }
            self.implicitly_granted = permission_set.implicitly_granted
        else:
            self.permissions = permissions
            self.implicitly_granted = implicitly_granted

        if created_at:
            self.created_at = created_at
        else:
            self.created_at = now()

    def has_permission(self, permission_name):
        return self.permissions.get(permission_name, self.implicitly_granted)

    def get_permission_dict(self):
        return {
            permission_name: self.has_permission(permission_name)
            for permission_name in PermissionNames.permissions_map
        }

    def clone(self):
        return Permissions(permissions=self.permissions, implicitly_granted=self.implicitly_granted)

    def get_view_permissions(self, view_basename: str) -> Dict[str, bool]:
        view_permissions = {}
        permission_prefix = view_basename + '.'
        for permission_name in PermissionNames.permissions_map:
            if permission_name.startswith(permission_prefix):
                view_permissions[permission_name] = self.has_permission(permission_name)

        return view_permissions

    def __or__(self, other: 'Permissions'):
        permissions = {}
        for name in PermissionNames.permissions_map:
            permissions[name] = self.has_permission(name) or other.has_permission(name)
        return Permissions(
            permissions=permissions,
            implicitly_granted=self.implicitly_granted or other.implicitly_granted
        )

    def __and__(self, other: 'Permissions'):
        permissions = {}
        for name in PermissionNames.permissions_map:
            permissions[name] = self.has_permission(name) and other.has_permission(name)
        return Permissions(
            permissions=permissions,
            implicitly_granted=self.implicitly_granted and other.implicitly_granted
        )


ALL_PERMISSIONS = Permissions(permissions={}, implicitly_granted=True, created_at=datetime.min.replace(tzinfo=utc))
NO_PERMISSIONS = Permissions(permissions={}, implicitly_granted=False, created_at=datetime.min.replace(tzinfo=utc))
