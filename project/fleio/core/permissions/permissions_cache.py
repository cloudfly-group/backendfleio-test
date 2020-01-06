from typing import Dict

from django.conf import settings
from django.utils.timezone import now

from fleio.core.models import AppUser
from fleio.core.permissions import permissions

PERMISSION_CACHE_EXPIRE_SECONDS = 10


class PermissionsCache(object):
    def __init__(self, expire_seconds: int):
        self.user_permission_cache = {}  # type: Dict[int, permissions.Permissions]
        self.expire_seconds = expire_seconds

    def cache_user_permissions(self, user: AppUser):
        user_permissions = None
        if user.is_superuser:
            # superusers have all permissions
            user_permissions = permissions.ALL_PERMISSIONS.clone()

        if not user_permissions and user.is_anonymous:
            # no permissions for anonymous user
            user_permissions = permissions.NO_PERMISSIONS.clone()

        if not user_permissions:
            has_db_permissions = False
            db_permissions = permissions.NO_PERMISSIONS
            for group in user.user_groups.all():
                if group.permissions:
                    db_permissions = db_permissions | permissions.Permissions(permission_set=group.permissions)
                    has_db_permissions = True

            if user.permissions:
                db_permissions = db_permissions | permissions.Permissions(permission_set=user.permissions)
                has_db_permissions = True

            if has_db_permissions:
                user_permissions = db_permissions
            else:
                if getattr(settings, 'GRANT_ALL_PERMISSIONS_IMPLICITLY', False):
                    user_permissions = permissions.ALL_PERMISSIONS.clone()
                else:
                    user_permissions = permissions.NO_PERMISSIONS.clone()

        self.user_permission_cache[user.id] = user_permissions

    def refresh_cached_permissions(self, user: AppUser):
        age = now() - self.user_permission_cache.get(user.id, permissions.NO_PERMISSIONS).created_at
        if age.total_seconds() > self.expire_seconds:
            self.cache_user_permissions(user=user)

    def get_user_permissions(self, user: AppUser) -> permissions.Permissions:
        self.refresh_cached_permissions(user)
        return self.user_permission_cache[user.id]

    def get_view_permissions(self, user: AppUser, view_basename: str) -> Dict[str, bool]:
        return self.get_user_permissions(user).get_view_permissions(view_basename)


permissions_cache = PermissionsCache(expire_seconds=PERMISSION_CACHE_EXPIRE_SECONDS)
