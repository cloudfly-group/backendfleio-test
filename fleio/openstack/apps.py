from importlib import import_module

from django import apps
from django.utils.translation import ugettext_lazy as _

from fleio.activitylog.formatting import logclass_text

from fleio.billing.modules.definition import BillingModuleDefinition

from fleio.core.plugins.plugin_definition import PluginDefinition
from fleio.core.plugins.plugin_definition import PluginConfigTypes
from fleio.core.operations_base.operation_factory import operations_factory


class AppConfig(apps.AppConfig):
    name = 'fleio.openstack'
    verbose_name = 'Fleio openstack application'

    module_definition = BillingModuleDefinition(
        module_name='Openstack Module',
        import_path='fleio.openstack.billing_module',
        class_name='OpenstackModule'
    )

    plugin_definition = None

    @classmethod
    def initialize_operations(cls):
        from fleio.openstack.volumes.operations import VolumeRestoration
        from fleio.openstack.instances.operations import InstanceDeletion
        operations_factory.register_class(operation_class=VolumeRestoration)
        operations_factory.register_class(operation_class=InstanceDeletion)

    @classmethod
    def initialize_plugin(cls) -> PluginDefinition:
        if not cls.plugin_definition:
            definition = PluginDefinition(
                display_name=_('Openstack'),
                app_name=cls.name,
                app_label='openstack',
                feature_name='openstack',
                staff_feature_name='openstack',
            )

            definition.add_url_config(
                config_type=PluginConfigTypes.enduser,
                module_name='fleio.openstack.urls',
                path='',
                namespace='openstack',
                base_path='',
            )

            definition.add_url_config(
                config_type=PluginConfigTypes.staff,
                module_name='fleiostaff.openstack.urls',
                path='',
                namespace='openstack',
                base_path='',
            )

            cls.plugin_definition = definition

        return cls.plugin_definition

    def load_module(self, name, quiet=True):
        full_name = '%s.%s' % (self.name, name)
        try:
            import_module(full_name)
        except ImportError:
            if quiet:
                return None
            raise

    def ready(self):
        self.load_module('signals.handlers')
        self.load_module('activitylog')

        logclass_text['openstack update credentials'] = _(
            'Staff user {username} ({user_id}) updated openstack credentials.',
        )

        logclass_text['volume extra details synchronization'] = _(
            'Volume {volume_id} extra details synchronization.',
        )

        logclass_text['volume backup extra details synchronization'] = _(
            'Volume backup {backup_id} extra details synchronization.',
        )
