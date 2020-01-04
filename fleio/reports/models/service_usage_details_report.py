from django.db import models
from jsonfield import JSONField

from .service_report import ServiceRevenueReport


class ServiceUsageDetailsReport(models.Model):
    service_report = models.OneToOneField(ServiceRevenueReport, related_name='usage_details', on_delete=models.CASCADE)
    locations = JSONField(default={})
    location_costs = JSONField(default={})
    total_cost = models.DecimalField(max_digits=14, decimal_places=2, default='0.00')
