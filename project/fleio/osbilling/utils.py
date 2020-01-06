import decimal
from iso8601 import iso8601
from django.conf import settings

from fleio.utils.time import parse_isotime

# How many seconds to consider for a month/billing cycle
RESIZABLE_UNITS = ('b', 'k', 'm', 'g', 't', 'p', 'e')
TYPE_NUMBERS = ('integer', 'float', 'number')

TIME_ROUNDING = getattr(settings, 'OSBILLING_TIME_ROUNDING', decimal.ROUND_UP)
INTER_TIME_ROUNDING_PREC = getattr(settings, 'OSBILLING_INTER_TIME_ROUNDING_PREC', '0.000000001')
TIME_ROUNDING_PREC = getattr(settings, 'OSBILLING_TIME_ROUNDING_PREC', '1.')
INTER_PRICE_ROUNDING = getattr(settings, 'OSBILLING_INTER_PRICE_ROUNDING', decimal.ROUND_HALF_UP)
INTER_PRICE_PREC = getattr(settings, 'OSBILLING_INTER_PRICE_PREC', '0.000000001')
INTER_PRICE_DISPLAY_PREC = getattr(settings, 'OSBILLING_INTER_PRICE_DISPLAY_PREC', '0.0001')
PRICE_ROUNDING = getattr(settings, 'OSBILLING_PRICE_ROUNDING', decimal.ROUND_HALF_UP)
PRICE_PREC = getattr(settings, 'OSBILLING_PRICE_PREC', '0.01')
VALUE_PREC = '1.'
VALUE_ROUNDING = decimal.ROUND_UP
SECONDS_MAP = {'s': 1, 'm': 60, 'h': 3600, 'd': 3600 * 24}

DECIMAL_ZERO = decimal.Decimal(0)

MINIMUM_PRICE_PER_RULE = decimal.Decimal('0.01')

TYPE_CONVERTERS = {'integer': int,
                   'int': int,
                   'decimal': decimal.Decimal,
                   'float': float,
                   'number': int,
                   'datetime': parse_isotime}


def parse_dt_wo_microseconds(dt, utc=False):
    """Some events have microseconds, others don't, for the same date/time in Kilo."""
    if utc:
        return parse_isotime(dt).replace(microsecond=0, tzinfo=iso8601.UTC)
    else:
        return parse_isotime(dt).replace(microsecond=0)


def cdecimal(value, q='.01', rounding=decimal.ROUND_HALF_UP):
    """
    Convert to Decimal
    """
    return decimal.Decimal(value).quantize(decimal.Decimal(q), rounding=rounding)


def resize_to(size, f, to, bsize=1024):
    """
    Convert bytes to megabytes a.s.o.
    Needed for price rule attribute value conversion.
    """
    a = {'b': 0, 'k': 1, 'm': 2, 'g': 3, 't': 4, 'p': 5, 'e': 6}
    r = float(size)
    if a[f] <= a[to]:
        for i in range(a[to] - a[f]):
            r /= bsize
    else:
        for i in range(a[f] - a[to]):
            r *= bsize
    return r


def convert_to_type(attr_value, attr_type):
    """Try to convert a value to a python base type or datetime."""
    if attr_type in TYPE_CONVERTERS:
        try:
            return TYPE_CONVERTERS[attr_type](attr_value)
        except (ValueError, TypeError):
            return attr_value
    else:
        return attr_value


def convert_currency(price, from_currency, to_currency):
    if from_currency == to_currency:
        return cdecimal(price, INTER_PRICE_PREC, INTER_PRICE_ROUNDING)
    else:
        price = decimal.Decimal(price)  # Convert to decimal in case we have a string or float
        price = price * from_currency.rate * to_currency.rate
        return cdecimal(price, INTER_PRICE_PREC, INTER_PRICE_ROUNDING)


def time_unit_seconds(time_unit, default=1):
    if time_unit not in SECONDS_MAP:
        raise ValueError('Unsupported time unit')

    return SECONDS_MAP.get(time_unit, default)
