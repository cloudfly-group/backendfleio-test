import logging
import copy
import phonenumbers
import string
from dateutil.relativedelta import relativedelta
from decimal import Decimal
from phonenumbers.phonenumberutil import COUNTRY_CODE_TO_REGION_CODE
from typing import List, Tuple, Union

import requests
from django.conf import settings
from django.utils.timezone import now as utcnow
from django.utils.translation import ugettext_lazy as _

from plugins.domains.models import Domain
from plugins.domains.models.domain import DomainStatus
from plugins.domains.models.registrar_prices import RegistrarPrices
from plugins.domains.registrars_connectors.exceptions import RegistrarConnectorException
from plugins.domains.registrars_connectors.registrar_connector_base import DomainActions, WhoisField
from plugins.domains.registrars_connectors.registrar_connector_base import RegistrarConnectorBase
from plugins.domains.utils.domain import DomainUtils

LOG = logging.getLogger(__name__)


class ResellerclubConnector(RegistrarConnectorBase):
    name = 'Resellerclub'

    LIVE_API_URL = 'https://httpapi.com/api/'
    TEST_API_URL = 'https://test.httpapi.com/api/'
    DOMAINCHECK_URL = 'https://domaincheck.httpapi.com/api/'

    DOMAIN_AVAILABLE_URL = 'domains/available.json'
    REGISTER_DOMAIN_URL = 'domains/register.json'
    RENEW_DOMAIN_URL = 'domains/renew.json'
    DOMAIN_ORDERID_URL = 'domains/orderid.json'
    DETAILS_BY_ORDERID_URL = 'domains/details.json'
    DETAILS_BY_DOMAIN_URL = 'domains/details-by-name.json'
    TRANSFER_DOMAIN_URL = 'domains/transfer.json'
    CANCEL_TRANSFER_URL = 'cancel-transfer.json'
    RELEASE_UK_DOMAIN_URL = 'domains/uk/release.json'
    DELETE_DOMAIN_URL = 'domains/delete.json'
    RESEND_TRANSFER_APPROVAL_URL = 'domains/resend-rfa.json'
    ENABLE_LOCK_URL = 'domains/enable-theft-protection.json'
    DISABLE_LOCK_URL = 'domains/disable-theft-protection.json'
    DOMAIN_LOCKS_URL = 'domains/locks.json'
    MODIFY_NS_URL = 'domains/modify-ns.json'
    MODIFY_AUTH_CODE_URL = 'domains/modify-auth-code.json'
    ADD_CHILD_NS_URL = 'domains/add-cns.json'
    MODIFY_CHILD_NS_URL = 'domains/modify-cns-name.json'
    MODIFY_CHILD_NS_IP_URL = 'domains/modify-cns-ip.json'
    MODIFY_CONTACT = 'domains/modify-contact.json'
    SUSPEND_ORDER_URL = 'orders/suspend.json'
    UNSUSPEND_ORDER_URL = 'orders/unsuspend.json'
    PRIVACY_PROTECTION_URL = 'domains/modify-privacy-protection.json'
    RESEND_RAA_URL = 'domains/raa/resend-verification.json'
    SKIP_RAA_URL = 'domains/raa/skip-verification.json'
    PREMIUM_CHECK_URL = 'domains/premium-check.json'
    CUSTOMER_SIGNUP_URL = 'customers/signup.json'
    CUSTOMER_SEARCH_URL = 'customers/search.json'
    CONTACTS_ADD_URL = 'contacts/add.json'
    COST_PRICE_URL = 'products/reseller-cost-price.json'
    CUSTOMER_PRICE_URL = 'products/customer-price.json'
    PROMO_PRICE_URL = 'resellers/promo-details.json'
    PRODUCTS_MAPPING_URL = 'products/category-keys-mapping.json'
    RESELLERS_DETAILS_URL = 'resellers/details.json'

    @property
    def registrar_settings(self):
        return settings.REGISTRARS.get('resellerclub', {})

    @staticmethod
    def _unsafe_testing_request(request_method, url, params=None, data=None):
        """Resellerclub testing API is using outdated and insecure SSL protocols"""
        sess = requests.Session()
        req = requests.Request(request_method, url, params=params, data=data)
        prepped = sess.prepare_request(req)
        sets = sess.merge_environment_settings(prepped.url, None, None, None, None)
        return sess.send(prepped, **sets)

    def api_request(self, request_method, sub_url, params, raise_on_error=True, domain_check=False):
        test_mode = self.registrar_settings.get('test', False)
        if not domain_check:
            api_url = self.TEST_API_URL if test_mode else self.LIVE_API_URL
        else:
            api_url = self.DOMAINCHECK_URL
        url = api_url + sub_url
        log_params = copy.deepcopy(params)
        try:
            log_params.pop('passwd', None)
        except (KeyError, ValueError):
            pass
        LOG.debug('Resellerclub: POST {} with data {}'.format(url, log_params))
        params['auth-userid'] = self.registrar_settings.get('auth_userid')
        params['api-key'] = self.registrar_settings.get('api_key')
        if not params.get('auth-userid') or not params.get('api-key'):
            raise RegistrarConnectorException('Registrar connector {} not configured'.format(self.__class__.__name__))

        req_method = self._unsafe_testing_request if test_mode else requests.request

        try:
            if request_method.upper() in ['POST', 'PUT', 'PATCH']:
                obj_response = req_method(request_method, url, data=params)
            else:
                obj_response = req_method(request_method, url, params=params)
        except Exception as e:
            LOG.exception(e)
            raise RegistrarConnectorException(e)
        try:
            json_response = obj_response.json()
        except ValueError as e:
            LOG.exception(e)
            raise RegistrarConnectorException(e)
        if raise_on_error:
            self._raise_if_errors(json_response)
        return json_response

    @staticmethod
    def _resellerclub_format_extensions(cost_extensions, customer_extensions, products_mapping, promo_prices):
        """Extract extensions from different dicts (individual and groups e.g donutsgroup1) and formats each extension
        to .extension and maps the cost price as well as max available years for registration/renewal and adds a
        promo price to it if available.

        cost_extensions: dict, a mapping of extensions with their corresponding cost prices
        customer_extensions: dict, a mapping of extensions with their max available years (e.g register .mx.com for
         6 years, .com for 10 years, etc.)
        products_mapping: dict, a mapping of a product (dotbuild, dotvegas, donutsgroup) to individual extensions
         (.build, .vegas, [.donutextension1, .donutextension2, ..] note that each donutsgroup has dozens of extensions
        promo_prices: dict, a mapping of a product (dotbuild, dotvegas, etc.) to a promotional price if active


        :returns dict, all extensions from resellerclub and their associated cost prices as well as their max years
        availability (some can be registered for 10 years, others for 2, others for 5, etc.) and their promo
        prices if any
        """

        formatted_extensions = {}
        active_promotions = {
            value['productkey']: value['resellerprice'] for value in promo_prices.values()
            if value['actiontype'] == 'addnewdomain' and value['isactive'] == 'true'
        }

        matching_extensions_prefixes = ('dot', 'dom', 'donuts', 'centralnic', 'thirdlevel', 'codot', 'indot')
        for key in cost_extensions:
            if key.startswith(matching_extensions_prefixes) and key != 'thirdleveldotname':
                try:
                    item_mapping = next(key_value for key_value in products_mapping['domorder'] if key in key_value)
                except StopIteration:
                    LOG.error('Product mapping not found for key {0}'.format(key))
                else:
                    cost_extensions[key].update(customer_values=customer_extensions[key])
                    if key in active_promotions:
                        cost_extensions[key].update(promo_price=active_promotions[key])
                    for extension in item_mapping[key]:
                        if extension.startswith('xn--'):
                            break
                        formatted_extensions['.{0}'.format(extension)] = cost_extensions[key]

        return formatted_extensions

    def _resellerclub_scrape(self, cost_prices, customer_prices, promo_prices, products_mapping, reseller_details):
        """Extracts quintessential information about: cost, customer and promo prices, details and extension groups

        cost_price: json, containing extensions and their corresponding cost prices for a particular reseller_id
        customer_price: json, containing a mapping between each extension and its max year: registration, renewal
        promo_price: json, containing extensions and their corresponding promotional prices
        products_mapping: json, containing a mapping from product names to individual extensions names
        reseller_details: json, containing details about a reseller like: his currency, his parent currency, etc.

        :return a dict with with the following keys: register, renew, transfer, promo prices, currency, min as well as
         max period (for registration) and registrar, which is resellerclub.
        """

        currency = reseller_details['parentsellingcurrencysymbol']
        formatted_extensions = self._resellerclub_format_extensions(cost_prices, customer_prices, products_mapping,
                                                                    promo_prices)

        for key, value in formatted_extensions.items():
            try:
                if len(value['customer_values']['addnewdomain']) > 1:
                    sorted_prices = sorted(value['customer_values']['addnewdomain'].items(),
                                           key=lambda x: Decimal(x[0]), reverse=True)
                    max_period = sorted_prices[0][0]
                    min_period = sorted_prices[-1][0]
                else:
                    min_period = max_period = next(iter(value['customer_values']['addnewdomain']))

                promo_price = value.get('promo_price')

                register_price = value['addnewdomain'][next(iter(value['addnewdomain']))]
                renew_price = value['renewdomain'][next(iter(value['renewdomain']))]
                transfer_price = value['addtransferdomain'][next(iter(value['addtransferdomain']))]

                formatted_extensions[key] = {
                    'register_price': register_price,
                    'renew_price': renew_price,
                    'transfer_price': transfer_price,
                    'promo_price': promo_price,
                    'min_years': min_period,
                    'max_years': max_period,
                    'currency': currency
                }
            except Exception as e:
                LOG.error('Encountered the following error: {0} with args: {1}. '
                          'Not adding the {2} extension to the final list'.format(type(e), e, key))
                del formatted_extensions[key]

        return formatted_extensions

    def update_prices(self, tld_name=None):
        """Extracts quintessential information about: cost, customer and promo prices, details and extension groups
        cost_price: json, containing extensions and their corresponding cost prices for a particular reseller_id
        customer_price: json, containing a mapping between each extension and its max year: registration, renewal
        promo_price: json, containing extensions and their corresponding promotional prices
        products_mapping: json, containing a mapping from product names to individual extensions names
        reseller_details: json, containing details about a reseller like: his currency, his parent currency, etc.
        :return a dict with with the following keys: register, renew, transfer, promo prices, currency, min as well as
             max period (for registration) and registrar, which is resellerclub.
        """

        products_mapping = self.api_request('GET', self.PRODUCTS_MAPPING_URL, {})
        cost_prices = self.api_request('GET', self.COST_PRICE_URL, {})
        customer_prices = self.api_request('GET', self.CUSTOMER_PRICE_URL, {})
        promo_prices = self.api_request('GET', self.PROMO_PRICE_URL, {})
        reseller_details = self.api_request('GET', self.RESELLERS_DETAILS_URL, {})
        extension_prices = self._resellerclub_scrape(cost_prices=cost_prices,
                                                     customer_prices=customer_prices,
                                                     promo_prices=promo_prices,
                                                     products_mapping=products_mapping,
                                                     reseller_details=reseller_details)

        for extension, prices in extension_prices.items():
            # FIXME(tomo): Support prices per multiple years if available
            update_defaults = dict(min_years=prices['min_years'],
                                   max_years=prices['max_years'],
                                   register_price=prices['register_price'],
                                   transfer_price=prices['transfer_price'],
                                   renew_price=prices['renew_price'],
                                   promo_price=prices['promo_price'])
            RegistrarPrices.objects.update_or_create(defaults=update_defaults,
                                                     tld_name=extension,
                                                     connector=self.get_db_connector(),
                                                     years=1,
                                                     currency=prices['currency'])

    def get_domain_actions(self, domain: Domain) -> List[str]:
        if domain.status == DomainStatus.pending:
            return [DomainActions.register]
        elif domain.status == DomainStatus.active:
            return [DomainActions.renew,
                    DomainActions.get_epp_code,
                    DomainActions.registrar_lock,
                    DomainActions.registrar_unlock,
                    DomainActions.request_delete]
        elif domain.status == DomainStatus.pending_transfer:
            return [DomainActions.transfer]
        elif domain.status == DomainStatus.pending:
            return [DomainActions.register]
        elif domain.status == DomainStatus.cancelled:
            return [DomainActions.register]
        elif domain.status == DomainStatus.deleted:
            return [DomainActions.restore]
        return [action for action in DomainActions.domain_actions_map]

    @staticmethod
    def _get_domain_rtld(domain_name: str):
        return domain_name.rpartition('.')[2]

    def search_customer_id(self, username):
        """ Get Customer ID based on username (e-mail address)."""
        api_params = {'username': username,
                      'no-of-records': 10,
                      'page-no': 1
                      }
        # TODO(tomo): Exclude deleted customers ?
        result = self.api_request('POST', self.CUSTOMER_SEARCH_URL, api_params)
        if '1' in result and 'customer.customerid' in result['1']:
            return result['1']['customer.customerid']
        else:
            return None

    def search_orders_by_domain(self, domain_name, options: Union[str, list] = 'All'):
        """ Get the search results based on the domain name. """
        api_params = {'no-of-records': 10,
                      'page-no': 1,
                      'order-by': 'orderid',
                      'domain-name': domain_name,
                      'options': options
                      }
        result = self.api_request('POST', self.DETAILS_BY_DOMAIN_URL, api_params)
        return result

    def create_contact(self, contact_details, customer_id, tld=None):
        """
        Create a logicboxes contact associated with a customer ID.
        If tld is specified, set the appropriate contact type.
        :type contact_details: dict
        :type customer_id: str or int
        :type tld: str or None
        """
        contact_type = 'Contact'
        if tld in ['ca', 'cn', 'co', 'coop', 'de', 'es', 'eu', 'nl', 'ru', 'uk']:
            contact_type = tld.title() + contact_type
        contact_details['customer-id'] = customer_id
        contact_details['type'] = contact_type

        result = self.api_request('POST', self.CONTACTS_ADD_URL, contact_details)
        try:
            int_value = int(str(result))
        except ValueError:
            # TODO(tomo): Log the exception/
            raise RegistrarConnectorException(_('Cannot create the customer account at the registrar.'))
        return str(int_value)

    def create_customer(self, customer_details):
        """
        Creare a customer account.
        :type customer_details: dict
        :returns str
        """
        result = self.api_request('POST', self.CUSTOMER_SIGNUP_URL, customer_details)
        try:
            int_value = int(str(result))
        except ValueError:
            raise RegistrarConnectorException(_('Cannot create the customer account at the registrar.'))
        return str(int_value)

    @staticmethod
    def contact_from_customer(customer_details):
        contact = dict()
        contact.update(customer_details)
        email = contact['username']
        contact['email'] = email
        extra_fields = ['username', 'passwd', 'other-state', 'lang-pref', 'alt-phone-cc', 'alt-phone', 'mobile-cc',
                        'mobile']
        for field in extra_fields:
            if field in contact:
                del contact[field]
        return contact

    def search_domain(self, domain: Domain) -> str:
        api_params = {'domain-name': DomainUtils.strip_tld(domain.name),
                      'tlds': domain.tld.name.lstrip('.')}
        response = self.api_request('POST', self.DOMAIN_AVAILABLE_URL, api_params, domain_check=True)
        return response

    def get_active_domain_orderid(self, domain_name):
        """
        Get the order ID of a registered domain name.
        This will only work for active domains.
        """
        api_params = {'domain-name': domain_name}
        order_id = self.api_request('POST', self.DOMAIN_ORDERID_URL, api_params)
        return order_id

    def execute_domain_action(self, domain: Domain, action: str, **kwargs):
        connector_action = getattr(self, action, None)
        if connector_action and callable(connector_action):
            try:
                return True, connector_action(domain)
            except RegistrarConnectorException as e:
                return False, str(e)
        else:
            return False, _('Invalid action')

    @staticmethod
    def get_phone_and_phone_cc(client_phone, country_code):
        """Get the phone country code from the short countru code (eg: US)"""
        phone_cc = None
        try:
            parsed_phone = phonenumbers.parse(client_phone)
            phone = phonenumbers.format_number(parsed_phone, phonenumbers.PhoneNumberFormat.E164)
        except Exception as e:
            LOG.debug(e)
            phone = client_phone
            for ph_cc, country_c in COUNTRY_CODE_TO_REGION_CODE.items():
                if country_code in country_c:
                    phone_cc = ph_cc
                    break
        return phone, phone_cc

    @staticmethod
    def generate_customer_password(length=9):
        """Generate a password and make sure it contains all required characters by Resellerclub"""
        limit = 0
        password = DomainUtils.generate_password(length)
        while limit < 20:
            lowecase_found = False
            uppercase_found = False
            number_found = False
            punctuation_found = False
            for char in password:
                if char in string.ascii_lowercase:
                    lowecase_found = True
                elif char in string.ascii_uppercase:
                    uppercase_found = True
                elif char in string.digits:
                    number_found = True
                elif char in string.punctuation:
                    punctuation_found = True
            if lowecase_found and uppercase_found and number_found and punctuation_found:
                return password
            else:
                password = DomainUtils.generate_password(length)
            limit += 1
        raise RegistrarConnectorException('Unable to generate a Customer password')

    def _prepare_register_params(self, domain, years=1):
        contact = domain.contact or domain.service.client  # NOTE(tomo): use either contact if available or client
        customer_password = self.generate_customer_password(12)
        phone, phone_cc = self.get_phone_and_phone_cc(contact.phone, contact.country)
        cust_details = {
            'username': contact.email,
            'passwd': customer_password,
            'email': contact.email,
            'name': contact.name,
            'state': contact.state,
            'zipcode': contact.zip_code,
            'company': contact.company or 'N/A',
            'address-line-1': contact.address1,
            'address-line-2': contact.address2,
            'city': contact.city,
            'country': contact.country,
            'phone-cc': phone_cc,
            'phone': phone,
            'lang-pref': 'en',
        }
        params = {'customer-details': cust_details,
                  'domain-name': domain.name,
                  'registrant-contact': cust_details,
                  'admin-contact': cust_details,
                  'tech-contact': cust_details,
                  'billing-contact': cust_details}
        customer_details = params['customer-details']
        domain_name = params['domain-name']

        reg_contact = params.get('registrant-contact')
        admin_contact = params.get('admin-contact')
        tech_contact = params.get('tech-contact')
        billing_contact = params.get('billing-contact')

        customer_id = self.search_customer_id(customer_details.get('username'))
        if customer_id is None:
            customer_id = self.create_customer(customer_details)

        if reg_contact is None:
            reg_contact = self.contact_from_customer(customer_details)

        tld = self._get_domain_rtld(domain_name)
        reg_contact_id = self.create_contact(reg_contact, customer_id, tld)

        if tld not in ['eu', 'nz', 'ru', 'uk']:
            if admin_contact:
                admin_contact_id = self.create_contact(admin_contact, customer_id, tld)
            else:
                admin_contact_id = reg_contact_id
            if tech_contact:
                tech_contact_id = self.create_contact(tech_contact, customer_id, tld)
            else:
                tech_contact_id = reg_contact_id
            if tld in ['ca', 'nl']:
                billing_contact_id = -1
            elif billing_contact:
                billing_contact_id = self.create_contact(billing_contact, customer_id, tld)
            else:
                billing_contact_id = reg_contact_id
        else:
            admin_contact_id = -1
            tech_contact_id = -1
            billing_contact_id = -1

        nameservers = self.get_domain_nameservers(domain)

        return {'domain-name': domain_name,
                'years': str(years),
                'ns': nameservers,
                'invoice-option': 'NoInvoice',
                'protect-privacy': params.get('protect-privacy', False),
                'customer-id': customer_id,
                'reg-contact-id': reg_contact_id,
                'admin-contact-id': admin_contact_id,
                'tech-contact-id': tech_contact_id,
                'billing-contact-id': billing_contact_id
                }

    def get_domain_nameservers(self, domain: Domain) -> list:
        if self.registrar_settings.get('test'):
            nameservers = ['ns1.onlyfordemo.net', 'ns2.onlyfordemo.net']
        else:
            nameservers = [ns['host_name'] for ns in domain.nameservers.values('host_name')]
        return nameservers

    def register(self, domain: Domain) -> (bool, str):
        """ Register a domain name."""
        api_params = self._prepare_register_params(domain, years=domain.registration_period)
        # TODO: Handle .asia .ca .coop .es .nl .pro .ru .us .au and others

        api_response = self.api_request('POST', self.REGISTER_DOMAIN_URL, api_params)
        # TODO(tomo): status can be Success, InvoicePaid and others. Fail if not Success ?
        message = self.get_actionstatusdesc(api_response)
        domain.status = DomainStatus.active

        # TODO: maybe we should set registration and expiry date based on information from registrar
        domain.registration_date = utcnow().date()
        domain.expiry_date = domain.registration_date + relativedelta(years=domain.registration_period)
        domain.save()
        return message

    def transfer(self, domain: Domain) -> str:
        api_params = self._prepare_register_params(domain, years=1)
        api_params['auth-code'] = DomainUtils.decode_epp_code(domain.epp_code)
        api_response = self.api_request('POST', self.TRANSFER_DOMAIN_URL, api_params)
        message = self.get_actionstatusdesc(api_response)
        domain.status = DomainStatus.active
        domain.save(update_fields=['status'])
        return message

    def update_nameservers(self, domain: Domain) -> str:
        nameserver_list = self.get_domain_nameservers(domain)
        order_id = self.get_active_domain_orderid(domain.name)
        api_params = {'ns': nameserver_list,
                      'order-id': order_id}
        api_response = self.api_request('POST', self.MODIFY_NS_URL, api_params)
        message = self.get_actionstatusdesc(api_response)
        return message

    def restore(self, domain: Domain) -> str:
        raise RegistrarConnectorException(_('Restore domain not implemented'))

    def release_domain(self, domain: Domain) -> str:
        """Delete the order associated with an active domain.
        Release a .uk domain name.
        """
        order_id = self.get_active_domain_orderid(domain.name)
        api_params = {'order-id': order_id}
        if domain.tld == 'uk':
            api_params['new-tag'] = '#VI'  # TODO(tomo): set a proper tag ?
            self.api_request('POST', self.RELEASE_UK_DOMAIN_URL, api_params)
        else:
            self.api_request('POST', self.DELETE_DOMAIN_URL, api_params)
        domain.status = DomainStatus.deleted
        domain.save(update_fields=['status'])
        return _('{} deleted successfully').format(domain.name)

    def renew(self, domain: Domain) -> str:
        domain_name = domain.name
        years = domain.registration_period

        order_details = self.search_orders_by_domain(domain_name, options='OrderDetails')

        api_params = {'order-id': order_details.get('orderid'),
                      'exp-date': order_details.get('endtime'),
                      'years': str(years),
                      'invoice-option': 'NoInvoice'
                      }
        api_response = self.api_request('POST', self.RENEW_DOMAIN_URL, api_params)
        # TODO: maybe we should set expiry date based on information from registrar
        domain.expiry_date = domain.expiry_date + relativedelta(years=domain.registration_period)
        domain.save()
        return self.get_actionstatusdesc(api_response)

    def registrar_lock(self, domain: Domain) -> str:
        """ Enable the registrar lock (theft protection)."""
        order_id = self.get_active_domain_orderid(domain.name)
        api_params = {'order-id': order_id}
        api_response = self.api_request('POST', self.ENABLE_LOCK_URL, api_params)
        domain.registrar_locked = True
        domain.save(update_fields=['registrar_locked'])
        return self.get_actionstatusdesc(api_response)

    def registrar_unlock(self, domain: Domain) -> str:
        """ Disable the registrar lock (theft protection)."""
        order_id = self.get_active_domain_orderid(domain.name)
        api_params = {'order-id': order_id}
        api_response = self.api_request('POST', self.DISABLE_LOCK_URL, api_params)
        domain.registrar_locked = False
        domain.save(update_fields=['registrar_locked'])
        return self.get_actionstatusdesc(api_response)

    def request_delete(self, domain: Domain) -> str:
        return self.release_domain(domain)

    def get_epp_code(self, domain: Domain) -> str:
        """ Get the domain EPP code."""
        api_result = self.search_orders_by_domain(domain.name, options='OrderDetails')
        return api_result.get('domsecret')

    def get_price(self, domain: Domain) -> (bool, Decimal, str):
        """Get the domain price from registry"""
        api_params = {'domain-name': domain.name}
        api_result = self.api_request('POST', self.PREMIUM_CHECK_URL, api_params)
        return api_result

    def get_whois_data(self, domain: Domain) -> List[WhoisField]:
        """
        Retrieves the whois fields for a domain

        :param domain: The domain to retrieve field for
        :return: list of WhoisField instances
        """
        fields_map = {'emailaddr': 'email',
                      'telnocc': 'phone-cc',
                      'address1': 'address-line-1',
                      'address2': 'address-line-2',
                      'telno': 'phone',
                      'zip': 'zipcode'}
        try:
            response = self.search_orders_by_domain(domain_name=domain.name, options='RegistrantContactDetails')
        except RegistrarConnectorException as e:
            LOG.debug(e)
            return []
        whois_fields = []
        for key, value in response.get('registrantcontact', {}).items():
            if key and key not in ('contacttype', 'parentkey', 'contactstatus', 'customerid', 'contactid', 'type'):
                whois_fields.append(WhoisField(name=fields_map.get(key, key),
                                               label=key.capitalize(),
                                               value=value,
                                               required=True))
        return whois_fields

    def set_whois_data(self, domain: Domain, whois_data: List[WhoisField]) -> Tuple[bool, str]:
        """
        Retrieves the whois fields for a domain

        :param domain: The domain to set whois data for
        :param whois_data List of WhoisField instances

        :return: tuple of status and error message
        """
        fields_map = {'emailaddr': 'email',
                      'telnocc': 'phone-cc',
                      'address1': 'address-line-1',
                      'address2': 'address-line-2',
                      'telno': 'phone',
                      'zip': 'zipcode',
                      'company': 'company'}
        try:
            response = self.search_orders_by_domain(domain_name=domain.name, options=['OrderDetails',
                                                                                      'RegistrantContactDetails'])
        except RegistrarConnectorException as e:
            return False, '{}'.format(e)
        registrant_contact = response.get('registrantcontact')
        order_id = response.get('orderid')
        if not order_id:
            return False, _('Unable to find domain order')
        contact_data = {}
        for key, value in registrant_contact.items():
            contact_data[fields_map.get(key, key)] = value
        for wfield in whois_data:
            if wfield.name in contact_data:
                contact_data[wfield.name] = wfield.value
        contact_id = self.create_contact(contact_details=contact_data,
                                         customer_id=registrant_contact['customerid'],
                                         tld=domain.tld.name)
        try:
            params = {'order-id': order_id, 'reg-contact-id': contact_id,
                      'admin-contact-id': contact_id, 'tech-contact-id': contact_id,
                      'billing-contact-id': contact_id}
            self.api_request('POST', self.MODIFY_CONTACT, params)
        except RegistrarConnectorException as e:
            return False, '{}'.format(e)
        return True, _('Whois data modified')

    @staticmethod
    def get_actionstatusdesc(api_response) -> str:
        """ Return 'actionstatusdesc' if present. Raise otherwise."""
        try:
            return api_response['actionstatusdesc']
        except KeyError:
            raise RegistrarConnectorException(_('Invalid response from registrar'))

    @staticmethod
    def _raise_if_errors(json_response):
        # TODO(tomo): Better handling of errors. If msg is None after error status, set default for .get()
        if isinstance(json_response, dict):
            status = json_response.get('status')
            if status is not None:
                if status.lower() == 'success':
                    return
                msg = None
                if status == 'error':
                    msg = json_response.get('error')
                if status == 'ERROR':
                    msg = json_response.get('message')
                if status == 'Failed':
                    msg = json_response.get('actionstatusdesc')
                if msg is not None:
                    raise RegistrarConnectorException(msg)
