from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from jsonfield import JSONField


@python_2_unicode_compatible
class SubnetPool(models.Model):
    id = models.CharField(max_length=36, db_index=True, primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    project_id = models.CharField(max_length=36, null=True, blank=True, db_index=True)
    region = models.CharField(max_length=128, db_index=True)
    prefixes = JSONField(default=list())
    ip_version = models.PositiveSmallIntegerField(choices=((4, 'IPv4'), (6, 'IPv6')))
    default_prefixlen = models.PositiveSmallIntegerField()
    min_prefixlen = models.PositiveSmallIntegerField()
    max_prefixlen = models.PositiveSmallIntegerField()
    shared = models.BooleanField(default=False)
    default_quota = models.IntegerField(null=True, blank=True)
    address_scope_id = models.UUIDField(max_length=36, null=True, blank=True, db_index=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    sync_version = models.BigIntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return "{} - {} - {}".format(self.id, self.name, self.description)
