from django import apps
from django.utils.translation import ugettext_lazy as _

from fleio.billing.modules.definition import BillingModuleDefinition
from fleio.core.plugins.plugin_definition import PluginDefinition
from fleio.core.plugins.plugin_definition import PluginConfigTypes


class CPanelPluginConfig(apps.AppConfig):
    name = 'plugins.cpanel'
    verbose_name = 'Fleio cPanel manage2 plugin'

    module_definition = BillingModuleDefinition(
        module_name='CPanel Manage2 Module',
        import_path='plugins.cpanel.manage2',
        class_name='Manage2Module'
    )

    plugin_definition = None

    @classmethod
    def initialize_plugin(cls) -> PluginDefinition:
        if not cls.plugin_definition:
            definition = PluginDefinition(
                display_name=_('CPanel Manage2'),
                app_name=cls.name,
                app_label='cpanel',
                feature_name='plugins.cpanel',
                staff_feature_name='plugins.cpanel',
            )

            # Staff urls
            definition.add_url_config(
                config_type=PluginConfigTypes.staff,
                module_name='plugins.cpanel.staff.urls',
                path='cpanel',
                namespace='cpanel'
            )
            # Enduser urls
            definition.add_url_config(
                config_type=PluginConfigTypes.enduser,
                module_name='plugins.cpanel.enduser.urls',
                path='cpanel',
                namespace='cpanel'
            )

            cls.plugin_definition = definition

        return cls.plugin_definition
