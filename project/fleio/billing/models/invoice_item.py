import decimal

from django.db import models

from .invoice import Invoice
from .service import Service
from .service import Product
from .service import ProductCycle

from fleio.billing.settings import BillingItemTypes


class InvoiceItem(models.Model):
    """All prices include taxes."""

    MAX_UNIT_PRICE = decimal.Decimal('9999999999.99')
    MAX_QUANTITY = decimal.Decimal('9999999999.99')
    MAX_SUBTOTAL = Invoice.MAX_TOTAL

    invoice = models.ForeignKey(Invoice, related_name='items', unique=False, on_delete=models.CASCADE)
    item_type = models.CharField(max_length=16, db_index=True, choices=BillingItemTypes.CHOICES)
    service = models.ForeignKey(Service, null=True, blank=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL)
    cycle = models.ForeignKey(ProductCycle, null=True, blank=True, on_delete=models.SET_NULL)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    taxed = models.BooleanField(default=False)
    description = models.TextField(max_length=1024)

    def __str__(self):
        return self.description
