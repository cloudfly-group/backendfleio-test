from jsonfield import JSONField

from django.db import models
from django.utils.translation import ugettext_lazy as _

from fleio.core.models import Plugin


class ProductModule(models.Model):
    name = models.CharField(max_length=32, unique=True)
    description = models.CharField(max_length=255, default='')
    path = models.CharField(max_length=255, db_index=True, unique=True, help_text=_('Importable module path'))
    config = JSONField(default=dict())
    plugin = models.ForeignKey(Plugin, null=True, on_delete=models.SET_NULL, related_name='product_modules')

    @property
    def plugin_name(self):
        return self.plugin.app_name if self.plugin else None

    @property
    def plugin_label(self):
        return self.plugin.app_label if self.plugin else None

    def __str__(self):
        return self.name
