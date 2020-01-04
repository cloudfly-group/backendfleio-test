from os import environ
from os.path import abspath, dirname
import sys
import django

current_path = dirname(abspath(__file__))
fleio_path = dirname(dirname(dirname(current_path)))
sys.path.append(fleio_path)
environ.setdefault("DJANGO_SETTINGS_MODULE", "fleio.settings")
django.setup()

from django.conf import settings  # noqa

from fleio.billing.exchange_rate_manager import ExchangeRateManager  # noqa


def run():
    if settings.AUTO_UPDATE_EXCHANGE_RATES:
        ExchangeRateManager.update_exchange_rates()


if __name__ == '__main__':
    run()
