from django.db import models


class MonthlyRevenueReport(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    total_revenue = models.DecimalField(max_digits=14, decimal_places=2, default='0.00')
    currency_code = models.CharField(max_length=8, default='USD')
    generating = models.BooleanField(default=False)

    objects = models.Manager

    class Meta:
        ordering = ('-start_date', )
