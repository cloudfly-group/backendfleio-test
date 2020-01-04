import pytz
from datetime import datetime, timedelta

from django.conf import settings
from django.utils.timezone import now as utcnow

from rest_framework import permissions

from fleio.core.second_factor_auth.utils import REMEMBER_PASSWORD_CONFIRM_MINUTES


class SFAManagerPermissions(permissions.BasePermission):
    """Allow or deny access to manage sfa methods based on password confirmation."""
    message = 'Unable to perform the requested action'

    def has_permission(self, request, view):
        if not request.user.is_staff and 'impersonate' in request.session:
            return True
        elapsed_time_since_last_login = utcnow() - request.user.last_login
        if elapsed_time_since_last_login < timedelta(
                minutes=getattr(settings, 'ALLOW_CHANGING_SFA_AFTER_LOGIN_MINUTES', 5)
        ):
            return True  # if user logged in earlier than 2 mins he is allowed
        if 'sfa_manager' in request.session:
            allowed_at = datetime.strptime(request.session['sfa_manager']['allowed_at'], '%B %d %Y - %H:%M:%S')
            allowed_at = allowed_at.replace(tzinfo=pytz.utc)
            elapsed_time_since_last_allowed = utcnow() - allowed_at
            if elapsed_time_since_last_allowed > timedelta(minutes=REMEMBER_PASSWORD_CONFIRM_MINUTES):
                # more than defined time passed since last password confirmation
                return False
            return request.session['sfa_manager']['allowed']
        return False
