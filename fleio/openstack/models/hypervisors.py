from django.db import models


class Hypervisor(models.Model):
    id = models.CharField(max_length=64, unique=True, db_index=True, primary_key=True)
    host_ip = models.CharField(max_length=64, null=True, blank=True)
    host_name = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    memory_mb = models.IntegerField()
    local_gb = models.IntegerField()
    region = models.CharField(max_length=128, db_index=True)
    sync_version = models.BigIntegerField(default=0)
    hypervisor_type = models.CharField(max_length=32, default=None)

    class Meta:
        verbose_name_plural = 'Hypervisors'

    def __str__(self):
        if self.host_name:
            return 'Hypervisor {}'.format(self.host_name)
        return 'Hypervisor'
