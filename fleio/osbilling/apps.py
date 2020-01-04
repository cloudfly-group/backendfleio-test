from logging import getLogger
from importlib import import_module

from django import apps


LOG = getLogger(__name__)


class AppConfig(apps.AppConfig):
    name = 'fleio.osbilling'
    verbose_name = 'Billing app'

    def load_module(self, name, quiet=True):
        full_name = '%s.%s' % (self.name, name)
        try:
            import_module(full_name)
        except ImportError:
            if quiet:
                return None
            raise

    def ready(self):
        self.load_module('signals')
