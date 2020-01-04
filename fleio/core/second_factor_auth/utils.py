import logging
import sys
from typing import Optional

from django.utils.translation import ugettext_lazy as _
from django.contrib import auth
from django.apps import apps
from django.utils.module_loading import import_string

from rest_framework.response import Response

from fleio.core.exceptions import APIBadRequest
from fleio.core.features import active_features, staff_active_features
from fleio.core.models import AppUser, SecondFactorAuthMethod, SecondFactorAuthType
from fleio.core.second_factor_auth.remember_sfa import RememberSfa

LOG = logging.getLogger(__name__)

REMEMBER_PASSWORD_CONFIRM_MINUTES = 30  # number of minutes user won't be required to enter again his password in order
# to manage his own sfa settings

SECOND_FA_TABLE_UPDATED = False

SECOND_FA_NAME_PREFIX = 'plugins.'


def get_app_name(app_name):
    return app_name.replace(SECOND_FA_NAME_PREFIX, '')


def update_second_factor_auth_type_table():
    global SECOND_FA_TABLE_UPDATED
    if SECOND_FA_TABLE_UPDATED:
        return

    LOG.debug('Searching apps for second factor authentication types...')

    installed_plugins = []

    for app in apps.get_app_configs():
        if not app.name.startswith(SECOND_FA_NAME_PREFIX):
            continue
        if getattr(app, 'fleio_module_type', None):
            if app.fleio_module_type == 'second_factor_auth':
                try:
                    LOG.debug('Processing app ''{}'''.format(app.name))
                    name = get_app_name(app_name=app.name)
                    existing_type = SecondFactorAuthType.objects.filter(name=name).first()
                    installed_plugins.append(name)
                    sfa_type_params = {
                        'name': name,
                        'display_name': app.verbose_name,
                        'help_text': app.fleio_help_text,
                    }
                    if name == 'google_authenticator':
                        # we make google authenticator enabled by default
                        sfa_type_params['enabled_to_staff'] = True
                        sfa_type_params['enabled_to_enduser'] = True
                    if not existing_type:
                        SecondFactorAuthType.objects.create(**sfa_type_params)
                except Exception as e:
                    LOG.exception(e)

    try:
        SecondFactorAuthType.objects.all().exclude(name__in=installed_plugins).delete()
    except Exception as e:
        del e  # unused
        LOG.error('If you remove a second factor authentication plugin from installed apps that contains user data, '
                  'you will need to manually remove from \'django admin -> Fleio core app -> Second factor auth '
                  'types\' the record related to your plugin.')
        sys.exit()

    SECOND_FA_TABLE_UPDATED = True


def process_login_with_sfa(request) -> (bool, Optional[str]):
    sfa_params = request.data.get('sfa_params')
    sfa_completed = False
    cookies = request.stream.COOKIES or {}
    remember_sfa_token = cookies.get('rSFA')
    user = auth.authenticate(username=request.data.get('username'), password=request.data.get('password'))
    if remember_sfa_token and RememberSfa(user=user).check_token(token=remember_sfa_token):
        sfa_completed = True
    if sfa_params:
        del request.data['sfa_params']
        sfa_method_name = sfa_params.get('sfa_method_name')
        remember_sfa = sfa_params.get('rememberSFA', False)
        try:
            confirm_method = import_string(
                'plugins.{}.common.base_views.confirm_login'.format(sfa_method_name)
            )
        except ImportError:
            LOG.debug('Could not find sfa confirm method for {}'.format(sfa_method_name))
            raise APIBadRequest(_('Could not find confirmation method'))
        sfa_args = sfa_params.get('args')
        if sfa_args:
            try:
                remember_sfa_token = confirm_method(user=user, remember=remember_sfa, **sfa_args)
                sfa_completed = True
            except Exception as e:
                raise e
    return sfa_completed, remember_sfa_token


def check_sfa_required_and_get_settings(user: AppUser) -> (bool, Optional[Response]):
    if user.is_staff:
        if not staff_active_features.is_enabled('clients&users.second_factor_auth'):
            return False, None
    else:
        if not active_features.is_enabled('clients&users.second_factor_auth'):
            return False, None
    sfa_methods = SecondFactorAuthMethod.objects.filter(user=user, enabled=True)
    enabled_sfa_methods = sfa_methods.count()
    if enabled_sfa_methods:
        # if user has sfa methods enabled, sfa is required and he'll be able to choose from one of those
        available_sfa_methods = list()
        for method in sfa_methods:
            available_sfa_methods.append(dict(
                name=method.type.name, display_name=method.type.display_name,
                default=method.default, help_text=method.type.help_text,
            ))
        return True, Response({
            'detail': _('Second factor authentication required'),
            'sfa_required': True,
            'sfa_methods': available_sfa_methods,
        })
    return False, None
