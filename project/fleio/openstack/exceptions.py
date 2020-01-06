from __future__ import unicode_literals

import sys

import requests
from cinderclient import exceptions as cinderclient
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text
from keystoneauth1 import exceptions as keystoneclient
from neutronclient.common import exceptions as neutronclient
from novaclient import exceptions as novaclient
from glanceclient import exc as glanceclient
from rest_framework import exceptions as rest_exceptions
from rest_framework import status

NOT_FOUND = (novaclient.NotFound,
             neutronclient.NotFound,
             cinderclient.NotFound
             )

UNAUTHORIZED = (novaclient.Unauthorized,
                neutronclient.Unauthorized,
                cinderclient.Unauthorized,
                keystoneclient.http.Unauthorized
                )

RECOVERABLE = (novaclient.ClientException,
               novaclient.Forbidden,
               neutronclient.NeutronClientException,
               neutronclient.Forbidden,
               cinderclient.BadRequest,
               cinderclient.ClientException,
               glanceclient.HTTPForbidden
               )

CONNECTION = (keystoneclient.ConnectFailure,
              keystoneclient.ConnectionError,
              keystoneclient.ConnectTimeout,
              keystoneclient.discovery.DiscoveryFailure,
              neutronclient.ConnectionFailed,
              cinderclient.ConnectionError,
              keystoneclient.catalog.EndpointNotFound,
              )


def check_locked(exc_value):
    """Dirty way of checking if an instance is locked."""
    if hasattr(exc_value, 'message') and exc_value.message.endswith(' is locked'):
        return True
    return False


def check_protected(exc_value):
    """Dirty way of checking if an image is protected."""
    if hasattr(exc_value, 'message') and exc_value.message.endswith(' is protected'):
        return True
    return False


def handle(request, message=None):
    # FIXME(tomo): Better error handling!! message is also an exception class, not always a message
    exc_type, exc_value, exc_traceback = sys.exc_info()
    # trying to get the status of the exception, if all else fails default to 500
    if message:
        message = force_text(message)  # NOTE(tomo): just in case message is an exception
    if request.user and request.user.is_staff and not isinstance(message, Exception):
        # NOTE(tomo): Add exc_value to the exception if the user is staff and message is not the exception
        message = '{} {}'.format(message, force_text(exc_value)) if message else force_text(exc_value)
    # Set the response http status code based on what OpenStack sends us
    http_status = (getattr(exc_type, 'http_status', None) or
                   getattr(exc_value, 'status_code', None) or
                   getattr(exc_value, 'code', None) or
                   getattr(exc_type, 'status_code', None) or
                   requests.codes.get('internal_server_error'))
    if issubclass(exc_type, UNAUTHORIZED):
        raise OpenstackAuthError(detail=message)
    elif issubclass(exc_type, CONNECTION):
        raise OpenstackTimeout(detail=message)
    else:
        api_exc = rest_exceptions.APIException(detail=message)

    api_exc.status_code = http_status
    if issubclass(exc_type, NOT_FOUND) or issubclass(exc_type, RECOVERABLE):
        # TODO(tomo): Remove this once locking state can be queried via the OS API.
        if check_locked(exc_value):
            api_exc.detail = _('The instance is locked')
        elif check_protected(exc_value):
            api_exc.detail = _('The image is protected')
        else:
            api_exc.detail = message

    else:
        # TODO(adrian): translation just does work here, regardless if it's lazy or not
        if message:
            api_exc.detail = message
        else:
            api_exc.detail = _('An unexpected error occurred')
    # TODO(tomo): Handle unknown exceptions by using a generic message and APIException
    # six.reraise(exc_type, exc_value, exc_traceback)
    raise api_exc


class APIException(rest_exceptions.APIException):
    default_detail = _('Unable to perform the requested operation')


class APIBadRequest(rest_exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Bad request')


class APIConflict(rest_exceptions.APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = _('Unable to perform the requested operation')


class ObjectNotFound(rest_exceptions.APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = _('A required object was not found')


class ForbiddenException(rest_exceptions.PermissionDenied):
    pass


class ConfigurationError(rest_exceptions.APIException):
    status_code = status.HTTP_412_PRECONDITION_FAILED
    default_detail = _('Configuration missing')


class OpenstackTimeout(rest_exceptions.APIException):
    status_code = status.HTTP_504_GATEWAY_TIMEOUT
    default_detail = _('Can not connect to service api')


class OpenstackAuthError(rest_exceptions.APIException):
    status_code = status.HTTP_417_EXPECTATION_FAILED
    default_detail = _('OpenStack authentication failed')


class UnavailableException(rest_exceptions.APIException):
    status_code = status.HTTP_417_EXPECTATION_FAILED
    default_detail = _('Object not available')
