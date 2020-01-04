from django.db import models

from fleio.core.models import Client


class RecurringPaymentsOrder(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, db_index=True)
    gateway_name = models.CharField(max_length=255, db_index=True)
    order = models.IntegerField(default=None, null=True)

    objects = models.Manager

    class Meta:
        unique_together = ('gateway_name', 'client')
