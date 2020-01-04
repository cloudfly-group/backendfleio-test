import logging
from typing import List

from rest_framework import serializers

from django.db import transaction

from fleio.core.models import Plugin
from fleio.core.plugins.plugin_utils import PluginUtils

LOG = logging.getLogger(__name__)


class ComponentDataModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        plugins = PluginUtils.get_plugins_for_component(
            config_type=self.Meta.plugin_config_type,
            component_name=self.Meta.component_name
        )

        for plugin in plugins:  # PluginDefinition
            component = plugin.components[self.Meta.plugin_config_type].get(self.Meta.component_name)
            if component.reverse_relation_name is None or component.serializer_class is None:
                LOG.warning('Component does not define serializer class or reverse relation name, skipping')
                continue

            if self.Meta.fields != '__all__' and component.reverse_relation_name not in self.Meta.fields:
                self.Meta.fields += (component.reverse_relation_name, )
        super().__init__(*args, **kwargs)

        if not hasattr(self, 'Meta') or self.Meta.plugin_config_type is None or self.Meta.component_name is None:
            # component_name and plugin_config_type should be defined in serializer Meta class
            raise Exception('Serializer meta does contain component information')

        data = kwargs.get('data', None)
        partial = kwargs.get('partial', False)
        update = self.instance is not None and data is not None
        self.component_fields = {}
        for plugin in plugins:  # PluginDefinition
            component = plugin.components[self.Meta.plugin_config_type].get(self.Meta.component_name)
            if component.reverse_relation_name is None or component.serializer_class is None:
                LOG.warning('Component does not define serializer class or reverse relation name, skipping')
                continue

            if update:
                # performing an update
                if component.reverse_relation_name not in data:
                    # serializer has no data for component, ignoring
                    continue

                self.component_fields[component.reverse_relation_name] = component.serializer_class(
                    data=data[component.reverse_relation_name],
                    instance=getattr(self.instance, component.reverse_relation_name, None),
                    partial=partial
                )

                continue

            if data:
                # performing a create
                if component.reverse_relation_name not in data:
                    # serializer has no data for component, ignoring
                    continue

                component_data_serializer = component.serializer_class(
                    data=data[component.reverse_relation_name],
                )

                self.component_fields[component.reverse_relation_name] = component_data_serializer

                continue

            if self.instance:
                # performing a retrieve
                if hasattr(self.instance, component.reverse_relation_name):
                    self.fields[component.reverse_relation_name] = component.serializer_class(
                        instance=getattr(self.instance, component.reverse_relation_name, None)
                    )

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

            if component.reverse_relation_name in self.component_fields:
                component_data_serializer = self.component_fields[component.reverse_relation_name]
                if component_data_serializer.instance:
                    # performing an update
                    if component_data_serializer.is_valid(raise_exception=True):
                        component_data_serializer.save()
                else:
                    # performing an create
                    component_data_serializer = self.component_fields[component.reverse_relation_name]
                    component_data_serializer.initial_data[component.parent_obj_name] = instance.id
                    if component_data_serializer.is_valid(raise_exception=True):
                        component_data_serializer.save()

    def save(self, **kwargs):
        with transaction.atomic():
            super().save()
            self.save_component_data(self.instance)

    def cleanup_component_data(self, keep_for_plugins: List[Plugin] = None):
        if keep_for_plugins is None:
            keep_for_plugins = []

        if self.instance is None:
            LOG.error('Cleanup component data called with no instance, aborting')
            return

        plugins = PluginUtils.get_plugins_for_component(
            config_type=self.Meta.plugin_config_type,
            component_name=self.Meta.component_name
        )

        data_deleted = False
        for plugin in plugins:  # PluginDefinition
            component = plugin.components[self.Meta.plugin_config_type].get(self.Meta.component_name)
            if component.reverse_relation_name is None or component.serializer_class is None:
                LOG.warning('Component does not define serializer class or reverse relation name, skipping')
                continue

            if plugin.plugin_model in keep_for_plugins:
                continue

            component_data_instance = getattr(self.instance, component.reverse_relation_name, None)
            if component_data_instance is not None:
                component_data_instance.delete()
                setattr(self.instance, component.reverse_relation_name, None)
                data_deleted = True

        if data_deleted:
            self.instance.save()
