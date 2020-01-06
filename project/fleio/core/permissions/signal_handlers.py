from django.db.models.signals import post_save
from django.dispatch import receiver

from fleio.core.models import PermissionNames
from fleio.core.models import PermissionSet


@receiver(post_save, sender=PermissionSet, dispatch_uid='permission_set_post_save')
def permission_set_post_save_callback(**kwargs):
    permission_set = kwargs.get('instance')  # type: PermissionSet
    if kwargs.get('created', False):
        # create all permissions
        for permission_name in PermissionNames.permissions_map:
            permission_set.permissions.create(name=permission_name, granted=permission_set.implicitly_granted)
