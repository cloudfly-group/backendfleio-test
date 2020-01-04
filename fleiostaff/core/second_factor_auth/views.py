import logging
from datetime import datetime, timedelta

import pytz
from django.conf import settings
from django.utils.timezone import now as utcnow
from django.utils.translation import ugettext_lazy as _
from rest_framework import filters, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response

from fleio.core.drf import StaffOnly
from fleio.core.exceptions import APIBadRequest
from fleio.core.features import staff_active_features
from fleio.core.models import AppUser, SecondFactorAuthMethod, SecondFactorAuthType
from fleio.core.second_factor_auth.sfasettings import sfa_settings, SFASettingsConfig
from fleio.core.second_factor_auth.utils import REMEMBER_PASSWORD_CONFIRM_MINUTES
from fleiostaff.core.second_factor_auth.serializers import SFASettingsSerializer, StaffSecondFactorAuthTypeSerializer

LOG = logging.getLogger(__name__)


class SecondFactorAuthTypeViewSet(viewsets.GenericViewSet,
                                  viewsets.mixins.RetrieveModelMixin,
                                  viewsets.mixins.UpdateModelMixin,
                                  viewsets.mixins.ListModelMixin):
    serializer_class = StaffSecondFactorAuthTypeSerializer
    permission_classes = (StaffOnly,)
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('id', 'name')

    def list(self, request, *args, **kwargs):
        return super().list(request=request, *args, **kwargs)

    def get_queryset(self):
        if self.action == 'update' or self.action == 'get_for_settings':
            return SecondFactorAuthType.objects.all()
        return SecondFactorAuthType.objects.filter(enabled_to_staff=True)

    @action(detail=False, methods=['get'])
    def get_for_settings(self, request):
        return super().list(request=request)

    def perform_update(self, serializer):
        sfa_type = self.get_object()
        enabled_to_staff = serializer.validated_data.get('enabled_to_staff', None)
        enabled_to_enduser = serializer.validated_data.get('enabled_to_enduser', None)
        no_other_option_msg = _(
            'Second factor authentication is required and users have no other option than the one you want to disable.'
        )
        staff_users = AppUser.objects.filter(is_staff=True)
        if enabled_to_staff is False:
            # check if other method is available if sfa is required
            staff_other_types_count = SecondFactorAuthType.objects.filter(
                enabled_to_staff=True
            ).exclude(id=sfa_type.id).count()
            if staff_other_types_count == 0 and (sfa_settings.require_staff_users_to_use_sfa is True or
                                                 sfa_settings.require_end_users_to_use_sfa is True):
                raise APIBadRequest(no_other_option_msg)
            # disable methods only for staff-users
            SecondFactorAuthMethod.objects.filter(type=sfa_type, user__in=staff_users).update(
                enabled=False, default=False
            )
        if enabled_to_enduser is False:
            enduser_other_types_count = SecondFactorAuthType.objects.filter(
                enabled_to_enduser=True
            ).exclude(id=sfa_type.id).count()
            # check if other method is available if sfa is required
            if enduser_other_types_count == 0 and sfa_settings.require_end_users_to_use_sfa is True:
                raise APIBadRequest(no_other_option_msg)
            # disable methods only for end-users
            SecondFactorAuthMethod.objects.filter(
                type=sfa_type
            ).exclude(
                user__in=staff_users
            ).update(enabled=False, default=False)
        return super().perform_update(serializer=serializer)

    @action(detail=False, methods=['post'])
    def confirm_password(self, request):
        provided_password = request.data.get('password')
        if request.user.check_password(provided_password):
            self.request.session['sfa_manager'] = {
                'allowed': True,
                'allowed_at': utcnow().strftime('%B %d %Y - %H:%M:%S')
            }
            return Response({'detail': _('Password confirmed')})
        raise APIBadRequest(_('You provided an incorrect password'))

    @action(detail=False, methods=['get'])
    def has_password_confirmed(self, request):
        elapsed_time_since_last_login = utcnow() - request.user.last_login
        if elapsed_time_since_last_login < timedelta(
                minutes=getattr(settings, 'ALLOW_CHANGING_SFA_AFTER_LOGIN_MINUTES', 5)
        ):
            return Response({'allowed': True})  # if user logged in earlier than 2 mins he is allowed
        if 'sfa_manager' in request.session:
            allowed_at = datetime.strptime(request.session['sfa_manager']['allowed_at'], '%B %d %Y - %H:%M:%S')
            allowed_at = allowed_at.replace(tzinfo=pytz.utc)
            elapsed_time_since_last_allowed = utcnow() - allowed_at
            if elapsed_time_since_last_allowed > timedelta(minutes=REMEMBER_PASSWORD_CONFIRM_MINUTES):
                return Response({'allowed': False})
            return Response({'allowed': request.session['sfa_manager']['allowed']})
        return Response({'allowed': False})


def _get_sfa_settings(configuration: SFASettingsConfig):
    settings_serializer = SFASettingsSerializer(instance=configuration)
    response_obj = dict(
        sfa_settings=settings_serializer.data
    )
    return Response(response_obj)


@api_view(['GET', 'POST'])
@permission_classes((StaffOnly,))
def sfa_settings_view(request):
    conf = SFASettingsConfig(raise_if_required_not_set=False)
    if request.method == 'GET':
        return _get_sfa_settings(configuration=conf)
    elif request.method == 'POST':
        if staff_active_features.is_enabled('demo'):
            raise APIBadRequest(_('Cannot change second factor authentication settings in demo mode'))
        serializer = SFASettingsSerializer(instance=conf, data=request.data)
        serializer.is_valid(raise_exception=True)
        no_sfa_message = _('Cannot enable this setting because no second factor authentication method is enabled')
        if serializer.validated_data.get('require_end_users_to_use_sfa', None) is True:
            has_sfa = SecondFactorAuthType.objects.filter(enabled_to_enduser=True).count()
            if has_sfa == 0:
                raise APIBadRequest(no_sfa_message)
        if serializer.validated_data.get('require_staff_users_to_use_sfa', None) is True:
            has_sfa = SecondFactorAuthType.objects.filter(enabled_to_staff=True).count()
            if has_sfa == 0:
                raise APIBadRequest(no_sfa_message)
        serializer.save()
        return _get_sfa_settings(configuration=conf)
    else:
        return Response({})
