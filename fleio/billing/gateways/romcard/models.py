from django.db import models

from fleio.core.models import Client


class RecurringPayments(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE, db_index=True, related_name='+')
    active = models.BooleanField(default=False)
    # custom to romcard
    first_payment = models.BooleanField(default=True, db_index=True)
    recur_ref = models.CharField(max_length=255, null=True)
    int_ref = models.CharField(max_length=255, null=True)

    objects = models.Manager
