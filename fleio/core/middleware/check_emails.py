from django.urls import resolve
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from django.utils.translation import ugettext_lazy as _
from rest_framework import status
from fleio.core.signup.settings import signup_settings


class CheckUserEmailMiddleware(MiddlewareMixin):
    """Make sure the current user has an email address that was verified"""
    whitelisted_url_names = ('current-user', 'login', 'dynamic-ui-custom-menu-links', 'resend-email-confirmation',
                             'userprofile-create-options', 'userprofile-detail', 'userprofile-list',
                             'plugins-plugins-with-component', 'plugins-plugins-with-notifications',
                             'client-list', 'client-create-options', 'logout', 'reset-password',
                             'reset-password-confirm', 'email-sign-up-confirmation', 'dynamic-ui-plugin-data',
                             'tickets-get-current-user-tickets-count', 'get-external-billing-url',)

    def process_request(self, request):
        if signup_settings.require_confirmation:
            if request.user.is_anonymous or request.user.is_staff:
                return None
            path_resolved = resolve(request.path_info)
            if len(path_resolved.namespaces) and path_resolved.namespaces[0] == 'staff':
                return None
            if path_resolved.url_name not in self.whitelisted_url_names:
                if not request.user.email_verified:
                    # NOTE: "emailNotVerified" is used by frontend to make sure the error is an email
                    # verification error
                    return JsonResponse({
                        'detail': _('Email verification is required to fulfill the request'),
                        'emailNotVerified': True
                    },
                        status=status.HTTP_428_PRECONDITION_REQUIRED
                    )
