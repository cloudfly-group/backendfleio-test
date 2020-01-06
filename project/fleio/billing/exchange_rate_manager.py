from decimal import Decimal
import logging
import requests
import xml.dom.minidom as minidom
from typing import Optional

from rest_framework.exceptions import APIException

from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from fleio.billing.models import ConfigurableOptionCycle
from fleio.billing.models import ProductCycle
from fleio.core.models import Currency


LOG = logging.getLogger(__name__)


# European Central Bank connector
class ECBConnector:
    name = 'ECBConnector'

    def __init__(self):
        self.api_url = 'http://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml'
        self.reference_currency = 'EUR'

    def get_exchange_rates(self):
        exchange_rates = {}
        response = requests.request('GET', self.api_url)
        if response.status_code == 200:
            parsed_xml = minidom.parseString(response.content)
            items = parsed_xml.getElementsByTagName('Cube')

            for item in items:
                if 'currency' in item.attributes:
                    rate = item.attributes['rate'].value
                    exchange_rates[item.attributes['currency'].value] = Decimal(rate)
        else:
            raise APIException(_('Failed to retrieve exchange rates'))

        return exchange_rates


# Romanian National Bank connector
class BNRConnector:
    name = 'BNRConnector'

    def __init__(self):
        self.api_url = 'http://www.bnr.ro/nbrfxrates.xml'
        self.reference_currency = 'RON'

    def get_exchange_rates(self):
        exchange_rates = {}
        response = requests.request('GET', self.api_url)
        if response.status_code == 200:
            parsed_xml = minidom.parseString(response.content)
            items = parsed_xml.getElementsByTagName('Rate')

            for item in items:
                currency = item.attributes['currency'].value
                exchange_rates[currency] = 1 / Decimal(item.firstChild.nodeValue)
        else:
            raise APIException(_('Failed to retrieve exchange rates'))

        return exchange_rates


class ExchangeRateManager:
    connectors = {
        BNRConnector.name: {
            'currency': 'RON',
            'connector': BNRConnector(),
        },
        ECBConnector.name: {
            'currency': 'EUR',
            'connector': ECBConnector(),
        },
    }

    @staticmethod
    def update_exchange_rates():
        default_currency = Currency.objects.filter(is_default=True).first()  # type: Currency

        # get the required connector (in this order: default from settings, related to default currency, any other
        # existent connector
        connector = None
        connector_details = ExchangeRateManager.connectors.get(
            getattr(settings, 'DEFAULT_EXCHANGE_RATE_CONNECTOR'),
            None
        )
        if connector_details:
            connector = connector_details['connector']
        else:
            for intermediary_connector in ExchangeRateManager.connectors:
                connector_details = ExchangeRateManager.connectors.get(intermediary_connector)
                if default_currency.code == connector_details['currency']:
                    connector = connector_details['connector']
        if not connector:
            connector_details = ExchangeRateManager.connectors.get(ECBConnector.name)
            connector = connector_details['connector']

        # calculate exchange rates
        if default_currency.code == connector_details['currency']:
            exchange_rates = connector.get_exchange_rates()
            for currency_code in exchange_rates:
                currency = Currency.objects.filter(code=currency_code).first()
                if currency:
                    currency.rate = exchange_rates[currency.code]
                    currency.save()
        else:
            ExchangeRateManager.calculate_exchange_rates(
                connector_details=connector_details,
                default_currency=default_currency,
            )

    @staticmethod
    def calculate_exchange_rates(connector_details, default_currency: Currency):
        connector = connector_details['connector']
        exchange_rates = connector.get_exchange_rates()
        for currency_code in exchange_rates:
            currency = Currency.objects.filter(code=currency_code).first()
            if currency:
                currency.rate = exchange_rates[currency.code] / exchange_rates[default_currency.code]
                currency.save()
        currency = Currency.objects.filter(code=connector_details['currency']).first()
        if currency:
            currency.rate = 1 / exchange_rates[default_currency.code]
            currency.save()

    @staticmethod
    def find_base_price_cycle_for_product(cycle: ProductCycle) -> Optional[ProductCycle]:
        base_cycle = cycle.product.cycles.exclude(
            is_relative_price=True,
        ).filter(
            currency__is_default=True,
            cycle=cycle.cycle,
            cycle_multiplier=cycle.cycle_multiplier,
        ).first()

        return base_cycle

    @staticmethod
    def find_base_price_cycle_for_configuration_option(
            cycle: ConfigurableOptionCycle
    ) -> Optional[ConfigurableOptionCycle]:
        base_cycle = cycle.option.cycles.filter(
            currency__is_default=True,
            cycle=cycle.cycle
        ).first()

        return base_cycle

    @staticmethod
    def update_relative_prices():
        # process product cycles
        for cycle in ProductCycle.objects.filter(is_relative_price=True).all():  # type: ProductCycle
            # this is an extra check here because we do not handle relative price/default currency relation
            if not cycle.currency.is_default:
                base_cycle = ExchangeRateManager.find_base_price_cycle_for_product(cycle)
                if base_cycle:
                    cycle.fixed_price = base_cycle.fixed_price * cycle.currency.rate
                    cycle.save()
            else:
                LOG.warning('Cycle with relative price and default currency found {}'.format(cycle.id))

        # process option cycles
        for option_cycle in ConfigurableOptionCycle.objects.filter(is_relative_price=True).all():
            # this is an extra check here because we do not handle relative price/default currency relation
            if not option_cycle.currency.is_default:
                base_cycle = ExchangeRateManager.find_base_price_cycle_for_configuration_option(
                    cycle=option_cycle)
                if base_cycle:
                    option_cycle.price = base_cycle.price * option_cycle.currency.rate
                    option_cycle.save()
            else:
                LOG.warning('Option cycle with relative price and default currency found {}'.format(option_cycle.id))
