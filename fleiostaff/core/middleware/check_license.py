from os import path

from django.contrib import auth
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from django.utils.translation import ugettext_lazy as _
from rest_framework import status


class CheckLicenseMiddleware(MiddlewareMixin):
    """Check the license and redirect to the set license view"""
    def process_request(self, request):
        excluded_urls = [
            reverse('staff:set-license'),
            reverse('staff:current-user'),
            reverse('staff:login'),
            reverse('staff:logout'),
        ]

        if request.user and request.user.is_authenticated:
            if (not path.isfile('./fleio/core/loginview.so') and not path.isfile(
                    './fleio/core/loginview.py') and not path.isfile('./fleio/core/loginview.pyd')) or \
                    not path.isfile('./fleio/core/utils'):
                if request.user.is_staff:
                    if request.path_info not in excluded_urls:
                        return JsonResponse({'detail': _('License not found')},
                                            status=status.HTTP_402_PAYMENT_REQUIRED)
                else:
                    auth.logout(request)
                    return JsonResponse({'detail': _('Please contact support')},
                                        status=status.HTTP_402_PAYMENT_REQUIRED)
        return None
