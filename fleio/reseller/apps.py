from django.utils.translation import ugettext_lazy as _

from importlib import import_module

from django.apps import AppConfig

from fleio.billing.modules.definition import BillingModuleDefinition
from fleio.core.plugins.plugin_definition import PluginDefinition


class ResellerConfig(AppConfig):
    name = 'fleio.reseller'

    verbose_name = 'Fleio reseller'

    module_definition = BillingModuleDefinition(
        module_name='Reseller Module',
        import_path='fleio.reseller.billing_module',
        class_name='ResellerBillingModule'
    )

    plugin_definition = None

    @classmethod
    def initialize_plugin(cls) -> PluginDefinition:
        if not cls.plugin_definition:
            cls.plugin_definition = PluginDefinition(
                display_name=_('Reseller'),
                app_name=cls.name,
                app_label='reseller',
                feature_name='billing.reseller',
                staff_feature_name='billing.reseller',
            )

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
        self.load_module('activitylog')
