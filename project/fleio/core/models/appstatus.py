import json
from django.db import models
from django.utils import timezone


class StatusTypesMap:
    updated_messages_count = 'updated_messages_count'


class AppStatus(models.Model):
    details = models.CharField(max_length=10240, null=True)
    last_updated = models.DateTimeField(default=timezone.now)
    status_type = models.CharField(max_length=48, blank=False, null=False, unique=True)

    class Meta:
        verbose_name_plural = 'App statuses'

    @property
    def details_as_dict(self):
        return json.loads(self.details)

    def __str__(self):
        return 'App status'
