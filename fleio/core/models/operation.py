from django.db import models
from django.utils.timezone import now


class Operation(models.Model):
    operation_type = models.CharField(max_length=255, null=False, blank=False, db_index=True)
    params = models.CharField(max_length=10240, null=True)
    primary_object_id = models.CharField(max_length=36, null=True, blank=False)
    created_at = models.DateTimeField(default=now)
    status = models.CharField(max_length=32, null=True, blank=True)
    completed = models.BooleanField(default=False, db_index=True)

    objects = models.Manager

    def __str__(self):
        return self.operation_type
