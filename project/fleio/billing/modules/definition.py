from importlib import import_module
import logging

LOG = logging.getLogger(__name__)


class BillingModuleDefinition(object):
    def __init__(self, module_name: str, import_path: str, class_name: str):
        self.module_name = module_name
        self.import_path = import_path
        self.class_name = class_name

    def try_import(self) -> bool:
        try:
            import_module(self.import_path)
            return True
        except Exception as e:
            LOG.exception('Exception {} when attempting to load module {}'.format(e, self.module_name))
            return False
