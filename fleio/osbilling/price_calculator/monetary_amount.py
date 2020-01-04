from decimal import Decimal

from django.conf import settings

from fleio.billing.utils import cdecimal
from fleio.core.models import Currency


class MonetaryAmount:
    def __init__(self, value: Decimal, currency: Currency):
        self.value = value
        self.currency = currency

    def get_value_in_currency(self, currency: Currency) -> Decimal:
        if currency == self.currency:
            return self.value
        else:
            return self.value * self.currency.rate * currency.rate

    def __add__(self, other):
        return MonetaryAmount(self.value + other.get_value_in_currency(self.currency), self.currency)

    def __sub__(self, other):
        return MonetaryAmount(self.value - other.get_value_in_currency(self.currency), self.currency)

    def __mul__(self, other: Decimal):
        return MonetaryAmount(self.value * other, self.currency)

    def __div__(self, other: Decimal):
        return MonetaryAmount(self.value / other, self.currency)

    def __eq__(self, other):
        return self.value == other.get_value_in_currency(self.currency)

    def __lt__(self, other):
        return self.value < other.get_value_in_currency(self.currency)

    def __lte__(self, other):
        return self == other or self < other

    def __gte__(self, other):
        return self == other or self > other

    def format(self, precision: str = settings.OSBILLING_PRICE_PREC, include_currency: bool = True):
        if include_currency:
            return '{} {}'.format(
                cdecimal(self.value, precision),
                self.currency.code
            )
        else:
            return str(cdecimal(self.value, precision))
