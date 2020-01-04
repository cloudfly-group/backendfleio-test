from django.utils.translation import ugettext_lazy as _

from rest_framework.exceptions import APIException
from rest_framework import status


class SFATypeNotFound(APIException):
    default_detail = _('Second factor authentication type was not found')
    status_code = status.HTTP_404_NOT_FOUND


class SFAMethodNotFound(APIException):
    default_detail = _('Requested second factor authentication method was not found')
    status_code = status.HTTP_404_NOT_FOUND


class SFAMethodNotEnabled(APIException):
    default_detail = _('Requested second factor authentication method was not enabled')
    status_code = status.HTTP_403_FORBIDDEN


class SFAMethodNotAdded(APIException):
    default_detail = _('Requested second factor authentication method was not added')
    status_code = status.HTTP_403_FORBIDDEN
