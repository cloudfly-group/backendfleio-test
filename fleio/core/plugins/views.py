from importlib import import_module

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from fleio.core.drf import EndUserOnly
from fleio.core.models import Plugin
from fleio.core.plugins.plugin_definition import PluginConfigTypes
from fleio.core.plugins.plugin_loader import plugin_loader
from fleio.core.plugins.plugin_utils import PluginUtils

from fleio.core.plugins.serializers import EnduserPluginSerializer


has_license = True

try:
    import_module('fleio.core.loginview')
except Exception as e:
    del e  # unused
    has_license = False


class EnduserPluginsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (EndUserOnly if has_license else AllowAny, )
    model = Plugin
    queryset = Plugin.objects.all()
    serializer_class = EnduserPluginSerializer

    @action(detail=False, methods=['get'])
    def plugins_with_component(self, request):
        component_name = request.query_params.get('component_name', None)
        labels = PluginUtils.get_plugins_labels_for_component(
            config_type=PluginConfigTypes.enduser,
            component_name=component_name,
        )

        plugins = self.queryset.filter(app_label__in=labels).all()

        return Response(
            data={
                'plugins': EnduserPluginSerializer(many=True).to_representation(plugins),
            }
        )

    @action(detail=False, methods=['get'])
    def plugins_with_notifications(self, request: Request):
        plugins_with_notifications = {
            'total_notification_count': 0,
            'plugins': [],
        }

        for plugin in plugin_loader.enduser_plugins.values():
            if 'PluginNotifications' in plugin.components[PluginConfigTypes.enduser]:
                component = plugin.components[PluginConfigTypes.enduser]['PluginNotifications']
                if hasattr(component, 'get_notification_count') and callable(component.get_notification_count):
                    notifications_count = component.get_notification_count(user=request.user)
                    plugins_with_notifications['plugins'].append(
                        {
                            'plugin': EnduserPluginSerializer().to_representation(instance=plugin.plugin_model),
                            'notification_count': notifications_count,
                        }
                    )
                    plugins_with_notifications['total_notification_count'] += notifications_count

        return Response(data=plugins_with_notifications)

    @action(detail=False, methods=['get'], permission_classes=(AllowAny,))
    def plugins_menu(self, request):
        del request  # unused
        if has_license:
            return Response(data=PluginUtils.get_plugins_menus(PluginConfigTypes.enduser))
        else:
            return Response(
                data={
                    'menus': [],
                    'menu_items': [],
                }
            )
