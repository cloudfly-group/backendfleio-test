from django import apps
from django.utils.translation import ugettext_lazy as _

from fleio.billing.modules.definition import BillingModuleDefinition

from fleio.core.plugins.plugin_definition import PluginDefinition
from fleio.core.plugins.plugin_definition import PluginConfigTypes


class HypanelPluginConfig(apps.AppConfig):
    name = 'plugins.hypanel'
    verbose_name = 'Fleio Hypanel plugin'

    module_definition = BillingModuleDefinition(
        module_name='Hypanel Module',
        import_path='plugins.hypanel.billing_module',
        class_name='HypanelModule'
    )

    plugin_definition = None

    @classmethod
    def initialize_plugin(cls) -> PluginDefinition:
        if not cls.plugin_definition:

            definition = PluginDefinition(
                display_name=_('Hypanel'),
                app_name=cls.name,
                app_label='hypanel',
                feature_name='plugins.hypanel',
                staff_feature_name='plugins.hypanel',
                server_settings={'hostname': {'required': True}}
            )

            definition.add_url_config(
                config_type=PluginConfigTypes.staff,
                module_name='plugins.hypanel.staff.urls',
                path='hypanel',
                namespace='hypanel'
            )

            cls.plugin_definition = definition

        return cls.plugin_definition
