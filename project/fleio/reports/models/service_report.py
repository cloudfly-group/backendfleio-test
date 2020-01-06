from django.db import models

from .client_revenue_report import ClientRevenueReport


class ServiceRevenueReport(models.Model):
    report = models.ForeignKey(ClientRevenueReport, related_name='services_report', on_delete=models.CASCADE)
    service_id = models.CharField(max_length=255)
    service_name = models.CharField(max_length=255)
    service_description = models.CharField(max_length=255, null=True, blank=True)
    price_overridden = models.BooleanField()
    fixed_monthly_price = models.DecimalField(max_digits=14, decimal_places=2, default='0.00')
    total_paid_from_invoices = models.DecimalField(max_digits=14, decimal_places=2, default='0.00')
    total_paid_from_credit = models.DecimalField(max_digits=14, decimal_places=2, default='0.00')
    cost_still_required = models.DecimalField(max_digits=14, decimal_places=2, default='0.00')
    cost_required_percent = models.DecimalField(max_digits=5, decimal_places=2)
    alloted_from_credit = models.DecimalField(max_digits=14, decimal_places=2, default='0.00')
    debt = models.DecimalField(max_digits=14, decimal_places=2, default='0.00')
