from django import apps
from django.utils.translation import ugettext_lazy as _

from fleio.billing.modules.definition import BillingModuleDefinition

from fleio.core.plugins.plugin_definition import MenuItem
from fleio.core.plugins.plugin_definition import PluginDefinition
from fleio.core.plugins.plugin_definition import PluginConfigTypes

from fleio.core.plugins.plugin_dispatcher import plugin_dispatcher


class TodoPluginConfig(apps.AppConfig):
    name = 'plugins.todo'
    verbose_name = 'Fleio TODO plugin'

    module_definition = BillingModuleDefinition(
        module_name='TODO Module',
        import_path='plugins.todo.billing_module',
        class_name='TodoModule'
    )

    plugin_definition = None

    @classmethod
    def initialize_plugin(cls) -> PluginDefinition:
        if not cls.plugin_definition:
            # register signals
            from plugins.todo import signals
            plugin_dispatcher.register_signal('todo', 'todo_created', signals.todo_created)
            plugin_dispatcher.register_signal('todo', 'todo_deleted', signals.todo_deleted)
            plugin_dispatcher.register_signal('todo', 'todo_updated', signals.todo_updated)

            # register functions
            from plugins.todo import utils
            plugin_dispatcher.register_function(
                'todo', 'create_todo', utils.create_todo_for_external_caller, ['title', 'description']
            )

            definition = PluginDefinition(
                display_name=_('TODO'),
                app_name=cls.name,
                app_label='todo',
                feature_name='plugins.todo',
                staff_feature_name='plugins.todo',
            )

            definition.add_menu_item(config_type=PluginConfigTypes.staff, menu_item=MenuItem(
                label=_('TODOs'),
                state='pluginsTodoTodos',
                icon='todo',
                feature='plugins.todo',
                plugin_name='todo',
            ))

            definition.add_url_config(
                config_type=PluginConfigTypes.staff,
                module_name='plugins.todo.staff.urls',
                path='todo',
                namespace='todo'
            )

            cls.plugin_definition = definition

        return cls.plugin_definition
