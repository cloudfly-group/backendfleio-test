import uuid
from django.db import models
from django.utils.translation import ugettext_lazy as _
from jsonfield import JSONField

from fleio.core.models import Plugin
from .server_group import ServerGroup


class ServerStatus:
    enabled = 'enabled'
    disabled = 'disabled'

    CHOICES = [
        (enabled, _('Enabled')),
        (disabled, _('Disabled'))
    ]


class ServerQuerySet(models.QuerySet):
    def enabled(self):
        return self.filter(status=ServerStatus.enabled)


class Server(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    group = models.ForeignKey(ServerGroup, related_name='servers', on_delete=models.PROTECT)
    plugin = models.ForeignKey(Plugin, related_name='servers', null=True, db_index=True, on_delete=models.CASCADE)
    status = models.CharField(choices=ServerStatus.CHOICES, max_length=8, db_index=True)
    settings = JSONField(default={})
    created_at = models.DateTimeField(auto_now_add=True)

    objects = ServerQuerySet.as_manager()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
