from django import apps
from django.utils.translation import ugettext_lazy as _

from fleio.billing.modules.definition import BillingModuleDefinition
from fleio.core.plugins.plugin_definition import PluginDefinition
from fleio.core.plugins.plugin_definition import PluginConfigTypes


class CPanelServerPluginConfig(apps.AppConfig):
    name = 'plugins.cpanelserver'
    verbose_name = 'Fleio cPanel server'

    module_definition = BillingModuleDefinition(
        module_name='cPanel Billing',
        import_path='plugins.cpanelserver.billingmodule',
        class_name='CpanelBillingModule'
    )

    plugin_definition = None

    @classmethod
    def initialize_plugin(cls) -> PluginDefinition:
        if not cls.plugin_definition:
            definition = PluginDefinition(
                display_name=_('cPanel server'),
                app_name=cls.name,
                app_label='cpanelserver',
                feature_name='plugins.cpanelserver',
                staff_feature_name='plugins.cpanelserver',
                server_settings={'hostname': {'required': True},
                                 'username': {'required': True, 'default': 'root'},
                                 'api_token': {'required': True},
                                 'secure': {'default': True},
                                 'port': {'default': 2087},
                                 'max_accounts': {'required': False},
                                 'status_url': {'required': False},
                                 'location': {'required': False}}
            )

            # Staff urls
            definition.add_url_config(
                config_type=PluginConfigTypes.staff,
                module_name='plugins.cpanelserver.staff.urls',
                path='cpanelserver',
                namespace='cpanelserver'
            )
            # # Enduser urls
            # definition.add_url_config(
            #     config_type=PluginConfigTypes.enduser,
            #     module_name='plugins.cpanelserver.enduser.urls',
            #     path='cpanelserver',
            #     namespace='cpanelserver'
            # )

            cls.plugin_definition = definition

        return cls.plugin_definition
