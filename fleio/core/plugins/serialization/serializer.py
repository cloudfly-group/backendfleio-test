import logging

from rest_framework import serializers

from fleio.core.plugins.plugin_utils import PluginUtils


LOG = logging.getLogger(__name__)


class ComponentDataSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not hasattr(self, 'Meta') or self.Meta.plugin_config_type is None or self.Meta.component_name is None:
            # component_name and plugin_config_type should be defined in serializer Meta class
            raise Exception('Serializer meta does contain component information')

        plugins = PluginUtils.get_plugins_for_component(
            config_type=self.Meta.plugin_config_type,
            component_name=self.Meta.component_name
        )

        for plugin in plugins:  # PluginDefinition
            component = plugin.components[self.Meta.plugin_config_type].get(self.Meta.component_name)
            if component.reverse_relation_name is None or component.serializer_class is None:
                LOG.warning('Component does not define serializer class or reverse relation name, skipping')
                continue

            if 'data' in kwargs:
                data = kwargs['data']
                component_data = data[component.reverse_relation_name]
                # TODO: see if this is safe
                component_data[component.parent_obj_name] = data['id']
                self.fields[component.reverse_relation_name] = component.serializer_class(
                    data=component_data
                )
            else:
                self.fields[component.reverse_relation_name] = component.serializer_class()

    def update(self, instance, validated_data):
        super().update(instance, validated_data)

    def create(self, validated_data):
        super().create(validated_data)

    def save_component_data(self, instance):
        plugins = PluginUtils.get_plugins_for_component(
            config_type=self.Meta.plugin_config_type,
            component_name=self.Meta.component_name
        )

        for plugin in plugins:  # PluginDefinition
            component = plugin.components[self.Meta.plugin_config_type].get(self.Meta.component_name)
            if component.reverse_relation_name is None or component.serializer_class is None:
                LOG.warning('Component does not define serializer class or reverse relation name, skipping')
                continue

            component_data_serializer = self.fields[component.reverse_relation_name]
            if hasattr(instance, component.reverse_relation_name):
                if component_data_serializer.is_valid(raise_exception=True):
                    update_serializer = component.serializer_class(
                        instance=getattr(instance, component.reverse_relation_name)
                    )
                    validated_data = component_data_serializer.validated_data
                    del validated_data[component.parent_obj_name]
                    update_serializer.update(
                        instance=getattr(instance, component.reverse_relation_name),
                        validated_data=validated_data,
                    )
            else:
                setattr(component_data_serializer, component.parent_obj_name, instance)
                if component_data_serializer.is_valid(raise_exception=True):
                    component_data_serializer.save()
