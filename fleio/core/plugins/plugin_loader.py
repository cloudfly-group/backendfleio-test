import logging
from typing import Dict

from django import apps

from fleio.core.features import active_features
from fleio.core.features import staff_active_features
from fleio.core.models import Plugin
from fleio.core.plugins.plugin_definition import PluginDefinition

LOG = logging.getLogger(__name__)


class PluginLoader(object):
    def __init__(self):
        self.found_plugin_definitions = {}  # type: Dict[str, PluginDefinition]
        self.active_plugin_definitions = {}  # type: Dict[str, PluginDefinition]
        self.enduser_active_plugin_definitions = {}  # type: Dict[str, PluginDefinition]
        self.staff_active_plugin_definitions = {}  # type: Dict[str, PluginDefinition]

    def refresh_plugins(self):
        definitions = {}  # type: Dict[str, PluginDefinition]
        for app_config in apps.apps.get_app_configs():  # type: apps.AppConfig
            if hasattr(app_config, 'initialize_plugin') and callable(app_config.initialize_plugin):
                LOG.info('Found plugin {}'.format(app_config.name))
                definition = app_config.initialize_plugin()  # type: PluginDefinition
                definition.refresh_components()
                definitions[definition.app_label] = definition

        self.found_plugin_definitions = dict(definitions)

        plugins_in_db = []

        # update database
        for plugin in Plugin.objects.all():
            if plugin.app_label in definitions:
                plugins_in_db.append(plugin.app_label)

                if not plugin.app_loaded:
                    plugin.app_loaded = True
                    plugin.save(update_fields=['app_loaded'])

                # remove disabled definitions
                if not plugin.enabled:
                    del definitions[plugin.app_label]
                else:
                    definitions[plugin.app_label].plugin_model = plugin
            else:
                if plugin.app_loaded:
                    plugin.app_loaded = False
                    plugin.save(update_fields=['app_loaded'])

        for app_label in definitions:
            if app_label not in plugins_in_db:
                plugin_definition = definitions[app_label]  # type: PluginDefinition
                plugin_definition.plugin_model = Plugin.objects.create(
                    display_name=plugin_definition.display_name,
                    app_name=plugin_definition.app_name,
                    app_label=plugin_definition.app_label,
                    feature_name=plugin_definition.feature_name,
                    staff_feature_name=plugin_definition.staff_feature_name,
                    app_loaded=True
                )

        for definition in definitions.values():
            if active_features.is_enabled(definition.feature_name):
                LOG.info('Plugin {} is enabled for enduser'.format(definition.app_label))
                self.enduser_active_plugin_definitions[definition.app_label] = definition
            if staff_active_features.is_enabled(definition.staff_feature_name):
                LOG.info('Plugin {} is enabled for staff'.format(definition.app_label))
                self.staff_active_plugin_definitions[definition.app_label] = definition

        self.active_plugin_definitions = definitions

    @property
    def enduser_plugins(self) -> Dict[str, PluginDefinition]:
        return self.enduser_active_plugin_definitions

    @property
    def staff_plugins(self) -> Dict[str, PluginDefinition]:
        return self.staff_active_plugin_definitions


plugin_loader = PluginLoader()
