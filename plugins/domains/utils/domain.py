import logging
import re
import random
import string
import socket
from types import SimpleNamespace
from typing import Optional
from typing import Tuple

from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from fleio.core.models import get_default_currency
from fleio.core.models import Currency
from fleio.billing.utils import cdecimal
from fleio.billing.utils import convert_currency
from fleio.conf.utils import fernet_decrypt, fernet_encrypt

from plugins.domains.configuration import DomainsSettings
from plugins.domains.models import Domain
from plugins.domains.models import Registrar
from plugins.domains.models import RegistrarPrices
from plugins.domains.models import TLD
from plugins.domains.utils.whois_config import whois_config
from plugins.domains.whois import Whois

LOG = logging.getLogger(__name__)

DOMAIN_NAME_REGEX = r'(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9\-])+'


class DomainUtils:
    @staticmethod
    def validate_domain_name(domain_name: str) -> bool:
        """Validates a domain name.

        Keyword arguments:
            domain_name - the domain name to be validated
        Returns:
            True if domain_name is valid, False otherwise
        """
        if not domain_name:
            return False

        if '.' not in domain_name or '..' in domain_name:
            return False

        domain_name_match = re.fullmatch(DOMAIN_NAME_REGEX, domain_name)
        return domain_name_match is not None

    @staticmethod
    def validate_tld_name(tld_name: str) -> bool:
        """Validates a TLD name.

        Keyword arguments:
            tld_name - the TLD name to be validated
        Returns:
            True if tld_name is valid, False otherwise
        """
        if not tld_name:
            return False

        if not tld_name.startswith('.'):
            return False

        if '..' in tld_name:
            return False

        return True

    @staticmethod
    def strip_tld(domain_name: str) -> str:
        """Strips the TLD from a domain name.
        E.g test.com will return 'test' and test.co.uk will also return 'test'

        Keyword arguments:
            domain_name -- a valid domain name - should contain at least a dot
        Returns:
            domain name without tld
        Raises:
            ValueError in case of invalid domain_name
        """
        if not DomainUtils.validate_domain_name(domain_name=domain_name):
            raise ValueError('Invalid domain name {}'.format(domain_name))
        parts = domain_name.split('.')

        return parts[0]

    @staticmethod
    def get_tld_name(domain_name: str) -> str:
        """Gets the domain TLD name.
        E.g test.com will return '.com' and test.co.uk will return .co.uk

        Keyword arguments:
            domain_name -- a valid domain name - should contain at least a dot
        Returns:
            TLD name
        Raises:
            ValueError in case of invalid domain_name
        """
        if not DomainUtils.validate_domain_name(domain_name=domain_name):
            raise ValueError('Invalid domain name {}'.format(domain_name))
        return domain_name.replace(DomainUtils.strip_tld(domain_name), '').lower()

    @staticmethod
    def get_tld(domain_name: str) -> TLD:
        """Gets the TLD model instance for a specific domain name.

        Keywords arguments:
            domain_name -- a valid domain name - should containt at least a dot
        Returns:
            TLD model instance or None if no TLD model instance for domain was found
        """
        if not DomainUtils.validate_domain_name(domain_name=domain_name):
            raise ValueError('Invalid domain name {}'.format(domain_name))
        tld_name = DomainUtils.get_tld_name(domain_name=domain_name)
        return TLD.objects.filter(name__iexact=tld_name).first()

    @staticmethod
    def check_if_domains_is_available_for_registration(
            domain_name: str,
            domains_settings: Optional[DomainsSettings] = None,
            skip_whois_check: bool = False,
    ) -> Tuple[bool, str, str]:
        domain_available = False
        error_message = 'Invalid domain name'
        adjusted_domain_name = domain_name
        default_tld = domains_settings.default_tld if domains_settings.default_tld else None

        if not domain_name:
            return domain_available, error_message, adjusted_domain_name

        parts = domain_name.split('.')
        if len(parts) == 1:
            if not default_tld:
                error_message = _('No TLD specified and default TLD is not set.')
                return domain_available, error_message, adjusted_domain_name
            else:
                adjusted_domain_name += default_tld

        if len(adjusted_domain_name) < 3:
            return domain_available, error_message, adjusted_domain_name

        if not DomainUtils.validate_domain_name(domain_name=adjusted_domain_name):
            return domain_available, error_message, adjusted_domain_name

        tld_name = DomainUtils.get_tld_name(adjusted_domain_name)
        if tld_name not in whois_config.tld_whois_configurations:
            error_message = _('No whois server defined for TLD.')
            return domain_available, error_message, adjusted_domain_name

        if skip_whois_check:
            return True, _('Domain available'), adjusted_domain_name

        tld_config = whois_config.tld_whois_configurations[tld_name]
        domain_available = Whois.domain_available(
            domain_name=adjusted_domain_name,
            whois_server=tld_config.whois_server,
            available_search_str=tld_config.available_search_string
        )

        if not domain_available:
            error_message = _('Domain not available for registration')

        return domain_available, error_message, adjusted_domain_name

    @staticmethod
    def check_if_domains_is_available_for_transfer(
            domain_name: str,
            domains_settings: Optional[DomainsSettings] = None,
            skip_whois_check: bool = False,
    ) -> Tuple[bool, str, str]:
        domain_available = False
        error_message = 'Invalid domain name'
        adjusted_domain_name = domain_name
        default_tld = domains_settings.default_tld if domains_settings.default_tld else None

        if not domain_name:
            return domain_available, error_message, adjusted_domain_name

        parts = domain_name.split('.')
        if len(parts) == 1:
            if not default_tld:
                error_message = _('No TLD specified and default TLD is not set.')
                return domain_available, error_message, adjusted_domain_name
            else:
                adjusted_domain_name += default_tld

        if len(adjusted_domain_name) < 3:
            return domain_available, error_message, adjusted_domain_name

        if not DomainUtils.validate_domain_name(domain_name=adjusted_domain_name):
            return domain_available, error_message, adjusted_domain_name

        tld_name = DomainUtils.get_tld_name(adjusted_domain_name)
        if tld_name not in whois_config.tld_whois_configurations:
            error_message = _('No whois server defined for TLD.')
            return domain_available, error_message, adjusted_domain_name

        if skip_whois_check:
            return True, _('Domain available'), adjusted_domain_name

        tld_config = whois_config.tld_whois_configurations[tld_name]
        domain_available = not Whois.domain_available(
            domain_name=adjusted_domain_name,
            whois_server=tld_config.whois_server,
            available_search_str=tld_config.available_search_string
        )

        if not domain_available:
            error_message = _('Cannot transfer a unregistered domain.')

        return domain_available, error_message, adjusted_domain_name

    @staticmethod
    def get_domain_registrar_prices(domain: Domain, registrar: Registrar, years=None) -> SimpleNamespace or None:
        """Get the registrar prices for a domain"""
        # TODO(tomo): Check if domain is premium
        if years is None:
            years = domain.registration_period
        tld_name = domain.tld.name
        default_currency = get_default_currency()
        register_price = None
        transfer_price = None
        renew_price = None

        response = RegistrarPrices.objects.filter(
            tld_name=tld_name,
            connector=registrar.connector
        )
        if years > 1:
            # If we need a higher number of years, check if we have the answer cached
            # otherwise we need to calculate it
            response = response.filter(Q(years=1) | Q(years=years))
        # Prices can be in multiple currencies and with different years. At least for 1 year we should have the price
        price_currency_match = None
        for db_price in response:
            if db_price.currency == default_currency.code:
                if db_price.years == years:
                    price_currency_match = db_price
                elif db_price.years == 1 and not price_currency_match:
                    price_currency_match = db_price
        price_years_match = None
        if not price_currency_match:
            for db_price in response:
                if db_price.years == years:
                    price_years_match = db_price
                elif db_price.years == 1 and not price_years_match:
                    price_years_match = db_price
        if price_currency_match:
            if price_currency_match.years != years:
                register_price = cdecimal(price_currency_match.register_price * years)
                renew_price = cdecimal(price_currency_match.renew_price * years)
                transfer_price = cdecimal(price_currency_match.transfer_price)  # Transfers are on 1 year only
            else:
                register_price = cdecimal(price_currency_match.register_price)
                renew_price = cdecimal(price_currency_match.renew_price)
                transfer_price = cdecimal(price_currency_match.transfer_price)
        elif price_years_match:
            if price_years_match.years != years:
                pre_register_price = cdecimal(price_years_match.register_price * years)
                pre_renew_price = cdecimal(price_years_match.renew_price * years)
                pre_transfer_price = cdecimal(price_years_match.transfer_price)  # Transfers are on 1 year only
            else:
                pre_register_price = cdecimal(price_years_match.register_price)
                pre_renew_price = cdecimal(price_years_match.register_price)
                pre_transfer_price = cdecimal(price_years_match.register_price)
            try:
                tld_currency = Currency.objects.get(code=price_years_match.currency)
            except Currency.DoesNotExist:
                LOG.error('Registry currency {} does not exist in Fleio'.format(price_years_match.currency))
                return None
            register_price = convert_currency(price=pre_register_price, from_currency=tld_currency,
                                              to_currency=default_currency)
            renew_price = convert_currency(price=pre_renew_price, from_currency=tld_currency,
                                           to_currency=default_currency)
            transfer_price = convert_currency(price=pre_transfer_price, from_currency=tld_currency,
                                              to_currency=default_currency)

        if register_price or renew_price or transfer_price:
            tld_prices = SimpleNamespace()
            tld_prices.register_price = cdecimal(register_price)
            tld_prices.renew_price = cdecimal(renew_price)
            tld_prices.transfer_price = cdecimal(transfer_price)
            tld_prices.currency = default_currency.code
            return tld_prices
        else:
            return None

    @staticmethod
    def encode_epp_code(epp_code):
        if epp_code is None:
            return None
        return fernet_encrypt(epp_code)

    @staticmethod
    def decode_epp_code(epp_code):
        if epp_code is None:
            return None
        return fernet_decrypt(epp_code)

    @staticmethod
    def generate_password(length=9):
        """Generate a password, used for domains registration"""
        return ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits + string.punctuation)
                       for _ in range(length))

    @staticmethod
    def resolve_nameserver(host_name):
        try:
            address_list = socket.getaddrinfo(host_name, None)
            ipv4_list = []
            ipv6_list = []
            for address_info in address_list:
                if address_info[0] == socket.AF_INET:
                    ipv4_list.append(address_info[4][0])
                elif address_info[0] == socket.AF_INET6:
                    ipv6_list.append(address_info[4][0])
            return ipv4_list, ipv6_list
        except socket.gaierror:
            return None, None
