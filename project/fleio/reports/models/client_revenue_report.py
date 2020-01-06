from django.db import models
from .monthly_revenue_report import MonthlyRevenueReport


class ClientRevenueReport(models.Model):
    client = models.ForeignKey('core.Client', on_delete=models.DO_NOTHING)
    monthly_revenue_report = models.ForeignKey(MonthlyRevenueReport, related_name='revenue_report',
                                               on_delete=models.CASCADE)
    client_display_name = models.CharField(max_length=255, null=True, blank=True)
    credit_in = models.DecimalField(max_digits=14, decimal_places=2, default='0.00')
    credit_out = models.DecimalField(max_digits=14, decimal_places=2, default='0.00')
    credit_available = models.DecimalField(max_digits=14, decimal_places=2, default='0.00')
    total_debt = models.DecimalField(max_digits=14, decimal_places=2, default='0.00')
    total_alloted_from_credit = models.DecimalField(max_digits=14, decimal_places=2, default='0.00')
    start_date = models.DateField()
    end_date = models.DateField()
