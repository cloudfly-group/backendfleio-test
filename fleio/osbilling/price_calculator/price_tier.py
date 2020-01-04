from decimal import Decimal

from fleio.core.models import Currency
from fleio.osbilling.price_calculator.monetary_amount import MonetaryAmount


class PriceTier:
    def __init__(self, applies_from: int, applies_to: int, price: Decimal, currency: Currency):
        self.applies_from = applies_from
        self.applies_to = applies_to
        self.price = MonetaryAmount(price, currency)
