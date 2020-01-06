import logging
from typing import List
from typing import Optional

from fleio.core.plugins.plugin_definition import PluginDefinition
from fleio.core.plugins.plugin_definition import PluginConfigTypes
from fleio.core.plugins.plugin_loader import plugin_loader
from fleio.core.plugins.plugin_ui_component import PluginUIComponent
from fleio.core.plugins.plugin_ui_service import PluginUIService

LOG = logging.getLogger(__name__)


class PluginUtils(object):
    @classmethod
    def get_plugins(cls, config_type: str):
        if config_type == PluginConfigTypes.enduser:
            return plugin_loader.enduser_plugins

        if config_type == PluginConfigTypes.staff:
            return plugin_loader.staff_plugins

        LOG.error('Invalid config type {}'.format(config_type))
        return {}

    @classmethod
    def get_plugin(cls, config_type: str, plugin_label: str):
        plugins = cls.get_plugins(config_type=config_type)
        return plugins.get(plugin_label, None)

    @classmethod
    def append_plugin_urls(cls, urlpatterns: List, config_type: str):
        plugins = cls.get_plugins(config_type=config_type)

        # add plugin urls module_definition
        for app_name in plugins:
            plugin_definition = plugins[app_name]  # type: PluginDefinition
            plugin_definition.append_url_patterns(
                config_type=config_type,
                urlpatterns=urlpatterns
            )

    @classmethod
    def get_component(cls, config_type: str, plugin_label: str, component_name: str) -> Optional[PluginUIComponent]:
        if not plugin_label:
            return None

        plugins = cls.get_plugins(config_type=config_type)
        if plugins and plugin_label in plugins:
            return plugins[plugin_label].components[config_type].get(component_name, None)
        else:
            LOG.warning('Plugin {} does not exists or is not loaded'.format(plugin_label))
            return None

    @classmethod
    def get_service(cls, config_type: str, plugin_label: str, service_name: str) -> Optional[PluginUIService]:
        plugins = cls.get_plugins(config_type=config_type)
        if plugins and plugin_label in plugins:
            return plugins[plugin_label].services[config_type].get(service_name, None)
        else:
            LOG.warning('Plugin {} does not exists or is not loaded'.format(plugin_label))
            return None

    @classmethod
    def get_staff_component(cls, plugin_label: str, component_name: str) -> Optional[PluginUIComponent]:
        return cls.get_component(
            config_type=PluginConfigTypes.staff,
            plugin_label=plugin_label,
            component_name=component_name
        )

    @classmethod
    def get_enduser_component(cls, plugin_label: str, component_name: str) -> Optional[PluginUIComponent]:
        return cls.get_component(
            config_type=PluginConfigTypes.enduser,
            plugin_label=plugin_label,
            component_name=component_name
        )

    @classmethod
    def has_component(cls, config_type: str, plugin_label: str, component_name: str) -> bool:
        return cls.get_component(
            config_type=config_type,
            plugin_label=plugin_label,
            component_name=component_name
        ) is not None

    @classmethod
    def has_staff_component(cls, plugin_label: str, component_name: str) -> bool:
        return cls.get_staff_component(
            plugin_label=plugin_label,
            component_name=component_name
        ) is not None

    @classmethod
    def has_enduser_component(cls, plugin_label: str, component_name: str) -> bool:
        return cls.get_enduser_component(
            plugin_label=plugin_label,
            component_name=component_name
        ) is not None

    @classmethod
    def get_plugin_definition_for_module_path(cls, module_path: str) -> PluginDefinition:
        for label in plugin_loader.active_plugin_definitions:
            plugin_definition = plugin_loader.active_plugin_definitions[label]
            if module_path.startswith('{}.'.format(plugin_definition.app_name)):
                return plugin_definition

    @classmethod
    def get_plugins_for_component(cls, config_type: str, component_name: str) -> List[PluginDefinition]:
        plugins = cls.get_plugins(config_type=config_type)
        found_plugins = []
        for plugin_label in plugins:
            if cls.has_component(
                    config_type=config_type,
                    plugin_label=plugin_label,
                    component_name=component_name,
            ):
                found_plugins.append(plugins[plugin_label])

        return found_plugins

    @classmethod
    def get_plugins_labels_for_component(cls, config_type: str, component_name: str) -> List[str]:
        plugins = cls.get_plugins(config_type=config_type)
        found_plugins = []
        for plugin_label in plugins:
            if cls.has_component(
                    config_type=config_type,
                    plugin_label=plugin_label,
                    component_name=component_name,
            ):
                found_plugins.append(plugin_label)

        return found_plugins

    @classmethod
    def get_plugins_menus(cls, config_type: str):
        menus = []
        menu_items = []

        plugins = cls.get_plugins(config_type)
        for plugin_name in plugins:
            plugin = plugins[plugin_name]
            if plugin.has_top_level_menu(config_type):
                top_level_menu = plugin.get_top_level_menu(config_type)
                menus.append(plugin.get_top_level_menu(config_type))
                for menu_item in top_level_menu['items']:
                    menu_items.append(menu_item)

        return {
            'menus': sorted(menus, key=lambda k: k['category']),
            'menu_items': menu_items,
        }

    @classmethod
    def get_server_plugins(cls) -> List:
        """Get plugins that support servers"""
        plugins = cls.get_plugins(config_type=PluginConfigTypes.staff)
        server_plugins = []
        for plugin_label, plugin in plugins.items():
            if plugin.server_settings:
                has_settings_component = cls.has_component(config_type='staff',
                                                           plugin_label=plugin_label,
                                                           component_name='ServerSettings')
                server_plugins.append({'label': plugin_label,
                                       'id': plugin.plugin_model.id,
                                       'display_name': plugin.display_name,
                                       'has_settings_component': has_settings_component,
                                       'has_server_settings': True,
                                       'server_settings': plugin.server_settings
                                       })
        return server_plugins

    @classmethod
    def get_all_ui(cls) -> str:
        return ''
