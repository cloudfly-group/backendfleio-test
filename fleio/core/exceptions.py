from typing import Optional

from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions as rest_exceptions
from rest_framework import status


class APIBadRequest(rest_exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Unable to perform the requested operation')


# NOTE: License error will be used by the binary license file generated in license server, do not delete
class LicenseError(rest_exceptions.APIException):
    status_code = status.HTTP_402_PAYMENT_REQUIRED
    default_detail = _('You must activate the software using a license key')


# NOTE: License error will be used by the binary license file generated in license server, do not delete
class LicenseNotFound(LicenseError):
    default_detail = _('You must activate the software using a license key')


# NOTE: License error will be used by the binary license file generated in license server, do not delete
class LicenseNotFoundUser(LicenseError):
    default_detail = _('Login not allowed. Please contact support')


# NOTE: License error will be used by the binary license file generated in license server, do not delete
class LicenseInvalid(LicenseError):
    default_detail = _('License is invalid')

    def __init__(self, message: Optional[str] = None):
        if message:
            self.message = message
        else:
            self.message = LicenseInvalid.default_detail


class ForbiddenException(rest_exceptions.APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = _('Cannot get or create token for inactive user')


class ObjectNotFound(rest_exceptions.APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = _('A required object was not found')


class APIConflict(rest_exceptions.APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = _('Unable to perform the requested operation')


class ConfigurationError(rest_exceptions.APIException):
    # TODO(adrian): Is it ok to through 500? There are about 26 places in the code that are using this class.
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = _('An unexpected error prevented the server from fulfilling your request')


class ServiceUnavailable(rest_exceptions.APIException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = _('Could not connect')


class InvalidSSL(rest_exceptions.APIException):
    status_code = 526
    default_detail = _('Invalid SSL certificate on OpenStack identity service')
