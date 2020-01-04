from django.urls import resolve
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from django.utils.translation import ugettext_lazy as _
from rest_framework import status

from fleio.reseller.utils import user_reseller_resources


class CheckClientsMiddleware(MiddlewareMixin):
    """Make sure the current user has a Client associated"""
    whitelisted_url_names = ('current-user', 'login', 'client-create-options', 'dynamic-ui-custom-menu-links',
                             'userprofile-create-options', 'userprofile-detail', 'userprofile-list',
                             'plugins-plugins-with-component', 'plugins-plugins-with-notifications',
                             'dynamic-ui-plugin-data', 'client-list', 'publickeys-list', 'publickeys-detail',
                             'resend-email-confirmation', 'logout', 'reset-password', 'reset-password-confirm',
                             'email-sign-up-confirmation', 'tickets-get-current-user-tickets-count', )

    def process_request(self, request):
        if request.user.is_anonymous or request.user.is_staff:
            return None
        path_resolved = resolve(request.path_info)
        if len(path_resolved.namespaces) and path_resolved.namespaces[0] == 'staff':
            return None
        if path_resolved.url_name not in self.whitelisted_url_names:
            if request.user.clients.count() == 0:
                # NOTE(tomo): "clientRequired" is used by frontend to make sure the error is a client required error
                return JsonResponse({'detail': _('Client billing information is required to fulfill the request'),
                                     'clientRequired': True},
                                    status=status.HTTP_428_PRECONDITION_REQUIRED)
            if request.user.is_reseller and (request.method == 'POST' or request.method == 'DELETE' or
                                             request.method == 'PUT' or request.method == 'PATCH'):
                # if user is a reseller and his client is suspended do not allow him to do any important action
                reseller_resources = user_reseller_resources(user=request.user)
                if reseller_resources.service and not reseller_resources.service.is_active():
                    return JsonResponse({
                        'detail': _('Your client is suspended.')
                    }, status=status.HTTP_403_FORBIDDEN)
