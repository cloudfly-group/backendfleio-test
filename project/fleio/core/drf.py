"""Collection of code used by our Django Rest Framework installation"""
import logging
from collections import OrderedDict

import six
from django.conf import settings
from django.core.paginator import InvalidPage
from django.utils.translation import ugettext_lazy as _
from pyvat import check_vat_number
from rest_framework import exceptions, fields, pagination, serializers
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.compat import unicode_http_header
from rest_framework.permissions import BasePermission
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.utils.mediatypes import _MediaType
from rest_framework.versioning import BaseVersioning
from stdnum.ch import uid as ch_uid
from stdnum.ch import vat as ch_vat

from fleio.reseller.utils import user_reseller_resources
from .operations import match_session_ip_or_401

LOG = logging.getLogger(__name__)


def validate_vat_id(vat_id, country_code: str = None) -> [bool, str]:
    if not country_code:
        return False, _('Did not receive country code')
    if country_code == 'CH':
        # validate Swiss business number, e.g. 'CHE-107.787.577'
        # or VAT ID number, which is the business number with  one of the suffixes:
        #   IVA, TVA, MWST, TPV, e.g. 'CHE-107.787.577 TVA'
        if ch_uid.is_valid(vat_id) or ch_vat.is_valid(vat_id):
            return True, _('Valid VAT ID')
        else:
            return False, _('Invalid VAT ID')
    elif country_code not in getattr(settings, 'EU_COUNTRIES'):
        return True, 'Non EU country'
    else:
        try:
            if country_code != vat_id[0:2]:
                return False, _('VAT ID country prefix do not match your selected country')
            if vat_id and not check_vat_number(vat_number=vat_id, country_code=country_code).is_valid:
                return False, _('Invalid VAT ID format')
            else:
                return True, _('Valid VAT ID')
        except Exception as e:
            LOG.debug(e)
            return False, _('Invalid VAT ID format')


class FakeFormBasedAuthentication(BaseAuthentication):
    """
    Form authentication against username/password.

    Mainly used to avoid the default browser popup that is shown on Basic authentication.
    Inspiration: http://stackoverflow.com/a/19102200

    WWW-Authenticate header is required by the standard on 401 HTTP code:
    http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html
    so we won't remove it but send header FormBased instead of Basic.
    """
    www_authenticate_realm = 'api'

    def authenticate(self, request):
        """
        It will always fail since this is a fake authentication.
        """
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != b'formbased':
            return None

        raise exceptions.AuthenticationFailed('Invalid username/password')

    def authenticate_header(self, request):
        return 'FormBased realm="%s"' % self.www_authenticate_realm


class StaffOnly(BasePermission):
    """
    Allows access only to users with is_staff flag set and raise 401 if flag is not set.
    """

    def has_permission(self, request, view):
        if request.user and request.user.is_staff:
            match_session_ip_or_401(request)
            return True
        else:
            raise exceptions.AuthenticationFailed()


class ResellerOnly(BasePermission):
    """
    Allows access only to users with is_reseller flag set and raise 401 if flag is not set.
    """

    def has_permission(self, request, view):
        if request.user and request.user.is_reseller:
            if user_reseller_resources(user=request.user):
                match_session_ip_or_401(request)
                return True

        raise exceptions.AuthenticationFailed()


class EndUserOnly(BasePermission):
    """
    Allows access only to end-users and raise 401 if user is admin(staff, superuser or reseller).
    """

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            match_session_ip_or_401(request)
            if request.user.is_admin:
                raise exceptions.AuthenticationFailed()
            else:
                return True
        else:
            return False


class SuperUserOnly(BasePermission):
    """
    Allows access only to users with is_superuser flag set and raise 401 if flag is not set.
    """

    def has_permission(self, request, view):
        if request.user and request.user.is_staff and request.user.is_superuser:
            match_session_ip_or_401(request)
            return True
        else:
            raise exceptions.AuthenticationFailed('Unauthorized: missing superuser status')


class CustomPermissions(BasePermission):
    """
    The CustomPermissions class allows dynamic registering of permission classes.
    A permission class is any class that has one/all of the two functions: has_permissions
        and has_object_permissions.
    Place this class in a view as a permission class where you want all dynamic
        permissions to take effect.
    """
    message = _('Unable to perform the requested action')
    has_permission_instances = tuple()
    has_object_permission_instances = tuple()

    @staticmethod
    def register(permission_class):
        """Register a permission class instance"""
        if hasattr(permission_class, 'has_permission') and callable(permission_class.has_permission):
            CustomPermissions.has_permission_instances += (permission_class,)
        elif hasattr(permission_class,
                     'has_object_permission') and callable(permission_class.has_object_permission):
            CustomPermissions.has_object_permission_instances += (permission_class,)

    @staticmethod
    def unregister(permission_class):
        """Unregister an instance of a permission class"""
        cp = CustomPermissions
        cp.has_permission_instances = (c for c in cp.has_permission_instances if c != permission_class)
        cp.has_object_permission_instances = (c for c in cp.has_object_permission_instances if c != permission_class)

    def has_permission(self, request, view):
        """Call has_permission on all registered classes"""
        for cls in CustomPermissions.has_permission_instances:
            if not cls.has_permission(request, view):
                self.message = _('Unable to perform the requested action')
                if hasattr(cls, 'message'):
                    self.message = cls.message
                return False
        return True

    def has_object_permission(self, request, view, obj):
        """Call has_permission on all registered classes"""
        for cls in CustomPermissions.has_object_permission_instances:
            if not cls.has_object_permission(request, view, obj):
                self.message = _('Unable to perform the requested action')
                if hasattr(cls, 'message'):
                    self.message = cls.message
                return False
        return True


class FleioPaginationSerializer(pagination.PageNumberPagination):
    page_size_query_param = 'page_size'  # Allow client to override, using `?page_size=xxx`.
    max_page_size = 10000  # Maximum limit allowed when using `?page_size=xxx`.

    def paginate_queryset(self, queryset, request, view=None):
        page_size = self.get_page_size(request)
        if not page_size:
            return None

        if not getattr(queryset, 'ordered', True):
            LOG.debug('Unordered query set for view {}, ordering descending by pk'.format(type(view).__name__))
            queryset = queryset.order_by('-pk')
        paginator = self.django_paginator_class(queryset, page_size)
        page_number = request.query_params.get(self.page_query_param, 1)
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages

        try:
            self.page = paginator.page(page_number)
        except InvalidPage as exc:
            msg = self.invalid_page_message.format(
                page_number=page_number, message=six.text_type(exc)
            )
            raise exceptions.NotFound(msg)

        if paginator.num_pages > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True
        self.request = request
        self.total_count = len(queryset)
        self.page_no = page_number
        return list(self.page)

    # NOTE(tomo): We change the 'results' field name to 'objects'
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('objects', data),
            ('totalCount', self.total_count),
            ('pageNo', self.page_no)
        ]))


class FleioJsonRenderer(JSONRenderer):
    media_type = 'application/vnd.fleio.api+json'


class FleioVersioning(BaseVersioning):
    """
    Combine NamespaceVersioning with AcceptHeaderVersioning.
    If conflicting versions are specified using both an HTTP header and a URI, the URI takes precedence.
    """
    invalid_uri_version_message = _('Invalid version in URL path')
    invalid_headers_version_message = _('Invalid version in "Accept" header')

    def determine_headers_version(self, request, *args, **kwargs):
        media_type = _MediaType(request.accepted_media_type)
        version = media_type.params.get(self.version_param, self.default_version)
        version = unicode_http_header(version)
        if not self.is_allowed_version(version):
            raise exceptions.NotAcceptable(self.invalid_headers_version_message)
        return version

    def determine_version(self, request, *args, **kwargs):
        resolver_match = getattr(request, 'resolver_match', None)
        if resolver_match is None or not resolver_match.namespace:
            return self.determine_headers_version(request, *args, **kwargs)
        version = resolver_match.namespace
        if not self.is_allowed_version(version):
            raise exceptions.NotFound(self.invalid_uri_version_message)
        return version

    def reverse(self, viewname, args=None, kwargs=None, request=None, format=None, **extra):
        resolver_match = getattr(request, 'resolver_match', None)
        if request.version is not None and resolver_match is not None:
            viewname = self.get_versioned_viewname(viewname, request)
        return super(FleioVersioning, self).reverse(viewname, args, kwargs, request, format, **extra)

    def get_versioned_viewname(self, viewname, request):
        return request.version + ':' + viewname


class FieldsModelSerializer(serializers.ModelSerializer):
    """
    A model serializer that accepts a fields variable
    to dynamically determine the fields to show
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(FieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class FlChoiceField(serializers.Field):
    default_error_messages = {
        'invalid_choice': _('"{input}" is not a valid choice.')
    }
    html_cutoff = None
    html_cutoff_text = _('More than {count} items...')

    def __init__(self, choices, **kwargs):
        self.choices = choices
        self.html_cutoff = kwargs.pop('html_cutoff', self.html_cutoff)
        self.html_cutoff_text = kwargs.pop('html_cutoff_text', self.html_cutoff_text)
        self.allow_blank = kwargs.pop('allow_blank', False)
        super(FlChoiceField, self).__init__(**kwargs)

    def init_choices(self, initial_choices):
        if callable(initial_choices):
            return initial_choices()
        else:
            return initial_choices

    @property
    def grouped_choices(self):
        choices = self.init_choices(self.choices)
        return fields.to_choices_dict(choices)

    @property
    def dict_choices(self):
        choices = fields.flatten_choices_dict(self.grouped_choices)
        return {six.text_type(key): key for key in choices}

    def to_internal_value(self, data):
        if data == '' and self.allow_blank:
            return ''

        try:
            return self.dict_choices[six.text_type(data)]
        except KeyError:
            self.fail('invalid_choice', input=data)

    def to_representation(self, value):
        if value in ('', None):
            return value
        return self.dict_choices.get(six.text_type(value), value)

    def iter_options(self):
        """
        Helper method for use with templates rendering select widgets.
        """
        return fields.iter_options(
            self.grouped_choices,
            cutoff=self.html_cutoff,
            cutoff_text=self.html_cutoff_text
        )
