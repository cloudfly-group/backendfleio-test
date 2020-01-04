from logging import getLogger
from django import apps


LOG = getLogger(__name__)


class AppConfig(apps.AppConfig):
    name = 'fleio.reports'
    verbose_name = 'Fleio reports'
