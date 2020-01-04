from jsonfield import JSONField

from django.db import models

from .gateway import Gateway


class GatewayLog(models.Model):
    gateway = models.ForeignKey(Gateway, related_name='gateway_logs', on_delete=models.CASCADE)
    error = models.BooleanField(default=False)
    error_code = models.CharField(max_length=16, blank=True, null=True)
    error_info = models.TextField(blank=True, null=True)
    external_id = models.CharField(max_length=64, null=True, blank=True)
    status = models.CharField(max_length=255)
    data = JSONField()

    def __str__(self):
        return '{} - {} - {}'.format(self.gateway.name, self.external_id, self.status)
