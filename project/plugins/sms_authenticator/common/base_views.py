import pyotp

from typing import Optional

from django.db import IntegrityError
from django.utils.module_loading import import_string
from django.utils.translation import ugettext_lazy as _
from django.contrib import auth
from rest_framework import permissions, throttling, viewsets

from rest_framework.decorators import action
from rest_framework.response import Response

from fleio.core.exceptions import APIBadRequest
from fleio.core.features import active_features, staff_active_features
from fleio.core.models.second_factor_auth import SecondFactorAuthMethod, SecondFactorAuthType
from fleio.core.second_factor_auth.exceptions import (SFAMethodNotAdded, SFAMethodNotEnabled, SFAMethodNotFound,
                                                      SFATypeNotFound)
from fleio.core.second_factor_auth.remember_sfa import RememberSfa
from fleio.core.second_factor_auth.utils import get_app_name as utils_get_app_name
from fleio.core.second_factor_auth.views import SFABaseViewSet
from fleio.core.sms_providers.throttle_rates import SMSSendingRateThrottle

from plugins.sms_authenticator.apps import SMSAuthenticatorPluginConfig
from plugins.sms_authenticator.common.smsasettings import sms_authenticator_settings
from plugins.sms_authenticator.models import SMSAuthenticatorData


class AnonymousSMSRateThrottle(throttling.AnonRateThrottle):
    scope = 'anonymous_sms_authenticator'


def confirm_login(user, remember=False, **args) -> Optional[str]:
    """Method called when user supplies second factor authentication info on login
    Returns either the remember token or None, in either case the user will get logged in
    Raising exception denies access to user"""
    if user.is_staff:
        demo_mode = staff_active_features.is_enabled('demo')
    else:
        demo_mode = active_features.is_enabled('demo')
    if demo_mode:
        return None  # in demo mode, allow any input and sign in the user

    code = args.get('code')
    if not code:
        raise APIBadRequest(_('Confirmation code is missing'))
    try:
        int(code)
    except Exception as e:
        del e  # unused
        raise APIBadRequest(_('Code has to be a number'))
    if int(code) > 999999:
        raise APIBadRequest(_('Code has to be a 6 digit number'))
    sfa_type = SecondFactorAuthType.objects.filter(
        name=utils_get_app_name(app_name=SMSAuthenticatorPluginConfig.name)
    ).first()
    if not sfa_type:
        raise SFATypeNotFound()
    sfa_method = SecondFactorAuthMethod.objects.filter(user=user, type=sfa_type).first()
    if not sfa_method:
        raise SFAMethodNotAdded()
    sms_auth_data = SMSAuthenticatorData.objects.filter(method=sfa_method).first()
    secret_key = sms_auth_data.get_secret_key()
    result = pyotp.hotp.HOTP(secret_key).verify(otp=code, counter=sms_auth_data.counter)
    if result:
        sms_auth_data.counter = sms_auth_data.counter + 1
        sms_auth_data.save(update_fields=['counter'])
        if remember:
            return RememberSfa(user=user).make_token()
        return None
    else:
        raise APIBadRequest(_('Code is invalid'))


def _get_sms_auth_data(sfa_method: SecondFactorAuthMethod, create: bool = False) -> SMSAuthenticatorData:
    # gets or creates sms auth data
    sms_auth_data = SMSAuthenticatorData.objects.filter(method=sfa_method).first()
    if not sms_auth_data and create:
        try:
            sms_auth_data = SMSAuthenticatorData.objects.create(
                method=sfa_method, secret_key=pyotp.random_base32()
            )  # secret key is encrypted on save()
        except IntegrityError:
            # sms data for this method/user already exists, recalculate and return it
            return SMSAuthenticatorData.objects.filter(method=sfa_method).first()
    return sms_auth_data


class SMSAuthenticatorBaseViewSet(SFABaseViewSet):

    @staticmethod
    def can_use_sfa_type(sfa_type: SecondFactorAuthType):
        raise NotImplementedError()

    @staticmethod
    def get_app_name():
        return utils_get_app_name(app_name=SMSAuthenticatorPluginConfig.name)

    @staticmethod
    def get_sms_auth_data(sfa_method: SecondFactorAuthMethod, create: bool = False) -> SMSAuthenticatorData:
        return _get_sms_auth_data(sfa_method=sfa_method, create=create)

    @action(detail=False, methods=['post'])
    def enable_sfa_method(self, request):
        verification_code = request.data.get('verification_code')
        try:
            int(verification_code)
        except Exception as e:
            del e  # unused
            raise APIBadRequest(_('Code has to be a number'))
        try:
            sfa_type = self.get_sfa_type()
        except Exception as e:
            raise e
        # sfa_method should already be here added through add_sfa_method action
        sfa_method = SecondFactorAuthMethod.objects.filter(user=self.request.user, type=sfa_type).first()
        if not sfa_method:
            raise SFAMethodNotAdded()
        if sfa_method.enabled:
            raise APIBadRequest(_('This method is already enabled'))
        sms_auth_data = self.get_sms_auth_data(sfa_method=sfa_method, create=True)
        secret_key = sms_auth_data.get_secret_key()
        allowed_to_enable = pyotp.hotp.HOTP(secret_key).verify(otp=verification_code, counter=sms_auth_data.counter)
        if allowed_to_enable:
            sfa_method.enabled = True
            # if no other method is set as default, set this one
            default_method = SecondFactorAuthMethod.objects.filter(user=self.request.user, default=True).first()
            if not default_method:
                sfa_method.default = True
            sms_auth_data.counter = sms_auth_data.counter + 1
            sms_auth_data.save(update_fields=['counter'])  # increase counter to generate another code next time
            sfa_method.save()
        else:
            raise APIBadRequest(_('Verification code is invalid.'))

        return Response({'detail': _('Operation completed')})

    @action(detail=False, methods=['post'])
    def disable_sfa_method(self, request):
        try:
            sfa_type = self.get_sfa_type()
        except Exception as e:
            raise e
        # sfa_method should already be here added through add_sfa_method action
        sfa_method = SecondFactorAuthMethod.objects.filter(user=self.request.user, type=sfa_type).first()
        if not sfa_method:
            raise SFAMethodNotAdded()
        if sfa_method.enabled is False:
            raise APIBadRequest(_('This method is already disabled'))
        sfa_method.enabled = False
        sfa_method.default = False
        sfa_method.save()
        return Response({'detail': _('Operation completed')})

    def get_throttles(self):
        if self.action == 'send_verification_code':
            return [SMSSendingRateThrottle(), ]
        return super().get_throttles()

    @action(detail=False, methods=['post'])
    def send_verification_code(self, request):
        if not request.user.mobile_phone_number:
            raise APIBadRequest(_('You need to set your mobile phone number first on your profile.'))
        try:
            provider_class_caller = import_string(
                'fleio.core.sms_providers.{}.{}.get_sms_provider_class'.format(
                    sms_authenticator_settings.provider, sms_authenticator_settings.provider
                )
            )
        except ImportError as e:
            del e  # unused
            raise APIBadRequest(_('Could not find SMS provider.'))
        provider_class = provider_class_caller()
        try:
            sfa_type = self.get_sfa_type()
        except Exception as e:
            raise e
        # sfa_method should already be here added through add_sfa_method action
        sfa_method = SecondFactorAuthMethod.objects.filter(user=self.request.user, type=sfa_type).first()
        if not sfa_method:
            raise SFAMethodNotAdded()
        sms_auth_data = self.get_sms_auth_data(sfa_method=sfa_method, create=True)
        secret_key = sms_auth_data.get_secret_key()
        code = pyotp.hotp.HOTP(secret_key).at(count=sms_auth_data.counter)
        provider_class.send_sms(
            phone_number=self.request.user.mobile_phone_number,
            message=sms_authenticator_settings.message.format(code),
            subject=sms_authenticator_settings.subject,
        )
        return Response({'detail': _('Verification code was sent.')})

    @action(detail=False, methods=['get'])
    def get_sfa_method_status(self, request):
        del request  # unused
        try:
            sfa_type = self.get_sfa_type()
        except SFATypeNotFound:
            return Response({'enabled': False, })
        try:
            sfa_method = self.get_sfa_method(sfa_type=sfa_type)
        except SFAMethodNotEnabled:
            return Response({'enabled': False, })
        except SFAMethodNotFound:
            sfa_method = self.add_sfa_method(sfa_type=sfa_type, user=self.request.user)
        return Response({
            'enabled': sfa_method.enabled,
            'default': sfa_method.default,
        })


class SMSAuthenticatorAnonymousBaseViewSet(viewsets.GenericViewSet):
    permission_classes = (permissions.AllowAny, )
    throttle_classes = (AnonymousSMSRateThrottle,)

    @action(detail=False, methods=['post'])
    def send_verification_code(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = auth.authenticate(username=username, password=password)
        if not user:
            raise APIBadRequest(_('Cannot send verification code.'))
        if not user.mobile_phone_number:
            raise APIBadRequest(_('User doesn\'t have a mobile number associated with the account.'))
        try:
            provider_class_caller = import_string(
                'fleio.core.sms_providers.{}.{}.get_sms_provider_class'.format(
                    sms_authenticator_settings.provider, sms_authenticator_settings.provider
                )
            )
        except ImportError as e:
            del e  # unused
            raise APIBadRequest(_('Could not find SMS provider.'))
        provider_class = provider_class_caller()
        sfa_type_name = utils_get_app_name(app_name=SMSAuthenticatorPluginConfig.name)
        sfa_type = SecondFactorAuthType.objects.filter(name=sfa_type_name).first()
        if not sfa_type:
            raise SFATypeNotFound()
        # sfa_method should already be here added through add_sfa_method action
        sfa_method = SecondFactorAuthMethod.objects.filter(user=user, type=sfa_type).first()
        if not sfa_method:
            raise SFAMethodNotAdded()
        sms_auth_data = _get_sms_auth_data(sfa_method=sfa_method, create=True)
        secret_key = sms_auth_data.get_secret_key()
        code = pyotp.hotp.HOTP(secret_key).at(count=sms_auth_data.counter)
        provider_class.send_sms(
            phone_number=user.mobile_phone_number,
            message=sms_authenticator_settings.message.format(code),
            subject=sms_authenticator_settings.subject,
        )
        user_phone = list(user.mobile_phone_number)
        for i in range(len(user_phone) - 3):
            user_phone[i] = '*'
        return Response({
            'detail': _('Verification code was sent.'),
            'receiver': ''.join(user_phone),
        })
