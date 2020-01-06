from django.db import models


class OpenstackRegionManager(models.Manager):
    def enabled(self):
        return self.filter(enabled=True)

    def enabled_for_enduser(self):
        return self.filter(enabled=True, disable_for_enduser=False)

    def for_volumes(self):
        return self.enabled().filter(enable_volumes=True)

    def for_snapshots(self):
        return self.enabled().filter(enable_snapshots=True)


class OpenstackRegion(models.Model):
    id = models.CharField(max_length=64, unique=True, primary_key=True)
    description = models.CharField(max_length=255, blank=True)
    parent_region_id = models.CharField(max_length=64, blank=True)
    extra = models.TextField(blank=True)
    enabled = models.BooleanField(default=True, blank=True)
    enable_volumes = models.BooleanField(default=True, blank=True)
    enable_snapshots = models.BooleanField(default=True, blank=True)
    disable_for_enduser = models.BooleanField(default=False, blank=True)

    objects = OpenstackRegionManager()

    class Meta:
        verbose_name_plural = 'Regions'

    def __str__(self):
        return self.id
