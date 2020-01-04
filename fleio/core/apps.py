from importlib import import_module

from django.apps import AppConfig


class CoreAppConfig(AppConfig):
    name = 'fleio.core'
    verbose_name = 'Fleio core app'

    def ready(self):
        from fleio.core import signals  # noqa
        from fleio.core import activitylog  # noqa
        from fleiostaff.core import signals  # noqa
        from fleiostaff.core import activitylog  # noqa
        import_module('fleio.core.permissions.user_permissions')
        import_module('fleio.core.permissions.signal_handlers')
