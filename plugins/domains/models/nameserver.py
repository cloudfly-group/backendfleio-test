from django.db import models


class Nameserver(models.Model):
    host_name = models.CharField(max_length=255, unique=True, db_index=True)
    ipv4 = models.GenericIPAddressField(null=True, blank=True)
    ipv6 = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
