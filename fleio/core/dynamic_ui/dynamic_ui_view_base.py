import copy

from django.conf import settings

from typing import Tuple

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from fleio.core.plugins.plugin_config_types import PluginConfigTypes
from fleio.core.plugins.plugin_utils import PluginUtils


class DynamicUIViewBase(viewsets.GenericViewSet):
    permission_classes = (AllowAny, )  # we allow any since this views will only return UI components
    config_type = PluginConfigTypes.undefined

    @action(detail=False, methods=['get'])
    def plugin_data(self, request: Request):
        del request  # unused
        menu_data = PluginUtils.get_plugins_menus(self.config_type)
        plugin_names = []
        plugin_states = {}
        plugin_components = {}
        plugins = PluginUtils.get_plugins(self.config_type)
        for plugin_name in plugins:
            plugin_names.append(plugin_name)
            plugin = plugins[plugin_name]
            if self.config_type in plugin.states:
                states_data, found = plugin.states[self.config_type].get_javascript()
                if found:
                    plugin_states[plugin_name] = states_data
            if self.config_type in plugin.components:
                components = plugin.components[self.config_type]
                plugin_components[plugin_name] = {}
                for component_name in components:
                    component_data, found = components[component_name].get_javascript()
                    if found:
                        plugin_components[plugin_name][component_name] = component_data

        return Response(data={
            'menu_data': menu_data,
            'plugin_names': plugin_names,
            'plugin_states': plugin_states,
            'plugin_components': plugin_components,
        })

    @staticmethod
    def _get_menu_data(custom_menu_options: list, custom_menu_categories: dict) -> Tuple[list, list]:
        menu_data = list()
        custom_links_under_category = list()
        if len(custom_menu_options):
            for option in custom_menu_options:
                if option.get('category', None):
                    if custom_menu_categories.get(option['category'], None):
                        if 'items' not in custom_menu_categories[option['category']]:
                            custom_menu_categories[option['category']]['items'] = list()
                        custom_menu_categories[option['category']]['items'].append(option)
                    else:
                        custom_links_under_category.append(option)
                else:
                    menu_data.append(option)
            for category, category_data in custom_menu_categories.items():
                category_data['category'] = category
                menu_data.append(category_data)
        return menu_data, custom_links_under_category

    @action(detail=False, methods=['get'])
    def custom_menu_links(self, request: Request):
        del request  # unused
        custom_menu_options_enduser = copy.deepcopy(settings.CUSTOM_MENU_OPTIONS_ENDUSER)  # type: list
        custom_menu_categories_enduser = copy.deepcopy(settings.CUSTOM_MENU_CATEGORIES_ENDUSER)  # type: dict
        custom_menu_options_staff = copy.deepcopy(settings.CUSTOM_MENU_OPTIONS_STAFF)  # type: list
        custom_menu_categories_staff = copy.deepcopy(settings.CUSTOM_MENU_CATEGORIES_STAFF)  # type: dict
        menu_data_enduser, custom_links_under_category_enduser = self._get_menu_data(
            custom_menu_options=custom_menu_options_enduser,
            custom_menu_categories=custom_menu_categories_enduser,
        )
        menu_data_staff, custom_links_under_category_staff = self._get_menu_data(
            custom_menu_options=custom_menu_options_staff,
            custom_menu_categories=custom_menu_categories_staff,
        )

        return Response(data={
            'custom_menu_enduser': {
                'menu_data': menu_data_enduser,
                'links_inside_category': custom_links_under_category_enduser,
            },
            'custom_menu_staff': {
                'menu_data': menu_data_staff,
                'links_inside_category': custom_links_under_category_staff,
            },
        })
