from decimal import Decimal
from fleio.billing.utils import cdecimal


ZERO_DECIMAL_CURRENCIES = [
    "bif", "clp", "djf", "gnf", "jpy", "kmf", "krw",
    "mga", "pyg", "rwf", "vnd", "vuv", "xaf", "xof", "xpf",
]


MIN_AMOUNT_CURRENCY = {'usd': Decimal('0.50'),
                       'aud': Decimal('0.50'),
                       'brl': Decimal('0.50'),
                       'cad': Decimal('0.50'),
                       'chf': Decimal('0.50'),
                       'dkk': Decimal('2.50'),
                       'eur': Decimal('0.50'),
                       'gbp': Decimal('0.30'),
                       'hkd': Decimal('4.00'),
                       'jpy': Decimal('50'),
                       'mxn': Decimal('10'),
                       'nok': Decimal('3.00'),
                       'nzd': Decimal('0.50'),
                       'sek': Decimal('3.00'),
                       'sgd': Decimal('0.50')}


def convert_amount_from_api(amount, currency=None):
    assert currency is not None, 'Currency cannot be None'
    if currency.lower() in ZERO_DECIMAL_CURRENCIES:
        return cdecimal(amount)
    else:
        return cdecimal(amount / Decimal("100"))


def convert_amount_to_api(amount, currency=None):
    assert currency is not None, 'Currency cannot be None'
    return int(amount * 100) if currency.lower() not in ZERO_DECIMAL_CURRENCIES else int(amount)
