from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler
from kombu.exceptions import KombuError


class TaskException(APIException):
    status_code = 502


def drf_exception_handler(exc, context):
    """
    Base DRF exception handler that deals with other
    generic exceptions that DRF does not handle.
    """
    if isinstance(exc, KombuError):
        # handle Celery generic exceptions for staff and end user
        if context and 'request' in context and context['request'].user.is_staff:
            exc = TaskException(detail='{}'.format(exc))
        else:
            exc = TaskException(detail=_('Unable to execute task'))
    return exception_handler(exc=exc, context=context)
