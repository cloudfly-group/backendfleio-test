from __future__ import unicode_literals

from ipware.ip import get_ip
from django.conf import settings

from rest_framework import exceptions


def match_session_ip_or_401(request):
    """
    Compare IP address stored in session with current request's IP.
    Use BIND_SESSINON_IP_END_USER and BIND_SESSION_IP_STAFF_USER in settings to toggle checking.

    :raises AuthenticationFailed: If the IP-s do not match.
    """
    current_ip = get_ip(request)
    session_ip = request.session.get('ip')
    if request.user.is_staff and settings.BIND_SESSION_IP_STAFF_USER or \
       not request.user.is_staff and settings.BIND_SESSION_IP_END_USER:
        if current_ip != session_ip:
            raise exceptions.AuthenticationFailed()
