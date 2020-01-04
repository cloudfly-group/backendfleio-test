import logging
import os
from typing import Dict
from typing import List
from typing import Tuple

from django import urls
from django.apps import apps
from django.conf import settings
from django.utils.module_loading import import_string

from fleio.core.features import active_features
from fleio.core.features import staff_active_features

from fleio.core.plugins.plugin_ui_component import PluginUIComponent
from fleio.core.plugins.plugin_config_types import PluginConfigTypes
from fleio.core.plugins.plugin_ui_service import PluginUIService
from fleio.core.plugins.plugin_ui_states import PluginUIStates

LOG = logging.getLogger(__name__)


class UrlsConfig(object):
    def __init__(
            self,
            module_name: str,
            base_path: str,
            path: str,
            namespace: str,
            app_name: str,
    ):
        self.module_name = module_name
        self.base_path = base_path
        self.path = path
        self.namespace = namespace
        self.app_name = app_name

    def get_url_patterns(self):
        if self.base_path == '' and self.path == '':
            path = ''
        else:
            path = '{}{}/'.format(self.base_path, self.path)
        return urls.path(
            path,
            urls.include((self.module_name, self.app_name), self.namespace)
        )


class MenuItem(object):
    def __init__(
            self,
            label: str,
            state: str,
            icon: str,
            feature: str,
            plugin_name: str
    ):
        self.label = label
        self.state = state
        self.icon = icon
        self.feature = feature
        self.plugin_name = plugin_name

    def to_item(self):
        return {
            'label': self.label,
            'state': self.state,
            'icon': self.icon,
            'feature': self.feature,
            'plugin_name': self.plugin_name,
        }


class PluginDefinition:
    def __init__(
            self,
            display_name: str,
            app_name: str,
            app_label: str,
            feature_name: str,
            staff_feature_name: str,
            server_settings=None,
    ):
        self.display_name = display_name
        self.app_name = app_name
        self.app_label = app_label
        self.feature_name = feature_name
        self.staff_feature_name = staff_feature_name
        self.urls_configs = {}
        self.plugin_model = None
        self._server_settings = server_settings
        self.components = {
            PluginConfigTypes.enduser: {},
            PluginConfigTypes.staff: {}
        }  # type: Dict[str, Dict[str, PluginUIComponent]]
        self.states = {}
        self.services = {
            PluginConfigTypes.enduser: {},
            PluginConfigTypes.staff: {}
            # type: Dict[str, Dict[str, PluginUIService]]
        }
        self.menu_config = {
            PluginConfigTypes.enduser: [],
            PluginConfigTypes.staff: []
        }  # type: Dict[str, List[MenuItem]]

    def has_top_level_menu(self, config_type: str):
        return len(self.menu_config[config_type]) > 0

    @property
    def server_settings(self):
        """Server settings is a list of fields that should be shown in UI server details/create"""
        if self._server_settings and type(self._server_settings) is dict:
            return self._server_settings

    def get_top_level_menu(self, config_type: str):
        if len(self.menu_config[config_type]) == 0:
            return None
        else:
            return {
                'category': self.display_name,
                'main_feature': self.feature_name,
                'items': [
                    menu_item.to_item() for menu_item in self.menu_config[config_type]
                ]

            }

    def add_menu_item(self, config_type: str, menu_item: MenuItem):
        self.menu_config[config_type].append(menu_item)

    def add_url_config(self, config_type: str, module_name: str, path: str, namespace: str, base_path: str = None):
        self.urls_configs[config_type] = UrlsConfig(
            module_name=module_name,
            base_path=settings.PLUGIN_URLS_BASE_PATH if base_path is None else base_path,
            path=path,
            namespace=namespace,
            app_name=self.app_name,
        )

    def get_url_patterns(self, config_type: str):
        urls_config = self.urls_configs.get(config_type, None)  # type: UrlsConfig
        return urls_config.get_url_patterns()

    def has_url_patterns(self, config_type: str):
        return config_type in self.urls_configs

    def append_url_patterns(self, config_type: str, urlpatterns: List):
        if self.has_url_patterns(config_type=config_type):
            urlpatterns.append(self.get_url_patterns(config_type=config_type))

    def load_components_and_services(self, path: str, import_path: str, config_type: str) -> Tuple[Dict, Dict]:
        found_components = {}
        found_services = {}
        if not os.path.isdir(path):
            return found_components, found_services
        for component_disk_name in os.listdir(path):
            if component_disk_name.startswith('__') and component_disk_name.endswith('__'):
                # skipping python special files
                continue
            component_full_path = os.path.join(path, component_disk_name)
            if os.path.isdir(component_full_path):
                component_name = ''.join(part.title() for part in component_disk_name.split('_'))
                component_import_path = '{}.{}.component.{}'.format(import_path, component_disk_name,
                                                                    component_name)
                try:
                    component_class = import_string(component_import_path)
                    component_instance = component_class()  # type: PluginUIComponent
                    if not isinstance(component_instance, PluginUIComponent):
                        raise TypeError('Component does not derives from base class.')
                except (ImportError, TypeError):
                    LOG.debug('Component folder structure invalid for {}'.format(component_full_path))
                else:
                    if not component_instance.disabled:
                        # if no features are specified assume they are enabled
                        features_enabled = len(component_instance.features) == 0
                        if not features_enabled:
                            # some features are specified, check them
                            if config_type == PluginConfigTypes.enduser:
                                features_enabled = active_features.is_at_least_one_feature_enabled(
                                    component_instance.features
                                )
                            else:
                                features_enabled = staff_active_features.is_at_least_one_feature_enabled(
                                    component_instance.features
                                )

                        if features_enabled:
                            if component_instance.initialize(
                                config_type=config_type,
                                plugin_definition=self,
                                component_name=component_name,
                                frontend_files_base_name=component_disk_name.replace('_', ''),
                                frontend_files_path=component_full_path
                            ):
                                found_components[component_name] = component_instance
                                LOG.info('Loaded component {} for plugin {}'.format(component_name, self.app_label))
                            else:
                                LOG.error('Failed to initialize component {}, ignoring'.format(component_name))
                        else:
                            LOG.info('Features for component {} are disabled, ignoring'.format(component_name))
                    else:
                        LOG.info('Component {} is disabled, ignoring'.format(component_name))
            else:
                if os.path.isfile(component_full_path):
                    service = PluginUIService()
                    if service.initialize(
                        service_file_name=component_disk_name,
                        frontend_files_path=path
                    ):
                        found_services[service.service_name] = service

        return found_components, found_services

    def refresh_components(self):
        app = apps.get_app_config(self.app_label)
        found_components, found_services = self.load_components_and_services(
            path=os.path.join(app.path, 'enduser/frontend/components'),
            import_path='{}.enduser.frontend.components'.format(self.app_name),
            config_type=PluginConfigTypes.enduser
        )
        self.components[PluginConfigTypes.enduser] = found_components
        self.services[PluginConfigTypes.enduser] = found_services
        enduser_states = PluginUIStates()
        if enduser_states.initialize(os.path.join(app.path, 'enduser/frontend/components')):
            self.states[PluginConfigTypes.enduser] = enduser_states

        found_components, found_services = self.load_components_and_services(
            path=os.path.join(app.path, 'staff/frontend/components'),
            import_path='{}.staff.frontend.components'.format(self.app_name),
            config_type=PluginConfigTypes.staff
        )
        self.components[PluginConfigTypes.staff] = found_components
        self.services[PluginConfigTypes.staff] = found_services
        staff_states = PluginUIStates()
        if staff_states.initialize(os.path.join(app.path, 'staff/frontend/components')):
            self.states[PluginConfigTypes.staff] = staff_states
