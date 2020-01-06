import pyotp
import qrcode

from typing import Optional

from django.db import IntegrityError
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _

from rest_framework.decorators import action
from rest_framework.response import Response

from fleio.core.exceptions import APIBadRequest
from fleio.core.features import active_features, staff_active_features
from fleio.core.models.second_factor_auth import SecondFactorAuthMethod, SecondFactorAuthType
from fleio.core.second_factor_auth.exceptions import SFAMethodNotAdded, SFAMethodNotEnabled, SFATypeNotFound
from fleio.core.second_factor_auth.remember_sfa import RememberSfa
from fleio.core.second_factor_auth.utils import get_app_name as utils_get_app_name
from fleio.core.second_factor_auth.views import SFABaseViewSet

from plugins.google_authenticator.apps import GoogleAuthenticatorPluginConfig
from plugins.google_authenticator.common.gasettings import google_authenticator_settings
from plugins.google_authenticator.models import GoogleAuthenticatorData


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
        name=utils_get_app_name(app_name=GoogleAuthenticatorPluginConfig.name)
    ).first()
    if not sfa_type:
        raise SFATypeNotFound()
    sfa_method = SecondFactorAuthMethod.objects.filter(user=user, type=sfa_type).first()
    if not sfa_method:
        raise SFAMethodNotAdded()
    google_auth_data = GoogleAuthenticatorData.objects.filter(method=sfa_method).first()
    secret_key = google_auth_data.get_secret_key()
    totp_code = pyotp.totp.TOTP(secret_key)
    result = totp_code.verify(code)
    if result:
        if remember:
            return RememberSfa(user=user).make_token()
        return None
    else:
        raise APIBadRequest(_('Code is invalid'))


class GoogleAuthenticatorBaseViewSet(SFABaseViewSet):

    @staticmethod
    def can_use_sfa_type(sfa_type: SecondFactorAuthType):
        raise NotImplementedError()

    @staticmethod
    def get_app_name():
        return utils_get_app_name(app_name=GoogleAuthenticatorPluginConfig.name)

    @staticmethod
    def get_google_auth_data(sfa_method: SecondFactorAuthMethod, create: bool = False) -> GoogleAuthenticatorData:
        # gets or creates google auth data
        google_auth_data = GoogleAuthenticatorData.objects.filter(method=sfa_method).first()
        if not google_auth_data and create:
            try:
                google_auth_data = GoogleAuthenticatorData.objects.create(
                    method=sfa_method, secret_key=pyotp.random_base32()
                )  # secret key is encrypted on save()
            except IntegrityError:
                # gdata for this method/user already exists, recalculate and return it
                return GoogleAuthenticatorData.objects.filter(method=sfa_method).first()
        return google_auth_data

    @action(detail=False, methods=['get'])
    def get_qr_code(self, request):
        del request  # unused
        try:
            sfa_type = self.get_sfa_type()
            sfa_method = self.get_sfa_method(sfa_type=sfa_type, raise_if_not_enabled=False)
        except (SFAMethodNotEnabled, SFATypeNotFound, SFAMethodNotAdded) as e:
            raise e
        google_auth_data = self.get_google_auth_data(sfa_method=sfa_method, create=True)
        secret = google_auth_data.get_secret_key()
        totp_code = pyotp.totp.TOTP(secret).provisioning_uri(
            self.request.user.email,
            issuer_name=google_authenticator_settings.issuer_name
        )
        qr_img = qrcode.make(totp_code).get_image()
        response = HttpResponse(content_type="image/png")
        qr_img.save(response, "PNG")
        return response

    @action(detail=False, methods=['get'])
    def get_code(self, request):
        del request  # unused
        try:
            sfa_type = self.get_sfa_type()
            sfa_method = self.get_sfa_method(sfa_type=sfa_type, raise_if_not_enabled=False)
        except (SFAMethodNotEnabled, SFATypeNotFound, SFAMethodNotAdded) as e:
            raise e
        google_auth_data = self.get_google_auth_data(sfa_method=sfa_method, create=True)
        secret_key = google_auth_data.get_secret_key()
        return Response({'secret_key': secret_key})

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
        google_auth_data = self.get_google_auth_data(sfa_method=sfa_method, create=True)
        secret_key = google_auth_data.get_secret_key()
        totp_code = pyotp.totp.TOTP(secret_key)
        allowed_to_enable = totp_code.verify(verification_code)
        if allowed_to_enable:
            sfa_method.enabled = True
            # if no other method is set as default, set this one
            default_method = SecondFactorAuthMethod.objects.filter(user=self.request.user, default=True).first()
            if not default_method:
                sfa_method.default = True
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

    @action(detail=False, methods=['post'])
    def regenerate_key(self, request):
        del request  # unused
        try:
            sfa_type = self.get_sfa_type()
            sfa_method = self.get_sfa_method(sfa_type=sfa_type, raise_if_not_enabled=False)
        except (SFAMethodNotEnabled, SFATypeNotFound, SFAMethodNotAdded) as e:
            raise e
        google_auth_data = self.get_google_auth_data(sfa_method=sfa_method)
        if not google_auth_data:
            raise APIBadRequest(_('The key was not yet generated'))
        google_auth_data.secret_key = pyotp.random_base32()  # key is hashed on model .save()
        google_auth_data.save()
        sfa_method.enabled = False
        sfa_method.default = False
        sfa_method.save()
        return Response({'detail': _('Successfully regenerated key')})
