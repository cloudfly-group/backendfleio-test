import logging
import requests
from requests.auth import HTTPDigestAuth
import phonenumbers
from phonenumbers import COUNTRY_CODE_TO_REGION_CODE

from dateutil import parser
from typing import List, Tuple, Union

from django.conf import settings
from django.utils.timezone import now as utcnow
from django.utils.translation import ugettext_lazy as _

from fleio.core.models import ClientCustomField

from plugins.domains.registrars_connectors.rotld_validators import RotldValidators
from plugins.domains.registrars_connectors.rotld_validators import CNP
from plugins.domains.models import ContactCustomField, Domain, RegistrarPrices
from plugins.domains.models.domain import DomainStatus
from plugins.domains.registrars_connectors.exceptions import RegistrarConnectorException
from plugins.domains.utils.domain import DomainUtils
from plugins.domains.registrars_connectors.registrar_connector_base import (DomainActions, RegistrarConnectorBase,
                                                                            WhoisField)

LOG = logging.getLogger(__name__)


class RotldDomainAvailability:
    available = 'Available'
    not_available = 'Not Available'
    not_allowed = 'Not Allowed'


class RotldActions:
    CHECK_DOMAIN = 'check-availability'
    REGISTER_DOMAIN = 'domain-register'
    CREATE_CONTACT = 'contact-create'
    GET_DOMAIN_INFO = 'domain-info'
    GET_CONTACT_INFO = 'contact-info'
    REGISTER_NAMESERVER = 'nameserver-create'
    UPDATE_DOMAIN_NAMESERVERS = 'domain-reset-ns'
    UPDATE_CONTACT = 'contact-update'
    RENEW_DOMAIN = 'domain-renew'
    TRANSFER_DOMAIN = 'domain-transfer'


class RotldConnector(RegistrarConnectorBase):
    name = 'Rotld'

    TEST_API_URL = 'https://rest2-test.rotld.ro:6080'
    LIVE_API_URL = 'https://rest2.rotld.ro:6080'
    EPP_API = 'https://epp2-test.rotld.ro:5544'

    @property
    def registrar_settings(self) -> dict:
        return settings.REGISTRARS.get('rotld', {})

    def _get_rotld_username_and_password(self) -> Tuple[str, str]:
        """Gets the RoTLD api authentication credentials and checks if they were provided"""
        username = self.registrar_settings.get('username', None)
        password = self.registrar_settings.get('password', None)
        if not username or not password:
            raise RegistrarConnectorException(_('The RoTLD connector is missing authentication credentials.'))
        return username, password

    def api_request(self, request_method, params, raise_on_error=True):
        api_url = self.TEST_API_URL if self.registrar_settings.get('test', False) else self.LIVE_API_URL

        params['lang'] = self.registrar_settings.get('language', 'en')
        if params['lang'] not in ('en', 'ro'):
            LOG.warning(_('RoTLD language must be either "ro" or "en"'))
            params['lang'] = 'en'
        params['format'] = 'json'
        params['command'] = request_method

        username, password = self._get_rotld_username_and_password()
        response = requests.post(
            url=api_url,
            data=params,
            verify=False,
            auth=HTTPDigestAuth(
                username=username,
                password=password,
            ),
            headers={
                "Accept-Charset": "utf-8;q=0.7,*;q=0.7",
                "Keep-Alive": "30"
            }
        )
        if response.status_code == 401:
            raise RegistrarConnectorException(_('Authentication Failure. Invalid credentials.'))
        if response.status_code == 500:
            raise RegistrarConnectorException(_('Service not available. Server side error.'))
        if response.status_code != 200:
            raise RegistrarConnectorException(_('Service not available.'))
        try:
            json_response = response.json()
        except ValueError as e:
            LOG.exception(e)
            raise RegistrarConnectorException(e)
        if raise_on_error:
            self._raise_if_errors(json_response)
        return json_response

    @staticmethod
    def _raise_if_errors(json_response):
        if isinstance(json_response, dict):
            error = json_response.get('error', 0)
            if error > 0:
                msg = json_response.get('result_message', None)
                if msg is not None:
                    raise RegistrarConnectorException(msg)

    def get_domain_actions(self, domain: Domain) -> List[str]:
        if domain.status == DomainStatus.pending:
            return [DomainActions.register]
        elif domain.status == DomainStatus.active:
            return [
                DomainActions.renew,
                # DomainActions.get_epp_code,
                # DomainActions.registrar_lock,
                # DomainActions.registrar_unlock,
                # DomainActions.request_delete,
            ]
        elif domain.status == DomainStatus.pending_transfer:
            return [DomainActions.transfer]
        elif domain.status == DomainStatus.pending:
            return [DomainActions.register]
        elif domain.status == DomainStatus.cancelled:
            return [DomainActions.register]
        elif domain.status == DomainStatus.deleted:
            return [DomainActions.restore]
        return [action for action in DomainActions.domain_actions_map]

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
    def _get_rotld_phone(national_number, phone_cc) -> str:
        """format the phone number"""
        return '+{}.{}'.format(phone_cc, national_number)

    @staticmethod
    def get_phone_and_phone_cc(client_phone, country_code):
        """
        Parse the contact phone number
        :param client_phone: the phone number added by the client
        :param country_code: eg.: 'RO', 'IT',..
        :return: returns the client national phone number and it's phone country code
        """
        phone_cc = None
        try:
            parsed_phone = phonenumbers.parse(client_phone)
            phone_cc = parsed_phone.country_code
            phone = parsed_phone.national_number
        except Exception as e:
            LOG.debug(e)
            if client_phone[0] != '+':  # number misses country code, determine it then add the national number
                for ph_cc, country_c in COUNTRY_CODE_TO_REGION_CODE.items():
                    if country_code in country_c:
                        phone_cc = ph_cc
                        break
                parsed_phone = phonenumbers.parse('+{}{}'.format(phone_cc, client_phone))
                phone = parsed_phone.national_number
            else:
                raise e
        return phone, phone_cc

    def check_availability(self, domain: Domain) -> Tuple[bool, str]:
        json_response = self.api_request(
            request_method=RotldActions.CHECK_DOMAIN,
            params={
                'domain': domain.name
            }
        )
        result_data = json_response.get('data', {})
        status = result_data.get('status', None)
        if status != RotldDomainAvailability.available:
            return False, result_data.get('result_message', _('Domain not available for registration'))
        return True, _('OK')

    def create_contact(self, domain: Domain):
        """
        Method that creates a registrant
        :param domain: the domain related to the registrant
        :return: returns the registrant id
        """
        cnp = None
        vat_id = None
        person_type = None
        registration_number = None
        reg_no_result = None
        if domain.contact:
            contact = domain.contact
            custom_fields = ContactCustomField.objects.filter(contact=contact)
        else:
            contact = domain.service.client
            custom_fields = ClientCustomField.objects.filter(client=domain.service.client)
        # get custom fields for .ro domain
        for custom_field in custom_fields:
            if custom_field.name == 'rocnp':
                cnp = custom_field.value
            if custom_field.name == 'roregistranttype':
                person_type = custom_field.value
            if custom_field.name == 'roregistrationnumber':
                registration_number = custom_field.value
        # VALIDATIONS
        if not person_type:
            raise RegistrarConnectorException(_('Contact must have the person type specified'))
        if person_type == 'p':  # validate cnp for persons
            if registration_number:
                raise RegistrarConnectorException(_('Romanian private person must not have registration number'))
            cnp_check = CNP(cnp=cnp)
            if not cnp_check.is_valid():
                raise RegistrarConnectorException(_('CNP is not valid'))
            if not cnp_check.check_if_at_least_eighteen_years_old():
                raise RegistrarConnectorException(_('Person must have at least 18 years old'))
        else:  # validate fiscal code for commercial entities and registry of commerce number
            vat_id = contact.vat_id
            if not RotldValidators.is_valid_fiscal_code(code=vat_id):
                raise RegistrarConnectorException(_('Fiscal code (VAT ID) is not valid.'))
            if (person_type == 'c' or person_type == 'ap') and contact.country == 'RO':
                # registry of commerce number validation
                if not registration_number:
                    raise RegistrarConnectorException(
                        _('Company Registry of Commerce number is mandatory for Commercial Romanian entities')
                    )
                is_valid, reg_no_result = RotldValidators.is_valid_com_reg_no(registration_number)
                if not is_valid:
                    raise RegistrarConnectorException(reg_no_result)
        # validate and format phone number
        phone, phone_cc = RotldConnector.get_phone_and_phone_cc(contact.phone, contact.country)
        client_phone = RotldConnector._get_rotld_phone(
            national_number=phone, phone_cc=phone_cc
        )

        params = {
            'name': contact.name,
            'address1': contact.address1,
            'address2': contact.address2,
            # 'address3'(optional): NOTE(manu) we don't have this field yet,
            'city': contact.city,
            'state_province': contact.state,
            'postal_code': contact.zip_code,
            'country_code': contact.country,
            'phone': client_phone,
            # 'fax'(optional): NOTE(manu) we don't have this field yet,
            'email': contact.email,
            'person_type': person_type,
            'cnp_fiscal_code': cnp if person_type == 'p' else vat_id,
        }
        if reg_no_result:
            params['registration_number'] = reg_no_result
        json_response = self.api_request(
            request_method=RotldActions.CREATE_CONTACT,
            params=params
        )
        response_data = json_response.get('data', {})
        return response_data.get('cid', None)

    def register(self, domain: Domain) -> Union[str, dict]:
        """Register a domain name"""
        if domain.status != DomainStatus.pending:
            return _('Cannot register domain that is not pending registration.')
        # check if the domain is available before creating contact and trying to register it
        is_available_for_registration, message = self.check_availability(domain=domain)
        if not is_available_for_registration:
            return message
        # try to create the registrant
        try:
            contact_id = self.create_contact(domain=domain)
        except RegistrarConnectorException as e:
            LOG.debug(e)
            return '{}'.format(e)
        params = {
            'domain': domain.name,
            'reservation': 0,  # NOTE: use 1 for reservation
            'c_registrant': contact_id,
            # 'domain_password': generated by rotld api if not provided,
            'domain_period': domain.registration_period
        }
        try:
            json_response = self.api_request(
                request_method=RotldActions.REGISTER_DOMAIN,
                params=params
            )
        except RegistrarConnectorException as e:
            LOG.debug(e)
            return '{}'.format(e)
        response_data = json_response.get('data', {})

        domain.status = DomainStatus.active
        domain.registration_date = utcnow().date()
        # set the expiration date based on the one received
        expiration_date = response_data.get('expiration_date', None)
        if expiration_date:
            expiration_date = parser.parse(expiration_date)
            domain.expiry_date = expiration_date
            domain.save()
        return response_data

    def get_domain_info(self, domain_name: str) -> dict:
        """Gets information about a domain"""
        json_response = self.api_request(
            request_method=RotldActions.GET_DOMAIN_INFO,
            params={
                'domain': domain_name
            },
        )
        return json_response.get('data', {})

    def get_contact_info(self, registrant_id: str) -> dict:
        """Gets information about a registrant"""
        json_response = self.api_request(
            request_method=RotldActions.GET_CONTACT_INFO,
            params={
                'cid': registrant_id
            }
        )
        return json_response.get('data', {})

    def determine_registrant_id_based_on_domain(self, domain: Domain) -> str:
        """
        Method used to determine the contact/registrant id of a domain
        :param domain: the registrant related domain
        :return: returns the rotld ID of the registrant
        """
        try:
            domain_info = self.get_domain_info(domain_name=domain.name)
        except RegistrarConnectorException as e:
            LOG.debug(e)
            raise RegistrarConnectorException(e)
        registrant_id = domain_info.get('registrant_id', None)
        if not registrant_id:
            raise RegistrarConnectorException(_('Domain information does not contain registrant id'))
        return registrant_id

    def set_whois_data(self, domain: Domain, whois_data: List[WhoisField]) -> Tuple[bool, str]:
        """
        Update whois data of a registrant
        :param domain: the domain that is tied to the registrant
        :param whois_data: the new registrant information
        :return: returns True if the data was successfully updated otherwise False
        """
        try:
            registrant_id = self.determine_registrant_id_based_on_domain(domain=domain)
        except RegistrarConnectorException as e:
            LOG.debug(e)
            return False, '{}'.format(e)
        params = dict()
        for data in whois_data:  # type: WhoisField
            params[data.name] = data.value
        params['cid'] = registrant_id
        try:
            self.api_request(
                request_method=RotldActions.UPDATE_CONTACT,
                params=params
            )
        except RegistrarConnectorException as e:
            LOG.debug(e)
            return False, '{}'.format(e)
        return True, _('WHOIS data updated')

    def get_whois_data(self, domain: Domain) -> List[WhoisField]:
        """
        Retrieves the whois fields for a domain
        :param domain: The domain to retrieve field for
        :return: list of WhoisField instances
        """
        try:
            registrant_id = self.determine_registrant_id_based_on_domain(domain=domain)
        except RegistrarConnectorException as e:
            LOG.debug(e)
            return []
        try:
            registrant_info = self.get_contact_info(registrant_id=registrant_id)
        except RegistrarConnectorException as e:
            LOG.debug(e)
            return []
        field_labels = {
            'address1': _('Address 1'),
            'address2': _('Address 2'),
            'address3': _('Address 3'),
            'city': _('City'),
            'state_province': _('State/province'),
            'postal_code': _('Postal code'),
            'country_code': _('Country code'),
            'phone': _('Phone'),
            'fax': _('Fax'),
            'email': _('Email'),
            'name': _('Name'),
        }
        whois_fields = list()
        for w_field, w_value in sorted(registrant_info.items()):
            required = True
            if w_field in ('address2', 'address3', 'state_province', 'postal_code', 'fax'):
                required = False
            if w_field in ('statuses', 'registration_date', 'last_update_date', 'registrant_id', 'cid', 'person_type'):
                pass
            else:
                whois_fields.append(
                    WhoisField(
                        name=w_field,
                        label=field_labels.get(w_field, w_field),
                        value=w_value,
                        required=required,
                    )
                )
        return whois_fields

    def renew(self, domain: Domain) -> str:
        """Renews a domain, adding the domain registration period years to the expiration date"""
        years = domain.registration_period
        json_response = self.api_request(
            request_method=RotldActions.RENEW_DOMAIN,
            params={
                'domain': domain.name,
                'domain_period': years
            }
        )
        response_data = json_response.get('data', {})
        new_expiry_date = response_data.get('expiration_date', None)
        # set the new expiration date based on the one received
        if new_expiry_date:
            new_expiry_date = parser.parse(new_expiry_date)
            domain.expiry_date = new_expiry_date
            domain.save()
        return _('Success')

    @staticmethod
    def get_user_input_domain_nameservers(domain: Domain) -> str:
        return ','.join(ns['host_name'] for ns in domain.nameservers.values('host_name'))

    def update_nameservers(self, domain: Domain) -> str:
        """Updates ns of a domain"""
        if domain.status == DomainStatus.pending:
            return _('Cannot update nameservers for domain that is pending registration')
        new_nameservers = self.get_user_input_domain_nameservers(domain=domain)
        params = {
            'domain': domain.name,
            'nameservers': new_nameservers
        }
        try:
            self.api_request(
                request_method=RotldActions.UPDATE_DOMAIN_NAMESERVERS,
                params=params
            )
        except RegistrarConnectorException as e:
            LOG.debug(e)
            return '{}'.format(e)
        return _('Nameservers updated')

    def update_prices(self, tld_name: str):
        if tld_name != '.ro':
            raise RegistrarConnectorException(_('RoTLD supports only .ro TLDs'))
        else:
            new_prices = dict()
            extension_prices = getattr(settings, 'ROTLD_PRICES', None)
            for key, value in extension_prices.items():
                if not value:
                    raise RegistrarConnectorException(_('RoTLD prices {} setting was not set').format(key))
                new_prices[key] = value
            RegistrarPrices.objects.update_or_create(
                defaults=new_prices,
                tld_name=tld_name,
                connector=self.get_db_connector(),
                years=1,
                currency='RON'
            )

    def transfer(self, domain: Domain) -> str:
        """Transfer domain to other registrar"""
        params = {
            'domain': domain.name,
            'authorization_key': DomainUtils.decode_epp_code(domain.epp_code)
        }
        try:
            self.api_request(request_method=RotldActions.TRANSFER_DOMAIN, params=params)
        except RegistrarConnectorException as e:
            LOG.debug(e)
            return '{}'.format(e)
        return _('Success')
