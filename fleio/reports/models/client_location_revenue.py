from django.db import models

from .client_revenue_report import ClientRevenueReport


class ClientLocationRevenue(models.Model):
    report = models.ForeignKey(ClientRevenueReport, related_name='revenue_per_location', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, db_index=True)
    revenue = models.DecimalField(max_digits=14, decimal_places=2, default='0.00')
