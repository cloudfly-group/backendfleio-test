import logging
from os import path

from django.conf import settings
from django.contrib import auth
from django.contrib.auth.tokens import default_token_generator
from django.core import signing
from django.utils.translation import ugettext_lazy as _
from ipware.ip import get_ip
from rest_framework import exceptions, permissions, throttling, viewsets
from rest_framework.decorators import action, api_view, permission_classes, throttle_classes
from rest_framework.response import Response

from fleio.billing.client_operations import ClientOperations
from fleio.core import utils
from fleio.core.clients.serializers import ClientBriefSerializer
from fleio.core.exceptions import APIBadRequest, ForbiddenException, LicenseNotFoundUser
from fleio.core.features import active_features
from fleio.core.models import TermsOfService
from fleio.core.second_factor_auth.utils import process_login_with_sfa
from fleio.core.serializers import (LoginSerializer, PasswordResetSerializer,
                                    UpdateUserSerializer, UserSerializer)
from fleio.core.signup.settings import signup_settings
from fleio.core.signup.signup_token import signup_token_generator
from fleio.core.signup.utils import generate_verification_token_and_send
from fleio.core.tasks import send_reset_password_email
from fleio.core.terms_of_service.tos_settings import tos_settings
from fleio.notifications.models import DispatcherLog
from fleiostaff.core.signals import staff_confirmed_password, staff_forgot_password
from .drf import EndUserOnly
from .models import AppUser
from .signals import user_confirmed_password
from .signals import user_forgot_password
from .signals import user_log_in_failed_missing_license
from .signals import user_log_in_non_existent
from .signals import user_logged_out
from .signals import user_update
from .signals import user_update_password
from .utils import fleio_parse_url

LOG = logging.getLogger(__name__)

VERSION = {'backend_version': settings.FLEIO_BACKEND_VERSION,
           'backend_build': settings.FLEIO_BACKEND_BUILD,
           'latest_frontend_version': settings.FLEIO_LATEST_FRONTEND_VERSION,
           'latest_frontend_build': settings.FLEIO_LATEST_FRONTEND_BUILD}


class LoginRateThrottle(throttling.AnonRateThrottle):
    scope = 'login'


class PasswordResetRateThrottle(throttling.AnonRateThrottle):
    scope = 'password_reset'


class ConfirmEmailRateThrottle(throttling.UserRateThrottle):
    scope = 'confirm_email'


class ResendEmailVerificationRateThrottle(throttling.UserRateThrottle):
    scope = 'resend_email_verification'


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
@throttle_classes([LoginRateThrottle])
def login(request):
    try:
        if (not path.isfile('./fleio/core/loginview.so') and not path.isfile(
                './fleio/core/loginview.py') and not path.isfile('./fleio/core/loginview.pyd')) or \
                not path.isfile('./fleio/core/utils'):
            serializer = LoginSerializer(data={
                'username': request.data.get('username', ''),
                'password': request.data.get('password', ''),
                'remember_me': request.data.get('remember_me', False),
            })
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            UserModel = auth.get_user_model()
            try:
                matched_user = UserModel.objects.get(username=data['username'])
            except UserModel.DoesNotExist:
                user_log_in_non_existent.send(sender=__name__, username=data['username'], request=request)
            else:
                user_log_in_failed_missing_license.send(sender=__name__, user=matched_user,
                                                        username=matched_user.username,
                                                        user_id=matched_user.pk, email=matched_user.email,
                                                        request=request)
            raise LicenseNotFoundUser()
        from fleio.core.loginview import login
        try:
            sfa_completed, remember_sfa_token = process_login_with_sfa(request=request)
        except Exception as e:
            raise e
        response = login(request, sfa_completed=sfa_completed, remember_sfa_token=remember_sfa_token)
        response.data.update({'is_white_label': utils.is_white_label_license()})
        return response
    except ImportError:
        raise LicenseNotFoundUser()


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def logout(request):
    user = request.user

    if not request.user.is_authenticated:
        return Response(status=200)  # nothing should happen
    else:
        auth.logout(request)
        user_logged_out.send(sender=__name__, user=user, username=user.username, user_id=user.pk,
                             email=user.email, request=request)

    return Response({'detail': _('Logged out')})


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def current_user(request):
    if request.user.is_authenticated and not request.user.is_staff:
        requires_email_verification = (True if request.user.email_verified is False and
                                       signup_settings.require_confirmation is True else False)

        response_data = {
            'user': get_current_user_info(request.user),
            'impersonated': 'impersonate' in request.session,
            'requires_email_verification': requires_email_verification,
            'features': active_features.all,
            'notifications': DispatcherLog.objects.filter(
                notification__client__in=request.user.clients.all(),
                name='frontend',
                status='pending'
            ).count(),
            'version': VERSION,
            'is_white_label': utils.is_white_label_license()
        }

        reseller_resources = request.user.reseller_resources
        if reseller_resources:
            request_url = '//{}{}'.format(request.get_host(), request.path_info)
            reseller_api_url = request_url.replace('api/current-user', 'resellerapi')
            frontend_url = getattr(settings, 'RESELLER_FRONTEND_URL', None)
            if not frontend_url:
                frontend_url = getattr(settings, 'FRONTEND_URL', None)
            reseller_frontend_url = fleio_parse_url(frontend_url) + settings.RESELLER_FRONTEND_URL_ENDPOINT

            response_data['reseller_api_url'] = reseller_api_url
            response_data['reseller_frontend_url'] = reseller_frontend_url

        return Response(response_data)
    else:
        latest_tos = None
        if tos_settings.require_end_users_to_agree_with_latest_tos:
            latest_tos = TermsOfService.objects.filter(
                draft=False
            ).order_by('-version').first()  # take the latest version
        return Response({
            'features': active_features.all,
            'version': VERSION,
            'is_white_label': utils.is_white_label_license(),
            'requires_tos_agreement': latest_tos.id if latest_tos else None,
        })


def get_current_user_info(user):
    clients = ClientBriefSerializer(user.clients.all(), many=True)
    return {
        'id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'full_name': user.get_full_name(),
        'email': user.email,
        'language': user.language,
        'clients': clients.data,
    }


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
@throttle_classes([PasswordResetRateThrottle])
def password_reset(request):
    if not active_features.is_enabled('enduser.allow_changing_password'):
        raise exceptions.APIException(_('Changing password is disabled. Please contact support.'))
    password_reset_serializer = PasswordResetSerializer
    serializer = password_reset_serializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        user = serializer.validated_data['username_or_email']

        if user is None:
            return Response(status=200)  # even if no user is found we return 200 for security issues (brute-force att)
        else:
            send_reset_password_email.delay(user.pk)
            if user.is_staff:
                staff_forgot_password.send(sender=__name__, user=user, username=user.username, user_id=user.pk,
                                           email=user.email, request=request)
            else:
                user_forgot_password.send(sender=__name__, user=user, username=user.username, user_id=user.pk,
                                          email=user.email, request=request)
            return Response(status=200)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
@throttle_classes([PasswordResetRateThrottle])
def password_reset_confirm(request):
    """View that checks the hash in a password reset link"""
    not_able_msg = _('Password reset fail')
    password_mismatch_msg = _('Passwords do not match')

    user_id = request.data.get('user_id', None)
    token = request.data.get('token', None)
    new_password = request.data.get('new_password', None)
    confirm_password = request.data.get('confirm_password', None)

    if not user_id or not token or not new_password or not confirm_password:
        raise exceptions.ValidationError({'detail': not_able_msg})
    if new_password != confirm_password:
        raise exceptions.ValidationError({'detail': password_mismatch_msg})
    else:
        password_complexity_status = utils.check_password_complexity(confirm_password)
        if not password_complexity_status['password_ok']:
            error_list = [key for key, value in password_complexity_status.items() if value is True]
            raise exceptions.ValidationError(detail={'password': error_list})

    try:
        user = AppUser.objects.get(pk=user_id)
    except Exception as e:
        LOG.exception(e)
        raise exceptions.ValidationError({'detail': not_able_msg})

    if not default_token_generator.check_token(user, token):
        raise exceptions.ValidationError({'detail': _('Token expired or invalid. Try to reset the password again.')})

    # at this point all requirements are checked and validated so we save the new password
    user.set_password(confirm_password)
    user.save()
    if user.is_staff:
        staff_confirmed_password.send(sender=__name__, user=user, username=user.username, user_id=user.pk,
                                      email=user.email, request=request)
    else:
        user_confirmed_password.send(sender=__name__, user=user, username=user.username, user_id=user.pk,
                                     email=user.email, request=request)
    return Response(status=200)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
@throttle_classes([LoginRateThrottle])
def sso(request):
    user_model = auth.get_user_model()
    try:
        euid = signing.loads(s=request.data.get('hash_val'), salt=settings.SSO_SALT, max_age=settings.SSO_MAX_AGE)
        user = user_model.objects.get(external_billing_id=euid)
    except (signing.BadSignature, signing.SignatureExpired, user_model.DoesNotExist) as e:
        LOG.debug(e)
        raise exceptions.AuthenticationFailed(detail=_('Unable to authenticate'))

    if user.is_active:
        utils.login_without_password(request, user)
        request.session['ip'] = get_ip(request)
        return Response({'user': get_current_user_info(request.user),
                         'features': active_features.all})
    else:
        raise exceptions.AuthenticationFailed(detail=_('This account is inactive'))


@api_view(['POST'])
@permission_classes((EndUserOnly,))
@throttle_classes([ConfirmEmailRateThrottle])
def confirm_email_after_signup(request):
    token = request.data.get('token', None)
    user = request.user
    if not token:
        raise APIBadRequest(_('Confirmation token is missing'))
    if user.email_verified is True:
        raise APIBadRequest(_('The email associated with this account is already confirmed'))
    if signup_token_generator.check_token(user=user, token=token):
        user.email_verified = True
        user.save()
        return Response({'detail': _('Email successfully confirmed')})
    raise APIBadRequest(_('Token is invalid or no longer available'))


@api_view(['POST'])
@permission_classes([EndUserOnly])
@throttle_classes([ResendEmailVerificationRateThrottle])
def resend_email_confirmation_email_message(request):
    user = request.user
    if user.email_verified:
        raise APIBadRequest(_('The email associated with this account is already confirmed'))
    generate_verification_token_and_send(user=user)
    return Response({'detail': _('An email with the confirmation token was sent to {}').format(user.email)})


@api_view(['GET'])
@permission_classes([EndUserOnly])
def get_external_billing_url(request):
    client = request.user.clients.all().first()
    client_operations = ClientOperations(client=client)
    add_credit_url = client_operations.get_add_credit_url()
    if client.reseller_resources:
        frontend_url = client.reseller_resources.enduser_panel_url
    else:
        frontend_url = getattr(settings, 'FRONTEND_URL', '')
    if add_credit_url == frontend_url:
        add_credit_url = ''  # there is not external add credit url
    return Response({
        'external_billing_url': add_credit_url
    })


class UserProfileViewSet(viewsets.ViewSet):
    permission_classes = (EndUserOnly,)

    @staticmethod
    def list(request):
        """List user info."""
        user = request.user
        serializer = UserSerializer(user)
        requires_email_validation = (True if request.user.email_verified is False and
                                     signup_settings.require_confirmation is True else False)
        return Response({
            'user': serializer.data,
            'requires_email_validation': requires_email_validation,
        })

    def update(self, request, pk):
        serializer_context = {'request': request}
        serializer = UpdateUserSerializer(data=request.data, context=serializer_context)
        serializer.is_valid(raise_exception=True)
        user = request.user  # type: AppUser
        updated_user_fields = utils.get_user_changed_values(user, serializer.validated_data)
        log_text = utils.format_for_log(updated_user_fields)
        old_password = serializer.validated_data.get('old_password', None)
        password = serializer.validated_data.get('password', None)
        user.first_name = serializer.validated_data['first_name']
        user.last_name = serializer.validated_data['last_name']
        if 'mobile_phone_number' in serializer.validated_data:
            user.mobile_phone_number = serializer.validated_data.get('mobile_phone_number')

        new_email = False
        if user.email != serializer.validated_data['email']:
            user.email_verified = False
            new_email = True

        user.email = serializer.validated_data['email']
        language = serializer.validated_data.get('language')
        if language:
            user.language = language

        password_changed = False
        if password:
            if active_features.is_enabled('demo'):
                raise ForbiddenException(detail=_('Changing password not allowed in demo mode'))
            if not active_features.is_enabled('enduser.allow_changing_password'):
                raise APIBadRequest(_('Changing password is disabled. Please contact support.'))
            if user.check_password(old_password):
                user.set_password(password)
                utils.login_without_password(request, user)
                password_changed = True
            else:
                raise APIBadRequest(_('Please enter the correct current password.'))

        user.save()

        # send email verification notification
        confirmation_email_sent = False
        if signup_settings.require_confirmation and user.email_verified is False and new_email is True:
            generate_verification_token_and_send(user=user)
            confirmation_email_sent = True

        if password_changed:
            user_update_password.send(sender=__name__, user=user, username=user.username, user_id=user.pk,
                                      email=user.email, request=request)
        if updated_user_fields:
            user_update.send(sender=__name__, user=user, username=user.username, user_id=user.pk, email=user.email,
                             request=request, updated_data=log_text)

        serializer.save_component_data(instance=request.user)

        return Response({'detail': _('User profile updated'), 'confirmation_email_sent': confirmation_email_sent})

    @action(detail=False, methods=['get'])
    def create_options(self, request, *args, **kwargs):
        create_options = {'languages': settings.LANGUAGES}
        return Response(create_options)
