from django.http import JsonResponse
from django.utils.translation import ugettext_lazy as _
from django.utils.deprecation import MiddlewareMixin
from django.utils.encoding import force_text
from rest_framework import status
from fleio.conf.exceptions import ConfigException


class ConfigurationErrorMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        if isinstance(exception, ConfigException) and request.user:
            if request.user.is_staff:
                return JsonResponse({'detail': force_text(exception),
                                     'section': exception.section,
                                     'configuration_id': exception.configuration_id},
                                    status=status.HTTP_412_PRECONDITION_FAILED)
            else:
                return JsonResponse({'detail': _('Configuration error. Contact support.')},
                                    status=status.HTTP_412_PRECONDITION_FAILED)
