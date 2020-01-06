from datetime import datetime, timedelta

import pytz
from django.conf import settings
from django.utils.timezone import now as utcnow
from django.utils.translation import ugettext_lazy as _
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from fleio.core.exceptions import APIBadRequest
from fleio.core.models import AppUser, SecondFactorAuthType
from fleio.core.models.second_factor_auth import SecondFactorAuthMethod
from fleio.core.second_factor_auth.exceptions import SFAMethodNotEnabled, SFAMethodNotFound, SFATypeNotFound
from fleio.core.second_factor_auth.permissions.sfa_manage import SFAManagerPermissions
from fleio.core.second_factor_auth.serializers import SecondFactorAuthTypeSerializer
from fleio.core.second_factor_auth.utils import get_app_name, REMEMBER_PASSWORD_CONFIRM_MINUTES


class SFABaseViewSet(viewsets.GenericViewSet):
    permission_classes = (SFAManagerPermissions,)

    @staticmethod
    def get_app_name():
        raise NotImplementedError()

    @action(detail=False, methods=['post'])
    def enable_sfa_method(self, request):
        raise NotImplementedError()

    @action(detail=False, methods=['post'])
    def disable_sfa_method(self, request):
        # disables the sfa method
        #   - remember to remove default status if this is the default sfa_method
        raise NotImplementedError()

    def get_sfa_type(self) -> SecondFactorAuthType:
        sfa_type_name = get_app_name(app_name=self.get_app_name())
        sfa_type = SecondFactorAuthType.objects.filter(name=sfa_type_name).first()
        if not sfa_type:
            raise SFATypeNotFound()
        if not self.can_use_sfa_type(sfa_type=sfa_type):
            raise SFATypeNotFound()
        return sfa_type

    @staticmethod
    def add_sfa_method(sfa_type: SecondFactorAuthType, user: AppUser):
        sfa_method = SecondFactorAuthMethod.objects.create(user=user, type=sfa_type)
        return sfa_method

    @action(detail=False, methods=['post'])
    def set_as_default(self, request):
        try:
            sfa_type = self.get_sfa_type()
        except SFATypeNotFound as e:
            raise e
        try:
            sfa_method = self.get_sfa_method(sfa_type=sfa_type)
        except (SFAMethodNotEnabled, SFAMethodNotFound) as e:
            raise e
        if sfa_method.default:
            raise APIBadRequest(_('This method is already default method'))
        default_sfa = SecondFactorAuthMethod.objects.filter(user=request.user, default=True).first()
        if default_sfa:
            default_sfa.default = False
            default_sfa.save()
        sfa_method.default = True
        sfa_method.save()
        return Response({'detail': 'Operation completed.'})

    @action(detail=False, methods=['get'])
    def get_sfa_method_status(self, request):
        del request  # unused
        try:
            sfa_type = self.get_sfa_type()
        except SFATypeNotFound:
            return Response({'enabled': False})
        try:
            sfa_method = self.get_sfa_method(sfa_type=sfa_type)
        except SFAMethodNotEnabled:
            return Response({'enabled': False})
        except SFAMethodNotFound:
            sfa_method = self.add_sfa_method(sfa_type=sfa_type, user=self.request.user)
        return Response({
            'enabled': sfa_method.enabled,
            'default': sfa_method.default,
        })

    @staticmethod
    def can_use_sfa_type(sfa_type: SecondFactorAuthType):
        raise NotImplementedError()

    def get_sfa_method(self, sfa_type: SecondFactorAuthType,
                       raise_if_not_enabled: bool = True) -> SecondFactorAuthMethod:
        sfa_method = SecondFactorAuthMethod.objects.filter(user=self.request.user, type=sfa_type).first()
        if not sfa_method:
            raise SFAMethodNotFound()
        if not sfa_method.enabled and raise_if_not_enabled:
            raise SFAMethodNotEnabled()
        return sfa_method


class SFATypesManagerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SecondFactorAuthType.objects.filter(enabled_to_enduser=True)
    serializer_class = SecondFactorAuthTypeSerializer

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
        if 'impersonate' in request.session:
            return Response({'allowed': True})
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
