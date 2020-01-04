import logging

from django import apps

LOG = logging.getLogger(__name__)


class AppConfig(apps.AppConfig):
    name = 'fleio.osbackup'

    def ready(self):
        try:
            # noinspection PyUnresolvedReferences
            from . import urls  # noqa
        except ImportError as e:
            LOG.error('Unable to import osbackup urls: {}'.format(e))
