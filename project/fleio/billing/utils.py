import datetime
import decimal
import importlib
import logging
import math
import uuid

from django.apps import apps
from django.utils import timezone
from django.utils.encoding import smart_text

LOG = logging.getLogger(__name__)

INTER_PRICE_ROUNDING = decimal.ROUND_05UP
INTER_PRICE_PREC = '0.00000001'
PRICE_ROUNDING = decimal.ROUND_HALF_UP
PRICE_PREC = '0.0001'

DECIMAL_INFINITE = decimal.Decimal(math.inf)
DECIMAL_ZERO = decimal.Decimal(0)
SECONDS_PER_HOUR = int(datetime.timedelta(hours=1).total_seconds())

DATETIME_MAX = timezone.make_aware(timezone.datetime.max - datetime.timedelta(days=3000), timezone.utc)


def get_module(module_string, raise_exception=True):
    try:
        return importlib.import_module(module_string)
    except (ImportError, AttributeError) as e:
        LOG.exception(e)
        if raise_exception:
            raise
        else:
            return None


def ceil_datetime(date):
    """
    Ceil datetime by day.
    Ex: 21.04.2017 17:59:23 would become 22.04.2017 00:00:00
    :param date: datetime
    """
    return date.replace(hour=23, minute=59, second=59, microsecond=0) + datetime.timedelta(seconds=1)


def end_of_day(date):
    """Return the last hour second and microsecond for the current day."""
    return date.replace(hour=23, minute=59, second=59, microsecond=99999)


def cdecimal(value, q='.01', rounding=decimal.ROUND_HALF_UP):
    """Convert to Decimal"""
    return decimal.Decimal(value).quantize(decimal.Decimal(q), rounding=rounding)


def convert_currency(price, from_currency, to_currency):
    """Convert currency"""
    if from_currency == to_currency:
        return cdecimal(price, INTER_PRICE_PREC, INTER_PRICE_ROUNDING)
    else:
        price = decimal.Decimal(price)  # Convert to decimal in case we have a string or float
        price = price * from_currency.rate * to_currency.rate
        return cdecimal(price, INTER_PRICE_PREC, INTER_PRICE_ROUNDING)


def generate_uuid():
    return smart_text(uuid.uuid4())


def get_payment_modules():
    for app_conf in apps.get_app_configs():
        if getattr(app_conf, 'fleio_module_type', None) == 'payment_gateway':
            app_label = getattr(app_conf, 'label')
            if app_label.isidentifier():
                yield app_conf
            else:
                LOG.error('Ignoring Django payment gateway app with invalid label {}'.format(app_label))


def get_payment_module_by_label(mod_label):
    for app_conf in apps.get_app_configs():
        if getattr(app_conf, 'fleio_module_type', None) == 'payment_gateway':
            if app_conf.label == mod_label:
                return app_conf


def config_option_cycles_match_product(configurable_option, product):
    """Check that all cycles from product are present in option cycles"""
    product_cycles = product.cycles.available_to_clients().values_list('cycle', 'cycle_multiplier', 'currency')
    product_cycles = ['{}{}{}'.format(c[0], c[1], c[2]) for c in product_cycles]
    product_cycles_set = set(product_cycles)
    if configurable_option.widget in configurable_option.WIDGET_CHOICES.WITHOUT_CHOICES:
        opt_cycles = configurable_option.cycles.values_list('cycle', 'cycle_multiplier', 'currency')
        opt_cycles = ['{}{}{}'.format(c[0], c[1], c[2]) for c in opt_cycles]
        set_intersect = product_cycles_set.intersection(set(opt_cycles))
        if set_intersect == product_cycles_set:
            return True
    else:
        filtered_qs = configurable_option.choices
        opt_cycles = filtered_qs.values_list('label',
                                             'cycles__cycle',
                                             'cycles__cycle_multiplier',
                                             'cycles__currency')
        opt_sort_cycles = {}
        for c in opt_cycles:
            if c[0] in opt_sort_cycles:
                opt_sort_cycles[c[0]].append('{}{}{}'.format(c[1], c[2], c[3]))
            else:
                opt_sort_cycles[c[0]] = ['{}{}{}'.format(c[1], c[2], c[3])]
        for key, value in opt_sort_cycles.items():
            optc_intersect = product_cycles_set.intersection(set(value))
            if product_cycles_set != optc_intersect:
                return False
        else:
            return True
    return False


def get_customer_invoice_details(invoice) -> str:
    """
    Method that gets what info to display on pdf invoices
    :param invoice: the invoice
    :return: Returns a string cotaining information separated by '\n'
    """
    client = invoice.client
    info = [client.long_name, client.vat_id, client.address1, client.address2,
            '{}, {}'.format(client.city, client.get_country_display()), client.phone]
    return '\n'.join([x for x in info if x])
