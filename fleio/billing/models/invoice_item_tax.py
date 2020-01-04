from django.db import models

from .invoice_item import InvoiceItem
from .tax_rule import TaxRule


class InvoiceItemTax(models.Model):
    """Invoice Item Taxes like VAT"""
    item = models.ForeignKey(InvoiceItem, related_name='taxes', on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    tax_rule = models.ForeignKey(TaxRule, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
