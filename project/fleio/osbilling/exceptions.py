from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions as rest_exceptions
from rest_framework import status


class ResourceNotFound(rest_exceptions.APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_details = _('Resource not found')


class CollectorException(Exception):
    message = _('Collector exception')
