from django import apps
from django.utils.translation import ugettext_lazy as _

from fleio.billing.modules.definition import BillingModuleDefinition

from fleio.core.plugins.plugin_definition import MenuItem
from fleio.core.plugins.plugin_definition import PluginDefinition
from fleio.core.plugins.plugin_definition import PluginConfigTypes

from plugins.domains.utils.whois_config import whois_config


class DomainsPluginConfig(apps.AppConfig):
    name = 'plugins.domains'
    verbose_name = 'Domains'

    module_definition = BillingModuleDefinition(
        module_name='Domains Module',
        import_path='plugins.domains.billing_module',
        class_name='DomainsModule'
    )

    plugin_definition = None

    @classmethod
    def initialize_plugin(cls) -> PluginDefinition:
        if not cls.plugin_definition:
            # register signals

            # register functions

            definition = PluginDefinition(
                display_name=_('Domains'),
                app_name=cls.name,
                app_label='domains',
                feature_name='plugins.domains',
                staff_feature_name='plugins.domains',
            )

            # Staff plugin menu definition
            definition.add_menu_item(config_type=PluginConfigTypes.staff, menu_item=MenuItem(
                label=_('Domains'),
                state='pluginsDomainsDomains',
                icon='dns_zones',
                feature='plugins.domains',
                plugin_name='domains',
            ))

            definition.add_menu_item(config_type=PluginConfigTypes.staff, menu_item=MenuItem(
                label=_('Register domain'),
                state='pluginsDomainsRegisterDomain',
                icon='shopping_cart',
                feature='plugins.domains',
                plugin_name='domains',
            ))

            definition.add_menu_item(config_type=PluginConfigTypes.staff, menu_item=MenuItem(
                label=_('Transfer domain'),
                state='pluginsDomainsTransferDomain',
                icon='tld',
                feature='plugins.domains',
                plugin_name='domains',
            ))

            definition.add_menu_item(config_type=PluginConfigTypes.staff, menu_item=MenuItem(
                label=_('Domain contacts'),
                state='pluginsDomainsContacts',
                icon='clients',
                feature='plugins.domains',
                plugin_name='domains',
            ))

            definition.add_menu_item(config_type=PluginConfigTypes.staff, menu_item=MenuItem(
                label=_('TLDs'),
                state='pluginsDomainsTlds',
                icon='tld',
                feature='plugins.domains',
                plugin_name='domains',
            ))

            definition.add_menu_item(config_type=PluginConfigTypes.staff, menu_item=MenuItem(
                label=_('Registrars'),
                state='pluginsDomainsRegistrars',
                icon='registrar',
                feature='plugins.domains',
                plugin_name='domains',
            ))

            # Enduser plugin menu definition
            definition.add_menu_item(config_type=PluginConfigTypes.enduser, menu_item=MenuItem(
                label=_('My domains'),
                state='pluginsDomainsDomains',
                icon='dns_zones',
                feature='plugins.domains',
                plugin_name='domains',
            ))

            definition.add_menu_item(config_type=PluginConfigTypes.enduser, menu_item=MenuItem(
                label=_('Domain contacts'),
                state='pluginsDomainsContacts',
                icon='clients',
                feature='plugins.domains',
                plugin_name='domains',
            ))

            definition.add_menu_item(config_type=PluginConfigTypes.enduser, menu_item=MenuItem(
                label=_('Register domain'),
                state='pluginsDomainsRegisterDomain',
                icon='shopping_cart',
                feature='plugins.domains',
                plugin_name='domains',
            ))

            definition.add_menu_item(config_type=PluginConfigTypes.enduser, menu_item=MenuItem(
                label=_('Transfer domain'),
                state='pluginsDomainsTransferDomain',
                icon='tld',
                feature='plugins.domains',
                plugin_name='domains',
            ))

            definition.add_url_config(
                config_type=PluginConfigTypes.staff,
                module_name='plugins.domains.staff.urls',
                path='domains',
                namespace='domains'
            )

            definition.add_url_config(
                config_type=PluginConfigTypes.enduser,
                module_name='plugins.domains.enduser.urls',
                path='domains',
                namespace='domains'
            )

            cls.plugin_definition = definition

            # additional initialization
            app_config = apps.apps.get_app_config(definition.app_label)
            app_path = app_config.path
            whois_config.load_config(app_path=app_path)

        return cls.plugin_definition
