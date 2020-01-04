from django.db import models

from plugins.domains.models import RegistrarConnector


class RegistrarPrices(models.Model):
    currency = models.CharField(max_length=8)
    tld_name = models.CharField(max_length=32, db_index=True)
    connector = models.ForeignKey(RegistrarConnector, related_name='registrar_prices',
                                  null=True, blank=True, on_delete=models.CASCADE)
    years = models.PositiveSmallIntegerField(default=1)
    min_years = models.PositiveSmallIntegerField(default=1)
    max_years = models.PositiveSmallIntegerField(default=10)
    register_price = models.DecimalField(max_digits=10, decimal_places=2)
    renew_price = models.DecimalField(max_digits=10, decimal_places=2)
    transfer_price = models.DecimalField(max_digits=10, decimal_places=2)
    promo_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        verbose_name_plural = 'Registrar prices'
        unique_together = ('tld_name', 'connector', 'currency', 'years')
        ordering = ('updated_at', )

    def __str__(self):
        return '{} {}'.format(self.connector.name, self.tld_name)
