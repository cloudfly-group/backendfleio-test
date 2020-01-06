from django.urls import resolve
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from django.utils.translation import ugettext_lazy as _
from rest_framework import status

from fleio.core.models import SecondFactorAuthMethod, SecondFactorAuthType
from fleio.core.second_factor_auth.sfasettings import sfa_settings


class CheckSFAMiddleware(MiddlewareMixin):
    """Make sure the current user uses second factor authentication if settings make it required"""
    whitelisted_url_names = ('current-user', 'login', 'dynamic-ui-custom-menu-links', 'resend-email-confirmation',
                             'userprofile-create-options', 'userprofile-detail', 'userprofile-list',
                             'plugins-plugins-with-component', 'plugins-plugins-with-notifications',
                             'client-list', 'client-create-options', 'logout', 'reset-password',
                             'reset-password-confirm', 'email-sign-up-confirmation', 'dynamic-ui-plugin-data',
                             'tickets-get-current-user-tickets-count', 'get-external-billing-url',
                             'todo-get-current-user-todo-count', 'termsofserviceagreements-agree',
                             'termsofserviceagreements-list', 'termsofserviceagreements-detail',
                             'termsofserviceagreements-get-active-tos')

    def process_request(self, request):
        if request.user.is_anonymous:
            return None
        elif request.user.is_staff:
            sfa_required = sfa_settings.require_staff_users_to_use_sfa
            enabled_query_param = 'enabled_to_staff'
        else:
            sfa_required = sfa_settings.require_end_users_to_use_sfa
            enabled_query_param = 'enabled_to_enduser'
        if sfa_required:
            sfa_enabled_methods = SecondFactorAuthMethod.objects.filter(user=request.user, enabled=True)
            if sfa_enabled_methods.count() > 0:
                # if it has a sfa method enabled, stop
                return None
            path_resolved = resolve(request.path_info)
            # make sure urls related to sfa types are accessible
            names = []
            for sfa_type in SecondFactorAuthType.objects.filter(**{enabled_query_param: True}):
                names.append(sfa_type.name)
            do_not_allow = (path_resolved.url_name not in self.whitelisted_url_names and
                            'sfa' not in path_resolved.url_name)
            for name in names:
                if name in path_resolved.url_name:
                    do_not_allow = False
                    break
            if do_not_allow:
                # NOTE: "sfaNotSet" is used by frontend to make sure the error is related to sfa
                return JsonResponse({
                    'detail': _('You must enable second factor authentication for your account'),
                    'sfaNotSet': True
                }, status=status.HTTP_428_PRECONDITION_REQUIRED)
        return None
