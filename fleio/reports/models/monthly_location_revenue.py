from django.db import models

from .monthly_revenue_report import MonthlyRevenueReport


class MonthlyLocationRevenue(models.Model):
    report = models.ForeignKey(MonthlyRevenueReport, related_name='total_revenue_per_location',
                               on_delete=models.CASCADE)
    name = models.CharField(max_length=255, db_index=True)
    revenue = models.DecimalField(max_digits=14, decimal_places=2, default='0.00')
