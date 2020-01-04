import logging

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from django.http import HttpResponse

from fleio.core.plugins.plugin_utils import PluginUtils


LOG = logging.getLogger(__name__)


class FrontendViewBase(viewsets.GenericViewSet):
    permission_classes = (AllowAny, )  # we allow any since this views will only return UI components
    config_type = None
    plugin_label = None

    @action(detail=False, methods=['GET'])
    def get_service(self, request: Request):
        service_name = request.query_params.get('service', None)
        service_instance = PluginUtils.get_service(
            config_type=self.config_type,
            plugin_label=self.plugin_label,
            service_name=service_name,
        )
        if service_instance:
            service_data, found = service_instance.get_javascript()

            if found:
                return Response(data={
                    'data': service_data
                })
            else:
                LOG.error('Service javascript not found for plugin {}:{}'.format(self.config_type, self.plugin_label))
                return HttpResponse(status=204)
        else:
            LOG.error('Service not registered for plugin {}:{}'.format(self.config_type, self.plugin_label))
            return HttpResponse(status=204)

    @action(detail=False, methods=['GET'])
    def get_component(self, request: Request):
        component_name = request.query_params.get('component', None)
        component_instance = PluginUtils.get_component(
            config_type=self.config_type,
            plugin_label=self.plugin_label,
            component_name=component_name,
        )
        if component_instance:
            component_data, found = component_instance.get_javascript()

            if found:
                return Response(data={
                    'data': component_data
                })
            else:
                LOG.error('Component javascript not found for plugin {}:{}'.format(self.config_type, self.plugin_label))
                return HttpResponse(status=204)
        else:
            LOG.error('Component not registered for plugin {}:{}'.format(self.config_type, self.plugin_label))
            return HttpResponse(status=204)

    @action(detail=False, methods=['GET'])
    def get_components(self, request: Request):
        component_names = request.query_params.get('components', None)  # type: str

        if not component_names:
            return HttpResponse(status=204)

        component_names_list = component_names.split(',')
        component_names_list = list(set(component_names_list))
        components_data = {}

        for component_name in component_names_list:
            component_instance = PluginUtils.get_component(
                config_type=self.config_type,
                plugin_label=self.plugin_label,
                component_name=component_name,
            )
            if component_instance:
                component_data, found = component_instance.get_javascript()

                if found:
                    components_data[component_instance.component_name] = component_data
                else:
                    LOG.error('Component {} javascript not found for plugin {}:{}'.format(
                        component_name,
                        self.config_type,
                        self.plugin_label,
                    ))
            else:
                LOG.error('Component {} not registered for plugin {}:{}'.format(
                    component_name,
                    self.config_type,
                    self.plugin_label,
                ))

        if len(components_data) > 0:
            return Response(data={
                'components': components_data
            })
        else:
            return HttpResponse(status=204)

    @action(detail=False, methods=['GET'])
    def get_states(self, request: Request):
        del request  # unused
        plugin_instance = PluginUtils.get_plugin(
            config_type=self.config_type,
            plugin_label=self.plugin_label,
        )
        if plugin_instance and self.config_type in plugin_instance.states:
            states_data, found = plugin_instance.states[self.config_type].get_javascript()

            if found:
                return Response(data={
                    'states': states_data
                })
            else:
                LOG.error('States javascript found for plugin {}:{}'.format(self.config_type, self.plugin_label))
                return HttpResponse(status=204)
        else:
            LOG.error('States not found for plugin {}:{}'.format(self.config_type, self.plugin_label))
            return HttpResponse(status=204)

    @action(detail=False, methods=['GET'])
    def get_all_ui(self, request: Request):
        del request  # unused
        return Response()
