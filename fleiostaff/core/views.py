import fcntl
import json
import logging
import sys
import types
from collections import OrderedDict
from datetime import date, timedelta

import pycountry
import requests
from django.conf import settings
from django.contrib import auth
from django.core import signing
from django.db import IntegrityError
from django.db.models.deletion import ProtectedError
from django.urls import clear_url_caches
from django.utils.translation import ugettext_lazy as _
from ipware.ip import get_ip
from rest_framework import exceptions as rest_exceptions, viewsets
from rest_framework import permissions, serializers, throttling
from rest_framework import status as rest_status
from rest_framework.decorators import action, api_view, permission_classes, throttle_classes
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from fleio.billing.exchange_rate_manager import ExchangeRateManager
from fleio.celery import app as celery
from fleio.conf.models import Option
from fleio.conf.utils import fernet_decrypt, fernet_encrypt
from fleio.core import utils
from fleio.core.drf import StaffOnly
from fleio.core.exceptions import APIBadRequest, ForbiddenException, LicenseNotFound, ObjectNotFound, ServiceUnavailable
from fleio.core.features import staff_active_features
from fleio.core.models import AppStatus, AppUser
from fleio.core.models import Currency
from fleio.core.models.appstatus import StatusTypesMap
from fleio.core.second_factor_auth.utils import check_sfa_required_and_get_settings, process_login_with_sfa
from fleio.core.serializers import CurrencySerializer, LoginSerializer
from fleio.core.signals import user_update, user_update_password
from fleio.core.utils import is_white_label_license
from fleio.notifications.models import DispatcherLog
from fleiostaff.core.serializers import StaffUpdateUserProfileSerializer
from fleiostaff.core.serializers import StaffUserProfileSerializer
from .licensing import extract_license, get_current_cores, get_license_file
from .signals import (staff_log_in_failed, staff_log_in_inactive, staff_log_in_non_existent, staff_logged_in,
                      staff_logged_out, user_log_in_denied)

VERSION = {'backend_version': settings.FLEIO_BACKEND_VERSION,
           'backend_build': settings.FLEIO_BACKEND_BUILD,
           'latest_frontend_version': settings.FLEIO_LATEST_FRONTEND_VERSION,
           'latest_frontend_build': settings.FLEIO_LATEST_FRONTEND_BUILD}

LOG = logging.getLogger(__name__)


class LicenseKeySerializer(serializers.Serializer):
    license_key = serializers.CharField(max_length=255)

    def validate_license_key(self, data):
        if not staff_active_features.is_enabled('demo'):
            return data
        else:
            raise ValidationError(_('License key cannot be changed in demo mode'))


class LoginRateThrottle(throttling.AnonRateThrottle):
    scope = 'login'


@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def set_license(request):
    """Wrapper view for _set_license."""
    serializer = LicenseKeySerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    license_key = serializer.validated_data['license_key']

    try:
        response, status = _set_license(license_key)
        return Response({'detail': response}, status=status)
    except requests.ConnectionError:
        raise ServiceUnavailable(detail=_('Can\'t connect to server. '
                                          'Please check your internet connection and retry.'))


@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def refresh_license(request):
    try:
        key = Option.objects.get(section='LICENSE', field='key')
        license_key = fernet_decrypt(key.value)
    except Option.DoesNotExist as e:
        LOG.error(e)
        raise ObjectNotFound(detail=_('License not found'))
    else:
        try:
            response, status = _set_license(license_key)
            return Response({'detail': response}, status=status)
        except requests.ConnectionError as e:
            LOG.error(e)
            raise ServiceUnavailable(detail=_('Can\'t connect to server. '
                                              'Please check your internet connection and retry.'))


def list_urls(url_list, li, max_depth, depth=0):
    for entry in url_list:
        if hasattr(entry, 'urlconf_name') and isinstance(entry.urlconf_name, types.ModuleType):
            li.append((entry.urlconf_name, depth))
            if max_depth[0] < depth:
                del max_depth[0]
                max_depth.append(depth)
        if hasattr(entry, 'url_patterns'):
            list_urls(entry.url_patterns, li, max_depth, depth + 1)


def reload_non_uwsgi_server():
    """Reload urls in a non uwsgi server"""
    from importlib import reload

    # reloading urls must be done in this order
    from fleio.core import loginview
    # NOTE: this can give a RemovedInDjango20Warning in python 2
    reload(loginview)

    li = list()
    depth = [0]
    if settings.ROOT_URLCONF in sys.modules:
        list_urls(sys.modules[settings.ROOT_URLCONF].urlpatterns, li, depth)

    # reload urls from the innermost to the outermost url configuration
    for i in range(depth[0], -1, -1):
        [reload(li_elem[0]) for li_elem in li if li_elem[1] == i]

    # reload the main url module
    if settings.ROOT_URLCONF in sys.modules:
        reload(sys.modules[settings.ROOT_URLCONF])

    clear_url_caches()


def reload_uwsgi():
    try:
        import uwsgi
    except ImportError:
        return False
    else:
        uwsgi.reload()
        return True


def _set_license(license_key, path='.'):
    """Install license"""
    # get license
    response = get_license_file(license_key)
    if response.status_code != rest_status.HTTP_200_OK:
        return response.content, response.status_code
    # save/update key in db
    Option.objects.update_or_create(section='LICENSE', field='key', defaults={'value': fernet_encrypt(license_key)})
    # extract
    extract_license(response, path)
    # reload server
    if not reload_uwsgi():
        reload_non_uwsgi_server()
    return 'Ok', rest_status.HTTP_200_OK


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
@throttle_classes([LoginRateThrottle])
def login(request):
    serializer = LoginSerializer(data={
        'username': request.data.get('username', ''),
        'password': request.data.get('password', ''),
        'remember_me': request.data.get('remember_me', False),
    })
    serializer.is_valid(raise_exception=True)

    data = serializer.validated_data

    user = auth.authenticate(username=data['username'], password=data['password'])

    ip = get_ip(request)

    if user is None or not user.is_staff:
        if user is None:
            UserModel = auth.get_user_model()
            try:
                matched_user = UserModel.objects.get(username=data['username'])
            except UserModel.DoesNotExist:
                staff_log_in_non_existent.send(sender=__name__, username=data['username'], request=request)
            else:
                if matched_user.is_staff:
                    staff_log_in_failed.send(sender=__name__, user=matched_user, user_id=matched_user.pk,
                                             username=data['username'], email=matched_user.email, request=request)
                else:
                    user_log_in_denied.send(sender=__name__, user=matched_user, user_id=matched_user.pk,
                                            username=data['username'], email=matched_user.email, request=request)
        elif not user.is_staff:
            user_log_in_denied.send(sender=__name__, user=user, user_id=user.pk, username=user.username,
                                    email=user.email, request=request)
        raise rest_exceptions.AuthenticationFailed(detail=_('Incorrect user name or password'))
    elif not user.is_active:
        staff_log_in_inactive.send(sender=__name__, user=user, username=user.username, user_id=user.pk,
                                   email=user.email, request=request)
        raise rest_exceptions.AuthenticationFailed(detail=_('This account is inactive'))
    else:
        try:
            sfa_completed, remember_sfa_token = process_login_with_sfa(request=request)
        except Exception as e:
            raise e
        if not sfa_completed:
            sfa_required, response = check_sfa_required_and_get_settings(user=user)
            if sfa_required:
                return response
        auth.login(request, user)
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
        if data['remember_me']:
            request.session.set_expiry(2 * 365 * 30 * 24 * 60 * 60)  # two years
        else:
            request.session.set_expiry(0)
        request.session['ip'] = ip
        staff_logged_in.send(sender=__name__, user=user, user_id=user.pk, username=user.username,
                             email=user.email, request=request)
        response_dict = {
            'user': get_current_user_info(request.user),
            'features': staff_active_features.all,
            'version': VERSION,
            'is_white_label': is_white_label_license()
        }
        if remember_sfa_token:
            response_dict['remember_sfa_token'] = remember_sfa_token
        return Response(response_dict)


def get_current_user_info(user: AppUser):
    return {
        'id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'full_name': user.get_full_name(),
        'email': user.email,
        'language': user.language,
        'is_superuser': user.is_superuser,
    }


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def current_user(request):
    if request.user.is_authenticated and request.user.is_staff:
        response = {
            'user': get_current_user_info(request.user),
            'features': staff_active_features.all,
            'notifications': DispatcherLog.objects.filter(
                notification__user=request.user,
                name='frontend',
                status='pending',
            ).count(),
            'version': VERSION,
            'is_white_label': is_white_label_license()
        }

        try:
            if settings.LICENSE_EXPIRY_DATE - timedelta(days=settings.LICENSE_WARNING_DAYS) <= date.today():
                response['user']['license_expiring'] = dict()
                response['user']['license_expiring']['warning_days'] = (
                    settings.LICENSE_EXPIRY_DATE - date.today()).days
                if settings.LICENSE_WARNING_DAYS // 2 >= response['user']['license_expiring']['warning_days']:
                    response['user']['license_expiring']['warning_level'] = 2
                else:
                    response['user']['license_expiring']['warning_level'] = 1
            if settings.CORES_IN_USE > settings.MAX_CORES:
                response['user']['cores_exceeded'] = dict()
                response['user']['cores_exceeded']['max_cores'] = settings.MAX_CORES
                response['user']['cores_exceeded']['cores_in_use'] = settings.CORES_IN_USE
                response['user']['cores_exceeded']['grace_days'] = settings.CORE_GRACE_DAYS
        except (TypeError, AttributeError):
            pass
        return Response(response)
    else:
        return Response({'features': staff_active_features.all,
                         'version': VERSION,
                         'is_white_label': is_white_label_license()})


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def logout(request):
    user = request.user

    if not user.is_authenticated:
        return Response(status=200)  # nothing should happen
    else:
        auth.logout(request)
        staff_logged_out.send(sender=__name__, user=user, username=user.username, user_id=user.pk,
                              email=user.email, request=request)

    return Response({'detail': _('Logged out')})


@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def get_sso_session(request):
    euid = request.data.get('euid')
    if euid is None:
        raise rest_exceptions.ValidationError({'detail': _('euid required')})
    auth_user_model = auth.get_user_model()
    try:
        auth_user_model.objects.get(external_billing_id=euid)
    except auth_user_model.DoesNotExist:
        raise rest_exceptions.NotFound(detail=_('User does not exist'))
    return Response({'hash_val': signing.dumps(obj=euid, salt=settings.SSO_SALT)},
                    status=rest_status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def get_license_info(request):
    """Get general info about license"""
    try:
        from fleio.core.loginview import get_license_info
        license_dict = json.loads(get_license_info(), object_pairs_hook=OrderedDict)
        license_dict.pop('License key', None)

        if 0 == license_dict.get('Maximum clients', -1):
            del license_dict['Maximum clients']
        if 0 == license_dict.get('Maximum services', -1):
            del license_dict['Maximum services']
        if 0 == license_dict.get('Maximum cloud objects', -1):
            del license_dict['Maximum cloud objects']

        try:
            license_dict['Cores used'] = get_current_cores()
        except APIException:
            license_dict['Cores used'] = _('Unknown')
        return Response(license_dict)
    except ImportError:
        raise LicenseNotFound()
    except Exception:
        return Response()


class StaffUserProfileViewSet(viewsets.ViewSet):
    permission_classes = (StaffOnly,)

    @staticmethod
    def list(request):
        """List user info."""
        user = request.user
        serializer = StaffUserProfileSerializer(user)
        return Response({'user': serializer.data})

    @staticmethod
    def allowed_to_update(user):
        if user.is_superuser is True and staff_active_features.is_enabled('demo'):
            raise ForbiddenException(detail=_('Operation not allowed in demo mode'))

    def update(self, request, pk):
        serializer_context = {'request': request}
        serializer = StaffUpdateUserProfileSerializer(data=request.data, context=serializer_context)
        serializer.is_valid(raise_exception=True)
        user = request.user  # type: AppUser
        updated_user_fields = utils.get_user_changed_values(user, serializer.validated_data)
        log_text = utils.format_for_log(updated_user_fields)
        password = serializer.validated_data.get('password', None)
        old_password = serializer.validated_data.get('old_password', None)
        user.first_name = serializer.validated_data['first_name']
        user.last_name = serializer.validated_data['last_name']
        user.email = serializer.validated_data['email']
        language = serializer.validated_data.get('language')
        if language:
            user.language = language
        if 'mobile_phone_number' in serializer.validated_data:
            user.mobile_phone_number = serializer.validated_data.get('mobile_phone_number')

        self.allowed_to_update(user)

        password_changed = False
        if password and not staff_active_features.is_enabled('demo'):
            if user.check_password(old_password):
                user.set_password(password)
                utils.login_without_password(request, user)
                password_changed = True
            else:
                raise APIBadRequest(_('Please enter the correct current password.'))

        user.save()

        if password_changed:
            user_update_password.send(sender=__name__, user=user, username=user.username, user_id=user.pk,
                                      email=user.email, request=request)
        if updated_user_fields:
            user_update.send(sender=__name__, user=user, username=user.username, user_id=user.pk, email=user.email,
                             request=request, updated_data=log_text)

        return Response({'detail': _('User profile updated')})

    @action(detail=False, methods=['get'])
    def create_options(self, request, *args, **kwargs):
        del request, args, kwargs  # unused
        create_options = {'languages': settings.LANGUAGES}
        return Response(create_options)


class CurrencyViewSet(viewsets.ModelViewSet):
    serializer_class = CurrencySerializer
    permission_classes = (StaffOnly,)
    http_method_names = ['delete', 'get', 'post', 'put']
    ordering = ['code']

    def get_queryset(self):
        return Currency.objects.all()

    def perform_destroy(self, instance):
        if instance.is_default:
            raise ForbiddenException({'detail': 'Cannot delete the default currency'})
        try:
            instance.delete()
        except ProtectedError as e:
            raise APIBadRequest(detail={
                'error_type': 'ProtectedError',
                'detail': e,
                'user_friendly_message': _('Currency cannot be deleted because it is used by other objects')
            })
        except IntegrityError as e:
            raise APIBadRequest(detail=e.args[1])

    def perform_update(self, serializer: Serializer):
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data['is_default']:
            # default may change
            previous_instance = self.get_object()  # Currency
            if not previous_instance.is_default:
                # default currency is changing, adjusting exchange rates
                rate_to_old_default = previous_instance.rate
                for currency in Currency.objects.all():
                    currency.rate = currency.rate / rate_to_old_default
                    currency.is_default = currency.code == previous_instance.code
                    currency.save()
        else:
            super().perform_update(serializer)

    @action(detail=False, methods=['get'])
    def create_options(self, request):
        del request  # unused
        return Response({'codes': [i.alpha_3 for i in pycountry.currencies]})

    @action(detail=False, methods=['POST'])
    def update_relative_prices(self, request):
        del request  # unused
        ExchangeRateManager.update_relative_prices()
        return Response()

    @action(detail=False, methods=['POST'])
    def update_exchange_rates(self, request):
        del request  # unused
        ExchangeRateManager.update_exchange_rates()
        return Response()


@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def get_services_statuses(request):
    celery_active = False
    if getattr(settings, 'CELERY_TASK_ALWAYS_EAGER', False) is True:
        celery_active = True
    else:
        celery_workers = celery.control.inspect().active()  # gets celery workers
        celery_workers_list = celery_workers.keys() if celery_workers else None
        if celery_workers_list and len(celery_workers_list) > 0:
            celery_active = True

    response_dict = OrderedDict([
        ('celery', celery_active),
    ])

    # check updated status
    if staff_active_features.is_enabled('openstack'):
        with open(getattr(settings, 'UPDATED_LOCK_FILE', '/var/fleio/updated_lock.pid'), 'a+') as fp:
            try:
                fcntl.flock(fp.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except IOError:
                # file is locked, updated is running
                updated = True
            else:
                # file is not locked, updated is not running
                fcntl.flock(fp.fileno(), fcntl.F_UNLCK)
                updated = False
        response_dict['updated'] = updated
    return Response(response_dict)


@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def get_app_status(request):
    if staff_active_features.is_enabled('openstack'):
        updated_info = AppStatus.objects.filter(status_type=StatusTypesMap.updated_messages_count).first()
    else:
        updated_info = None
    if updated_info:
        return Response({
            'updated_info_details': updated_info.details_as_dict,
            'updated_info_last_updated': updated_info.last_updated,
        })
    return Response(dict())
