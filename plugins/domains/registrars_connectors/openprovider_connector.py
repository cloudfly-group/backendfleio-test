import logging
import re
import phonenumbers
import requests

from typing import List, Tuple
from datetime import datetime
from decimal import Decimal
from phonenumbers.phonenumberutil import COUNTRY_CODE_TO_REGION_CODE

from lxml import objectify
from lxml import etree

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from fleio.core.models import Client
from plugins.domains.models import Contact, Domain, RegistrarPrices
from plugins.domains.models.domain import DomainStatus
from plugins.domains.registrars_connectors.registrar_connector_base import RegistrarConnectorBase, WhoisField
from plugins.domains.registrars_connectors.registrar_connector_base import DomainActions
from plugins.domains.utils.domain import DomainUtils
from .exceptions import RegistrarConnectorException

LOG = logging.getLogger(__name__)

E = objectify.ElementMaker(annotate=False)

re_addr_match = re.compile(r'(\D*)(\d+)(\D*)')  # NOTE(tomo): split address into address and number


class Response:
    def __init__(self, tree: objectify.ObjectifiedElement):
        self.tree = tree
        self.reply = self.tree.reply
        self.code = self.tree.reply.code
        self.desc = self.tree.reply.desc
        self.data = self.tree.reply.data

        try:
            self.array = self.tree.reply.array[0]
        except AttributeError:
            self.array = []

    @property
    def results_list(self):
        try:
            return self.data.results.array.getchildren()
        except AttributeError:
            return []

    def __str__(self):
        return etree.tostring(self.tree, pretty_print=True).decode('utf8')


class CustomerAddress:
    def __init__(self, street, number, zipcode, city, state, country):
        self.street = street
        self.number = number
        self.zipcode = zipcode
        self.city = city
        self.state = state
        self.country = country

    @classmethod
    def from_client(cls, client):
        client_address, client_address_number = cls.get_address_number(client.address1)
        return cls(street=client_address,
                   number=client_address_number,
                   zipcode=client.zip_code,
                   city=client.city,
                   state=client.state,
                   country=client.country)

    @staticmethod
    def get_address_number(address: str):
        num_match = re.match(re_addr_match, address)
        if num_match:
            addr = num_match[0] + num_match[2]
            number = num_match[1]
            return addr, number
        else:
            return address, 1

    def get_address_xml(self):
        return E.address(
            E.street(self.street),
            E.number(self.number),
            E.zipcode(self.zipcode),
            E.city(self.city),
            E.state(self.state),
            E.country(self.country)
        )


class OpenproviderSettings:
    user_id = settings.REGISTRARS.get('openprovider', {}).get('user_id')
    access_hash = settings.REGISTRARS.get('openprovider', {}).get('access_hash')
    membership_cost = settings.REGISTRARS.get('membership_cost', '0.00')
    try:
        premium_percent = int(settings.REGISTRARS.get('premium_percent', 0))
    except ValueError:
        premium_percent = 0
        LOG.error('Openprovider module only accepts integer permium_percent values')
    test = settings.REGISTRARS.get('openprovider', {}).get('test', False)
    if test:
        api_url = 'https://api.cte.openprovider.eu'
    else:
        api_url = settings.REGISTRARS.get('openprovider', {}).get('api_url', 'https://api.openprovider.eu')


class OpenproviderConnector(RegistrarConnectorBase):
    name = 'Openprovider'

    @staticmethod
    def api_request(data: objectify.ElementMaker) -> Response:
        LOG.debug('Openprovider request: {}'.format(etree.tostring(data)))
        credentials = E.credentials(E.username(OpenproviderSettings.user_id),
                                    E.hash(OpenproviderSettings.access_hash))
        request_xml = E.openXML(credentials, data)
        try:
            response = requests.post(OpenproviderSettings.api_url,
                                     headers={'Content-Type': 'application/xml'},
                                     data=etree.tostring(request_xml))
            response.raise_for_status()
        except (requests.exceptions.RequestException, requests.exceptions.HTTPError) as e:
            LOG.exception(e)
            raise RegistrarConnectorException(_('Unable to communicate with registrar'))
        LOG.debug('Openprovider response: {}'.format(response.content))
        try:
            response = Response(objectify.fromstring(response.content))
        except etree.XMLSyntaxError as e:
            LOG.exception(e)
            raise RegistrarConnectorException('Invalid response from registrar')
        if response.code != 0:   # Check for errors in response
            exception_message = response.desc
            if hasattr(response, 'data'):
                exception_message = '{} {}'.format(exception_message, response.data)
            raise RegistrarConnectorException(exception_message)
        return response

    @staticmethod
    def _xml_domain(domain: Domain):
        """Return an OpenXML formatted domain"""
        return E.domain(E.name(DomainUtils.strip_tld(domain.name)),
                        E.extension(domain.tld.stripped_name))

    def execute_domain_action(self, domain: Domain, action: str, **kwargs):
        domain_action = getattr(self, action, None)
        if domain_action and callable(domain_action):
            try:
                return True, domain_action(domain)
            except RegistrarConnectorException as e:
                return False, str(e)
        else:
            return False, _('Invalid request')

    def search_customer(self, email, last_name, company_name=None):
        search_fields = [E.lastNamePattern(last_name)]
        if company_name:
            search_fields.append(E.companyNamePattern(company_name))
        data = E.searchCustomerRequest(E.offset(0),
                                       E.limit(10),
                                       E.emailPattern(email),
                                       *search_fields,
                                       E.withAdditionalData(0))
        response = self.api_request(data=data)
        customer_list = response.results_list
        return customer_list

    def retrieve_customer(self, handle):
        retrieve_request = E.retrieveCustomerRequest(E.handle('{}'.format(handle)))
        return self.api_request(retrieve_request)

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
        if len(phone) > 3:
            phone_area = phone[:2]
        else:
            phone_area = '0'
        return phone, phone_area, phone_cc

    def create_customer(self, client: Client or Contact):
        client_phone, phone_area, client_phone_cc = self.get_phone_and_phone_cc(client.phone, client.country)
        client_address = CustomerAddress.from_client(client).get_address_xml()
        phone_det = E.phone(E.subscriberNumber(client_phone), E.countryCode(client_phone_cc), E.areaCode(phone_area))
        return self._create_customer(first_name=client.first_name,
                                     last_name=client.last_name,
                                     address=client_address,
                                     company=client.company,
                                     vat=client.vat_id or '',
                                     phone_details=phone_det,
                                     email=client.email)

    def _create_customer(self, first_name, last_name, address, company, vat, phone_details, email,
                         gender='M'):
        new_customer = E.createCustomerRequest(
            E.name(E.firstName(first_name), E.lastName(last_name)),
            E.gender(gender),
            address,
            E.companyName(company),
            E.vat(vat or ''),
            phone_details,
            E.email(email)
        )
        return self.api_request(data=new_customer).data.handle

    def find_or_create_customer(self, client):
        customer_list = self.search_customer(client.email, client.last_name, client.company)
        if not customer_list:
            return self.create_customer(client)
        elif len(customer_list) == 1:
            return customer_list[0].handle
        else:
            raise RegistrarConnectorException(_('Multiple customers with the same e-mail found in OpenProvider'))

    def _parse_pricelist(self, xml_tree: Response):
        """Parses a raw xml from string and converts it to a common format with all other registrars.

        xml_stream: str, represents the raw data from openprovider api; has the structure of an xml tree

        :returns dict, containing TLDs, gTLDs extensions with their corresponding attributes such as:
        (register, renew, transfer, promo prices as well as their max registration/renewal period and currency)
        """
        formatted_extensions = {}
        membership_cost = Decimal(OpenproviderSettings.membership_cost)

        for extension in xml_tree.results_list:
            extension_name = None
            try:
                if extension.status != 'ACT':
                    continue
                else:
                    extension_name = str(extension.name)
                    min_period = int(extension.minPeriod)
                    max_period = int(extension.maxPeriod)
                    try:
                        promo_price = Decimal(str(extension.prices.resellerPrice.reseller.price))
                    except AttributeError:
                        promo_price = None

                    if extension_name.startswith('xn--'):
                        continue

                    try:
                        register_price = renew_price = Decimal(str(extension.prices.renewPrice.reseller.price))
                        transfer_price = Decimal(str(extension.prices.transferPrice.reseller.price))
                        currency = extension.prices.resellerPrice.reseller.currency
                    except AttributeError:
                        continue

                    # register here being renew price and promo being the register (which is sometimes a promo)
                    if promo_price and promo_price == register_price:
                        promo_price = None
                    elif promo_price and promo_price > register_price:
                        register_price = promo_price
                        promo_price = None

                    register_price = str(register_price + membership_cost)
                    renew_price = str(renew_price + membership_cost)
                    if transfer_price:
                        transfer_price = str(transfer_price + membership_cost)
                    else:
                        transfer_price = '0.00'

                    formatted_extensions['.{}'.format(extension_name)] = {
                        'min_period': min_period,
                        'max_period': max_period,
                        'register_price': register_price,
                        'renew_price': renew_price,
                        'transfer_price': transfer_price,
                        'currency': currency,
                        'promo_price': promo_price,
                        'registrar': 'openprovider'
                    }
            except Exception as e:
                LOG.error('Skipping extension: {}, ran into following problems: {}'.format(extension_name, e))
                continue

        return formatted_extensions

    def update_prices(self, tld_name=None):
        # TODO(tomo): Support updates for single tld only
        # Openprivider has a search filter named: onlyNames
        data = E.searchExtensionRequest(E.withPrice('>0'), E.limit(0))
        resp = self.api_request(data)
        extension_prices = self._parse_pricelist(resp)
        for extension, prices in extension_prices.items():
            # FIXME(tomo): Support prices per multiple years if available
            update_defaults = dict(min_years=prices['min_period'],
                                   max_years=prices['max_period'],
                                   register_price=prices['register_price'],
                                   transfer_price=prices['transfer_price'],
                                   renew_price=prices['renew_price'],
                                   promo_price=prices['promo_price'])
            RegistrarPrices.objects.update_or_create(defaults=update_defaults,
                                                     tld_name=extension,
                                                     currency=prices['currency'],
                                                     years=1,
                                                     connector=self.get_db_connector())
        return resp

    @staticmethod
    def _get_domain_nameservers_as_xml(domain: Domain):
        nameserver_list = []
        for ns_host_name in domain.nameservers.values('host_name'):
            nameserver_list.append(E.item(E.name(ns_host_name['host_name'])))
        if not nameserver_list and OpenproviderSettings.test:
            # FIXME(tomo): Set proper testing nameservers
            nameserver_list.append(E.item(E.name('ns1.openprovider.nl'), E.ip('93.180.69.5')))
            nameserver_list.append(E.item(E.name('ns2.openprovider.eu'), E.ip('144.76.197.172')))
        return nameserver_list

    def register(self, domain: Domain):
        contact = domain.contact or domain.service.client
        owner_handle = '{}'.format(self.find_or_create_customer(client=contact))
        nameserver_list = self._get_domain_nameservers_as_xml(domain)
        if not nameserver_list:
            raise RegistrarConnectorException(_('Nameservers for domain are required'))
        dom_req = E.createDomainRequest(
            self._xml_domain(domain),
            E.period(domain.registration_period),
            E.ownerHandle(owner_handle),
            E.adminHandle(owner_handle),
            E.techHandle(owner_handle),
            E.billingHandle(owner_handle),
            E.resellerHandle(''),
            E.nameServers(E.array(*nameserver_list))
        )
        response = self.api_request(data=dom_req)
        if response.data.status == 'ACT':
            domain.status = DomainStatus.active
            domain.registration_date = datetime.strptime(str(response.data.activationDate), '%Y-%m-%d %H:%M:%S').date()
            domain.expiry_date = datetime.strptime(str(response.data.expirationDate), '%Y-%m-%d %H:%M:%S').date()
            domain.epp_code = DomainUtils.encode_epp_code(str(response.data.authCode))
            domain.save(update_fields=['status', 'registration_date', 'expiry_date', 'epp_code'])
            return _('Domain registered')
        elif response.data.status == 'REQ':
            domain.status = DomainStatus.pending
            domain.save(update_fields=['status'])
            return _('Domain pending registration')
        else:
            raise RegistrarConnectorException(_('Domain registration unknown'))

    def transfer(self, domain: Domain):
        if domain.epp_code is None:
            raise RegistrarConnectorException('EPP Code is missing')
        contact = domain.contact or domain.service.client
        owner_handle = self.find_or_create_customer(client=contact)
        nameserver_list = self._get_domain_nameservers_as_xml(domain)
        if not nameserver_list:
            raise RegistrarConnectorException(_('Nameservers for domain are required'))
        dom_req = E.createDomainRequest(
            self._xml_domain(domain),
            E.period(domain.registration_period),
            E.authCode(DomainUtils.decode_epp_code(domain.epp_code)),
            E.ownerHandle(owner_handle),
            E.adminHandle(owner_handle),
            E.techHandle(owner_handle),
            E.billingHandle(owner_handle),
            E.resellerHandle(''),
            E.nameServers(E.array(*nameserver_list))
        )
        response = self.api_request(data=dom_req)
        if response.data.status == 'ACT':
            domain.status = DomainStatus.active
            domain.registration_date = datetime.strptime(str(response.data.activationDate), '%Y-%m-%d %H:%M:%S').date()
            domain.expiry_date = datetime.strptime(str(response.data.expirationDate), '%Y-%m-%d %H:%M:%S').date()
            domain.epp_code = DomainUtils.encode_epp_code(str(response.data.authCode))
            domain.save(update_fields=['status', 'registration_date', 'expiry_date', 'epp_code'])
            return _('Domain transfered')
        elif response.data.status == 'REQ':
            domain.status = DomainStatus.pending
            domain.save(update_fields=['status'])
            return _('Domain pending registration')
        else:
            raise RegistrarConnectorException(_('Domain registration unknown'))

    def update_nameservers(self, domain: Domain) -> str:
        nameserver_list = self._get_domain_nameservers_as_xml(domain)
        if not nameserver_list:
            raise RegistrarConnectorException(_('Nameservers for domain are required'))
        renew_req = E.modifyDomainRequest(
            self._xml_domain(domain),
            E.nameServers(E.array(*nameserver_list))
        )
        self.api_request(data=renew_req)
        return _('Domain nameservers updated')

    def request_delete(self, domain: Domain):
        del_req = E.deleteDomainRequest(self._xml_domain(domain),
                                        E.type('delete'))
        self.api_request(data=del_req)
        domain.status = DomainStatus.deleted
        domain.save(update_fields=['status'])
        return _('Domain successfully deleted')

    def restore(self, domain: Domain):
        restore_req = E.restoreDomainRequest(self._xml_domain(domain))
        self.api_request(data=restore_req)
        domain.status = DomainStatus.active
        domain.save(update_fields=['status'])
        return _('Domain restored successfully')

    def renew(self, domain: Domain):
        renew_req = E.renewDomainRequest(
            self._xml_domain(domain),
            E.period(domain.registration_period)
        )
        self.api_request(data=renew_req)
        return _('Domain renew successfull')

    def registrar_lock(self, domain: Domain):
        lock_req = E.modifyDomainRequest(
            self._xml_domain(domain),
            E.isLocked(1)
        )
        self.api_request(data=lock_req)
        return _('Domain locked successfully')

    def registrar_unlock(self, domain: Domain):
        unlock_req = E.modifyDomainRequest(
            self._xml_domain(domain),
            E.isLocked(0)
        )
        self.api_request(data=unlock_req)
        return _('Domain unlocked successfully')

    def _retrieve_domain_premium_price(self, domain: Domain, operation='register'):
        xml_data = E.retrievePriceDomainRequest(self._xml_domain(domain), E.operation(operation))
        response = self.api_request(data=xml_data)
        reseller_price = response.data.price.reseller.price
        currency_code = response.data.price.reseller.currency
        is_premium = response.data.isPremium
        return is_premium, reseller_price, currency_code

    def _retrieve_domain(self, domain: Domain,
                         with_additional_data=False,
                         with_registry_details=False,
                         with_whois_privacy_data=False):
        retr_dom = E.retrieveDomainRequest(self._xml_domain(domain),
                                           E.withAdditionalData(with_additional_data),
                                           E.withRegistryDetails(with_registry_details),
                                           E.withWhoisPrivacyData(with_whois_privacy_data))
        return self.api_request(data=retr_dom)

    def get_price(self, domain: Domain) -> (bool, Decimal, str):
        """Get the domain price from registry"""
        is_premium, price, currency = self._retrieve_domain_premium_price(domain=domain)
        is_premium = bool(is_premium)
        price = Decimal(price)
        return is_premium, price, currency

    def get_epp_code(self, domain: Domain):
        response = self._retrieve_domain(domain)
        auth_code = str(response.data.authCode)
        domain.epp_code = DomainUtils.encode_epp_code(auth_code)
        domain.save(update_fields=['epp_code'])
        return auth_code

    def _search_domain_by_contact_handle(self, contact_handle):
        search_req = E.searchDomainRequest(E.contactHandle(str(contact_handle)))
        return self.api_request(search_req)

    def get_whois_data(self, domain: Domain) -> List[WhoisField]:
        """
        Retrieves the whois fields for a domain

        :param domain: The domain to retrieve field for
        :return: list of WhoisField instances
        """
        try:
            resp = self._retrieve_domain(domain=domain)
        except RegistrarConnectorException as e:
            LOG.exception(e)
            return []
        owner_handle = resp.data.ownerHandle
        # TODO(tomo): Support admin, tech, billing handles once Fleio supports them
        # admin_handle = resp.data.adminHandle
        # tech_handle = resp.data.techHandle
        # billing_handle = resp.data.billingHandle
        # reseller_handle = resp.data.resellerHandle
        try:
            owner = self.retrieve_customer(owner_handle).data
        except RegistrarConnectorException as e:
            LOG.exception(e)
            return []
        fields_map = {'companyName': _('Company name'),
                      'vat': _('VAT'),
                      'gender': _('Gender'),
                      'email': _('Email address')}
        name_fields_map = {'fullName': _('Full name'),
                           'initials': _('Initials'),
                           'firstName': _('First name'),
                           'prefix': _('Prefix'),
                           'lastName': _('Last name')}
        phone_fields_map = {'countryCode': _('Phone country code'),
                            'areaCode': _('Phone area code'),
                            'subscriberNumber': _('Phone')}
        address_fields_map = {'street': _('Street'),
                              'number': _('Street number'),
                              'zipcode': _('Zip code'),
                              'city': _('City'),
                              'country': _('Country'),
                              'state': _('State')}

        whois_fields = []
        for key, label in fields_map.items():
            whois_fields.append(WhoisField(name=key,
                                           label=label,
                                           value=str(getattr(owner, key, '')),
                                           required=False))
        for key, label in name_fields_map.items():
            required = True
            if key in ('initials', 'prefix', 'vat'):
                required = False
            whois_fields.append(WhoisField(name='flname{}'.format(key),
                                           label=label,
                                           value=str(getattr(owner.name, key, '')),
                                           required=required))
        for key, label in phone_fields_map.items():
            whois_fields.append(WhoisField(name='flphone{}'.format(key),
                                           label=label,
                                           value=str(getattr(owner.phone, key, '')),
                                           required=True))
        for key, label in address_fields_map.items():
            whois_fields.append(WhoisField(name='fladdress{}'.format(key),
                                           label=label,
                                           value=str(getattr(owner.address, key, '')),
                                           required=True))
        return whois_fields

    def set_whois_data(self, domain: Domain, whois_data: List[WhoisField]) -> Tuple[bool, str]:
        """
        Update the contact information for a domain. If the existing contact is used only for this domain
        and the company information is not changed, it will be updated, otherwise a new contact will be created.
        :param domain: The domain to set whois data for
        :param whois_data List of WhoisField instances

        :return: tuple of status and error message
        """
        domain_sld = DomainUtils.strip_tld(domain.name)
        resp = self._retrieve_domain(domain=domain)
        owner_handle = resp.data.ownerHandle
        create_new_contact = False
        whois_fields_data = {'name': {}, 'phone': {}, 'address': {}}
        for wfield in whois_data:
            if wfield.name == 'companyName':
                whois_fields_data['companyName'] = wfield.value
            elif wfield.name == 'gender':
                whois_fields_data['gender'] = wfield.value
            elif wfield.name == 'email':
                whois_fields_data['email'] = wfield.value
            elif wfield.name == 'vat':
                whois_fields_data['vat'] = wfield.value
            elif wfield.name.startswith('flname'):
                name_key = wfield.name.split('flname')[1]
                if name_key:
                    whois_fields_data['name'][name_key] = wfield.value
            elif wfield.name.startswith('fladdress'):
                addr_key = wfield.name.split('fladdress')[1]
                if addr_key:
                    whois_fields_data['address'][addr_key] = wfield.value
            elif wfield.name.startswith('flphone'):
                phone_key = wfield.name.split('flphone')[1]
                if phone_key:
                    whois_fields_data['phone'][phone_key] = wfield.value

        if not create_new_contact:
            existing_customer = self.retrieve_customer(owner_handle)
            if existing_customer.data.companyName != whois_fields_data.get('companyName'):
                create_new_contact = True
                LOG.debug('Creating new customer. Company name differs.')

        if not create_new_contact:
            # See if we actually need to create a new contact
            domains_used_by_handle = self._search_domain_by_contact_handle(owner_handle)
            # Look for company name changes
            for dom_used in domains_used_by_handle.results_list:
                if (dom_used.domain.name != domain_sld or
                        dom_used.domain.extension != domain.tld.stripped_name):
                    create_new_contact = True
                    LOG.debug('Creating new customer. Existing one is in use by multiple domains')
                    break

        address_details = E.address(E.street(whois_fields_data['address'].get('street', '')),
                                    E.number(whois_fields_data['address'].get('number', '')),
                                    E.zipcode(whois_fields_data['address'].get('zipcode', '')),
                                    E.city(whois_fields_data['address'].get('city', '')),
                                    E.country(whois_fields_data['address'].get('country', '')),
                                    E.state(whois_fields_data['address'].get('state', '')))
        phone_details = E.phone(E.countryCode(whois_fields_data['phone'].get('countryCode', '')),
                                E.areaCode(whois_fields_data['phone'].get('areaCode', '')),
                                E.subscriberNumber(whois_fields_data['phone'].get('subscriberNumber', '')))
        if not create_new_contact:
            modify_details = [E.email(whois_fields_data['email'])]
            if whois_fields_data.get('vat'):
                modify_details.append(E.vat(whois_fields_data['vat']))
            xml_req = E.modifyCustomerRequest(E.handle(str(owner_handle)),
                                              address_details,
                                              phone_details,
                                              *modify_details)
        else:
            new_handle = self._create_customer(first_name=whois_fields_data['name']['firstName'],
                                               last_name=whois_fields_data['name']['lastName'],
                                               email=whois_fields_data['email'],
                                               address=address_details,
                                               company=whois_fields_data.get('companyName', ''),
                                               vat=whois_fields_data.get('vat', ''),
                                               phone_details=phone_details)
            xml_req = E.modifyDomainRequest(self._xml_domain(domain),
                                            E.ownerHandle(str(new_handle)),
                                            E.adminHandle(str(new_handle)),
                                            E.techHandle(str(new_handle)),
                                            E.billingHandle(str(new_handle)))
        try:
            self.api_request(data=xml_req)
        except RegistrarConnectorException as e:
            LOG.exception(e)
            return False, str(e)
        return True, _('Whois data updated')

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
