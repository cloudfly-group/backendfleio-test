from django import apps
from django.utils.translation import ugettext_lazy as _

from fleio.core.plugins.plugin_definition import PluginDefinition
from fleio.core.plugins.plugin_definition import PluginConfigTypes


class SMSAuthenticatorPluginConfig(apps.AppConfig):
    name = "plugins.sms_authenticator"
    verbose_name = _("SMS authenticator")
    fleio_module_type = 'second_factor_auth'
    fleio_help_text = _('Get a verification code sent to your mobile phone')

    plugin_definition = None

    @classmethod
    def initialize_plugin(cls) -> PluginDefinition:

        if not cls.plugin_definition:

            definition = PluginDefinition(
                display_name=_('SMS authenticator'),
                app_name=cls.name,
                app_label='sms_authenticator',
                feature_name='clients&users.second_factor_auth.sms_authenticator',
                staff_feature_name='clients&users.second_factor_auth.sms_authenticator',
            )

            definition.add_url_config(
                config_type=PluginConfigTypes.staff,
                module_name='plugins.sms_authenticator.staff.urls',
                path='sms_authenticator',
                namespace='sms_authenticator'
            )

            definition.add_url_config(
                config_type=PluginConfigTypes.enduser,
                module_name='plugins.sms_authenticator.enduser.urls',
                path='sms_authenticator',
                namespace='sms_authenticator'
            )

            cls.plugin_definition = definition

        return cls.plugin_definition
