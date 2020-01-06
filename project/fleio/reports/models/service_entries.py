from django.db import models
from .service_report import ServiceRevenueReport


class ServiceEntriesReport(models.Model):
    service_report = models.ForeignKey(ServiceRevenueReport, related_name='entries', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=14, decimal_places=2, default='0.00')
    item_type = models.CharField(max_length=64)
    from_credit = models.BooleanField(default=False)
    taxes_amount = models.DecimalField(max_digits=14, decimal_places=2, default='0.00')
    taxes_percent = models.DecimalField(max_digits=5, decimal_places=2, default='0')
    source = models.CharField(max_length=3)
    date = models.DateTimeField()
