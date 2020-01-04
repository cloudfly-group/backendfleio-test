import logging

from django.conf import settings
from django.contrib import auth

from django.utils.translation import ugettext_lazy as _

from ipware.ip import get_ip
from rest_framework import permissions, throttling
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.exceptions import AuthenticationFailed

from fleio.core.features import reseller_active_features
from fleio.core.models import AppUser
from fleio.core.serializers import LoginSerializer

from fleio.core.second_factor_auth.utils import check_sfa_required_and_get_settings, process_login_with_sfa
from fleio.core.utils import is_white_label_license
from fleio.notifications.models import DispatcherLog
from fleio.reseller.utils import user_reseller_resources
from reseller.core.signals import reseller_logged_in, reseller_logged_out
from rest_framework.response import Response

LOG = logging.getLogger(__name__)


class LoginRateThrottle(throttling.AnonRateThrottle):
    scope = 'login'


VERSION = {'backend_version': settings.FLEIO_BACKEND_VERSION,
           'backend_build': settings.FLEIO_BACKEND_BUILD,
           'latest_frontend_version': settings.FLEIO_LATEST_FRONTEND_VERSION,
           'latest_frontend_build': settings.FLEIO_LATEST_FRONTEND_BUILD}


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

    if user is None or not user.is_reseller:
        if user is None:
            UserModel = auth.get_user_model()
            try:
                matched_user = UserModel.objects.get(username=data['username'])
            except UserModel.DoesNotExist:
                # reseller user does not exists
                LOG.info('User {} not found in database'.format(data['username']))
            else:
                if matched_user.is_reseller:
                    LOG.info('Login failed for user {}.'.format(data['username']))
                else:
                    LOG.info('Login denied for user {}.'.format(data['username']))
        else:
            if not user.is_reseller:
                LOG.info('Login denied for user {}.'.format(data['username']))
        raise AuthenticationFailed(detail=_('Incorrect user name or password'))
    elif not user.is_active:
        LOG.info('Inactive user {} login attempted.'.format(data['username']))
        raise AuthenticationFailed(detail=_('This account is inactive'))
    elif not user_reseller_resources(user):
        LOG.info('User {} login attempted, but user is not associated with a reseller.'.format(data['username']))
        raise AuthenticationFailed(detail=_('This account is not associated with a reseller client'))
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
        reseller_logged_in.send(
            sender=__name__, user=user, user_id=user.pk, username=user.username,
            email=user.email, request=request
        )
        response_dict = {
            'user': get_current_user_info(request.user),
            'features': reseller_active_features.all,
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
    }


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def current_user(request):
    if request.user.is_authenticated and request.user.is_reseller:
        impersonated_user = request.session.get('impersonate', None)
        return Response({
            'user': get_current_user_info(request.user),
            'impersonated': impersonated_user == request.user.id,
            'features': reseller_active_features.all,
            'notifications': DispatcherLog.objects.filter(
                notification__user=request.user,
                name='frontend',
                status='pending',
            ).count(),
            'version': VERSION,
            'is_white_label': is_white_label_license()
        })
    else:
        return Response({
            'features': reseller_active_features.all,
            'version': VERSION,
            'is_white_label': is_white_label_license()
        })


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def logout(request):
    user = request.user

    if not user.is_authenticated:
        return Response(status=200)  # nothing should happen
    else:
        auth.logout(request)
        reseller_logged_out.send(
            sender=__name__, user=user, username=user.username, user_id=user.pk,
            email=user.email, request=request,
        )

    return Response({'detail': _('Logged out')})
