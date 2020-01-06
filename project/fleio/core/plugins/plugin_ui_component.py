import logging
import os
import re

from typing import Dict
from typing import Optional
from typing import Tuple

from rest_framework.serializers import Serializer

from fleio.core.plugins.plugin_ui_utils import PluginUIUtils

LOG = logging.getLogger(__name__)


class PluginUIComponent(object):
    disabled = False
    parent_obj_name = None
    parent_obj_type = None
    model_manager = None
    required_services = []
    reverse_relation_name = None
    serializer_class = None
    features = []

    def __init__(self):
        self.config_type = None
        self.plugin_definition = None
        self.component_name = None
        self.frontend_files_path = None
        self.frontend_files_base_name = None
        self.html_file_path = None
        self.js_file_path = None
        self.has_dialogs = False
        self.dialogs_path = None

    def initialize(
            self,
            config_type: str,
            plugin_definition: object,
            component_name: str,
            frontend_files_base_name: str,
            frontend_files_path: str
    ):
        self.config_type = config_type
        self.plugin_definition = plugin_definition
        self.component_name = component_name
        self.frontend_files_base_name = frontend_files_base_name
        self.frontend_files_path = frontend_files_path
        self.html_file_path = os.path.join(
            self.frontend_files_path,
            '{}.html'.format(self.frontend_files_base_name)
        )
        self.js_file_path = os.path.join(
            self.frontend_files_path,
            '{}.component.js'.format(self.frontend_files_base_name)
        )
        self.dialogs_path = os.path.join(self.frontend_files_path, 'dialogs')
        self.has_dialogs = os.path.isdir(self.dialogs_path)

        return os.path.isfile(self.html_file_path) and os.path.isfile(self.js_file_path)

    def create_serializer(self, plugin_data: Dict, **kwargs) -> Optional[Serializer]:
        return None

    def get_javascript(self) -> Tuple[str, bool]:
        try:
            # TODO: throw exception if expected files are not found
            js = PluginUIUtils.read_file(path=self.js_file_path)
            html = PluginUIUtils.read_file(path=self.html_file_path).replace('\n', '').replace('\'', '\\\'')
            js = re.sub(
                '^.*templateUrl:.*$',
                '      template:\'{}\','.format(html),
                js,
                count=1,
                flags=re.MULTILINE,
            )

            if self.has_dialogs:
                # TODO: create python class for dialog and load when initializing plugin definition
                for dialog_name in os.listdir(self.dialogs_path):
                    file_name_base = dialog_name.replace('_', '')
                    dialog_html_file_name = '{}.html'.format(file_name_base)
                    dialog_html_file_path = os.path.join(
                        self.dialogs_path,
                        dialog_name,
                        dialog_html_file_name
                    )
                    dialog_js_file_path = os.path.join(
                        self.dialogs_path,
                        dialog_name,
                        '{}.controller.js'.format(file_name_base)
                    )
                    dialog_js = PluginUIUtils.read_file(path=dialog_js_file_path)
                    dialog_html = PluginUIUtils.read_file(
                        path=dialog_html_file_path
                    ).replace('\n', '').replace("'", "\\'")
                    regex = '^.*templateUrl:.*{}.*$'.format(file_name_base)
                    js = re.sub(
                        regex,
                        'template:\'{}\','.format(dialog_html),
                        js,
                        count=1,
                        flags=re.MULTILINE,
                    )

                    js = dialog_js + js

            # add services
            plugin_services = self.plugin_definition.services[self.config_type]
            for service_name in self.required_services:
                if service_name in plugin_services:
                    service = plugin_services[service_name]
                    service_js, js_loaded = service.get_javascript()
                    if js_loaded:
                        js = service_js + js

            return js, True
        except OSError:
            return '', False

    def check_parent_object(self, **kwargs) -> bool:
        parent_object = kwargs.get(self.parent_obj_name, None) if self.parent_obj_name else None
        if parent_object and self.parent_obj_type and type(parent_object) is not self.parent_obj_type:
            LOG.error(
                '{} is of type {} instead of expected type{}'.format(
                    self.parent_obj_name,
                    type(parent_object),
                    self.parent_obj_type,
                ),
            )
            return False
        else:
            return True

    def create(self, **kwargs):
        if self.check_parent_object(**kwargs) and self.model_manager:
            component_data = kwargs.get('component_data', None)
            if component_data and isinstance(component_data, dict):
                parent_object = kwargs[self.parent_obj_name]
                if parent_object:
                    component_data[self.parent_obj_name] = parent_object
                self.model_manager.create(**component_data)
            else:
                LOG.error('Invalid component data for component {}'.format(self.component_name))
        else:
            LOG.error('Invalid parent object or model manager for component {}'.format(self.component_name))

    def update(self, **kwargs):
        if self.check_parent_object(**kwargs) and self.model_manager:
            component_data = kwargs.get('component_data', None)
            if component_data and isinstance(component_data, dict):
                parent_object = kwargs[self.parent_obj_name]
                if parent_object:
                    component_data[self.parent_obj_name] = parent_object
                self.model_manager.update(**component_data)
            else:
                LOG.error('Invalid component data for component {}'.format(self.component_name))
        else:
            LOG.error('Invalid parent object or model manager for component {}'.format(self.component_name))

    def delete(self, **kwargs):
        if self.check_parent_object(**kwargs) and self.model_manager:
            parent_object = kwargs[self.parent_obj_name]
            if parent_object:
                search_params = {
                    self.parent_obj_name: parent_object
                }
                self.model_manager.filter(**search_params).delete()
            else:
                LOG.error('Parent data is none for component {}'.format(self.component_name))
        else:
            LOG.error('Invalid parent object or model manager for component {}'.format(self.component_name))

    def get(self, **kwargs):
        if self.check_parent_object(**kwargs) and self.model_manager:
            parent_object = kwargs[self.parent_obj_name]
            if parent_object:
                search_params = {
                    self.parent_obj_name: parent_object
                }
                return self.model_manager.filter(**search_params).values().first()
            else:
                LOG.error('Parent data is none for component {}'.format(self.component_name))
        else:
            LOG.error('Invalid parent object or model manager for component {}'.format(self.component_name))

    def validate(self, **kwargs):
        # implement in derived classes, raise ValidationError if something is wrong
        del self, kwargs  # unused
