from django.utils.translation import ugettext_lazy as _
from rest_framework import permissions

from fleio.core.drf import CustomPermissions

from fleio.billing.credit_checker import check_if_enough_credit


class BillingPermissions(permissions.BasePermission):
    """Allow or deny access based on credit balance."""
    message = 'Unable to perform the requested action'

    def has_permission(self, request, view):
        credit_required = _('Unable to perform this action. Your account credit is too low')
        client = request.user.clients.first()
        if client and hasattr(client, 'client_billing'):
            if view.action in ('create', 'rebuild', 'rescue', 'resize', 'create_snapshot', 'reset_state',
                               'extend', 'get_generated_key_pair', 'create_backup'):
                if not check_if_enough_credit(client=client, update_uptodate_credit=True):
                    self.message = credit_required
                    return False
        return True


# NOTE(tomo): This module needs to be imported from apps.py
permissions = (BillingPermissions, )
for perm in permissions:
    CustomPermissions.register(perm())
