from django import apps
from django.utils.translation import ugettext_lazy as _

from fleio.core.plugins.plugin_definition import PluginDefinition
from fleio.core.plugins.plugin_definition import PluginConfigTypes


class GoogleAuthenticatorPluginConfig(apps.AppConfig):
    name = "plugins.google_authenticator"
    verbose_name = _("Google authenticator")
    fleio_module_type = 'second_factor_auth'
    fleio_help_text = _('Get a verification code from the Google Authenticator app or another compatible app')

    plugin_definition = None

    @classmethod
    def initialize_plugin(cls) -> PluginDefinition:

        if not cls.plugin_definition:

            definition = PluginDefinition(
                display_name=_('Google authenticator'),
                app_name=cls.name,
                app_label='google_authenticator',
                feature_name='clients&users.second_factor_auth.google_authenticator',
                staff_feature_name='clients&users.second_factor_auth.google_authenticator',
            )

            definition.add_url_config(
                config_type=PluginConfigTypes.staff,
                module_name='plugins.google_authenticator.staff.urls',
                path='google_authenticator',
                namespace='google_authenticator'
            )

            definition.add_url_config(
                config_type=PluginConfigTypes.enduser,
                module_name='plugins.google_authenticator.enduser.urls',
                path='google_authenticator',
                namespace='google_authenticator'
            )

            cls.plugin_definition = definition

        return cls.plugin_definition
