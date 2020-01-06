import logging

from django.apps import apps
from django.db import IntegrityError
from django.utils.module_loading import import_string

from fleio.billing.exceptions import ModuleNotFoundException
from fleio.billing.models import Product
from fleio.billing.models import ProductModule
from fleio.billing.models import Service
from fleio.billing.modules.base import ModuleBase
from fleio.billing.modules.definition import BillingModuleDefinition
from fleio.billing.modules.null import NullModule
from fleio.billing.modules.universal import UniversalModule

from fleio.core.plugins.plugin_utils import PluginUtils

LOG = logging.getLogger(__name__)

IMPORT_BEFORE_GET = True
MODULE_DEFINITION_ATTRIBUTE = 'module_definition'


class RegisteredModule:
    def __init__(self, module_id, import_path):
        self.id, self.import_path = module_id, import_path
        self.module_class = import_string(self.import_path)

        if not IMPORT_BEFORE_GET:
            self.instance = self.module_class()
            self.reseller_usage_instance = self.module_class(reseller_usage=True)

    def get_module_instance(self, reseller_usage: bool = False):
        if IMPORT_BEFORE_GET:
            self.module_class = import_string(self.import_path)
            self.instance = self.module_class()
            self.reseller_usage_instance = self.module_class(reseller_usage=True)

        if reseller_usage:
            return self.reseller_usage_instance
        else:
            return self.instance

    @property
    def module_name(self):
        return self.module_class.module_name


class ModuleFactory:
    def __init__(self):
        LOG.debug('Creating module factory ...')
        self.modules_by_id = {}

    def refresh_modules(self):
        self.register_modules_from_apps()
        self.register_default_modules()

    def register_modules_from_apps(self):
        LOG.debug('Searching apps for billing modules ...')

        for app in apps.get_app_configs():
            if not hasattr(app, MODULE_DEFINITION_ATTRIBUTE):
                continue

            LOG.info('Processing app ''{}'''.format(app.name))

            module_definition = getattr(app, MODULE_DEFINITION_ATTRIBUTE)  # type: BillingModuleDefinition
            if not type(module_definition) is BillingModuleDefinition:
                LOG.error('Attribute {} does not have correct type, skipping'.format(MODULE_DEFINITION_ATTRIBUTE))
                continue

            if not module_definition.try_import():
                LOG.error('Failed to import module {}, skipping'.format(module_definition.module_name))
                continue

            module_path = '{}.{}'.format(module_definition.import_path, module_definition.class_name)
            self.register_module_safe(module_path, module_definition.module_name)

    def register_default_modules(self):
        LOG.debug("Registering universal module ...")
        self.register_module_safe('fleio.billing.modules.universal.UniversalModule', UniversalModule.module_name)

    def register_module(self, import_path, name):
        LOG.debug('Register called for ''{}'' -> {}'.format(name, import_path))

        product_module = ProductModule.objects.filter(path=import_path).first()
        plugin_definition = PluginUtils.get_plugin_definition_for_module_path(module_path=import_path)
        if product_module is None:
            LOG.debug('Product module not found in database by path, checking by name')
            product_module = ProductModule.objects.filter(name=name).first()

            if product_module is None:
                LOG.debug('Product module not found in database, creating')
                product_module = ProductModule.objects.create(
                    name=name,
                    path=import_path,
                    plugin=None if plugin_definition is None else plugin_definition.plugin_model
                )
            else:
                LOG.debug('Product module found in database by name, updating path')
                product_module.path = import_path
                product_module.plugin = plugin_definition.plugin_model
                product_module.save()

        else:
            if product_module.id in self.modules_by_id:
                LOG.debug('Module already registered, skipping')
                return

            if product_module.name != name:
                LOG.warning('Product names do not match, updating name')
                product_module.name = name
                product_module.save()

            if plugin_definition and product_module.plugin != plugin_definition.plugin_model:
                LOG.warning('Product plugins do not match, updating plugin')
                product_module.plugin = plugin_definition.plugin_model
                product_module.save()

        module_id = product_module.id
        self.modules_by_id[module_id] = RegisteredModule(module_id, import_path)
        LOG.debug('Module registered')

    def register_module_safe(self, import_path: str, name: str):
        try:
            self.register_module(import_path, name)
        except IntegrityError:
            # if integrity error was raised then probably module was registered from another process during
            # register_module call
            # a new call to register_module should succeed since it will look for existing modules
            LOG.debug('Integrity error when attempting to register module, retrying')
            self.register_module(import_path, name)

    def get_module_instance(
            self, product_module: ProductModule = None, product: Product = None, service: Service = None,
            reseller_usage: bool = False
    ) -> ModuleBase:
        if product_module is None:
            if product is None:
                product_module = service.product.module
            else:
                product_module = product.module

        if product_module is None:
            LOG.error('No product module provided')
            raise ValueError('At least one of product_module, product or service arguments should be provided')

        if product_module.id not in self.modules_by_id:
            LOG.error('Module not found, returning null module')
            # we return null module here in case module was not found
            # this should happen only if an app that provides a module was removed from fleio after some services
            # were created for that app
            return NullModule()

        registered_module = self.modules_by_id[product_module.id]  # type: RegisteredModule
        if product_module.path != registered_module.import_path:
            LOG.error('Module path changed {0} -> {1}'.format(product_module.path, registered_module.import_path))
            raise ModuleNotFoundException('Module path changed')

        return registered_module.get_module_instance(reseller_usage=reseller_usage)

    def has_module(self, import_path=None, module_name=None):
        if import_path is None and module_name is None:
            return False

        for module_id, registered_module in self.modules_by_id.items():
            if registered_module.import_path == import_path or registered_module.module_name == module_name:
                return True

        return False


module_factory = ModuleFactory()
