from django.db import models

from fleio.billing.models import Service


class ServiceAssignedIP(models.Model):
    """Any assigned IPs for a service if the service module supports it"""
    service = models.ForeignKey(Service, related_name='assigned_ips', db_index=True, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
