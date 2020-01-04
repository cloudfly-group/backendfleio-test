from abc import ABC
from abc import abstractmethod
from collections import OrderedDict
from typing import Dict, Optional
from typing import List
from typing import Tuple

from django.utils.translation import ugettext_lazy as _

from plugins.domains.models import Domain
from plugins.domains.models import RegistrarConnector
from plugins.domains.models import TLD


class DomainActions:
    register = 'register'
    transfer = 'transfer'
    renew = 'renew'
    reserve = 'reserve'
    restore = 'restore'
    modify_contact = 'modify_contact'
    get_epp_code = 'get_epp_code'
    registrar_lock = 'registrar_lock'
    registrar_unlock = 'registrar_unlock'
    request_delete = 'request_delete'
    release_domain = 'release_domain'
    update_nameservers = 'update_nameservers'

    domain_actions_map = OrderedDict([
        (register, _('Register')),
        (transfer, _('Transfer')),
        (renew, _('Renew')),
        (reserve, _('Reserve')),
        (restore, _('Restore')),
        (modify_contact, _('Modify Contact Details')),
        (get_epp_code, _('Get EPP Code')),
        (registrar_lock, _('Activate Registrar Lock')),
        (registrar_unlock, _('Deactivate Registrar Lock')),
        (request_delete, _('Request Delete')),
        (release_domain, _('Release Domain')),
        (update_nameservers, _('Update nameservers'))
    ])


class WhoisField:
    def __init__(self, name: str, value: str, required: bool, label: Optional[str]):
        self.name = name
        self.label = label
        self.value = value
        self.required = required

    def __str__(self):
        return '{}({}): {}'.format(self.label, self.name, self.value)


class RegistrarConnectorBase(ABC):
    name = 'RegistrarConnectorBase'

    def get_custom_fields_for_tld(self, tld: TLD) -> Dict[str, Dict]:
        """
        Retrieves needed custom fields for a tld

        :param tld: the tld to get custom fields for
        :return: dictionary containing custom fields
        """
        return {}

    def get_whois_data(self, domain: Domain) -> List[WhoisField]:
        """
        Retrieves the whois fields for a domain

        :param domain: The domain to retrieve field for
        :return: list of WhoisField instances
        """
        return []

    def set_whois_data(self, domain: Domain, whois_data: List[WhoisField]) -> Tuple[bool, str]:
        """
        Retrieves the whois fields for a domain

        :param domain: The domain to set whois data for
        :param whois_data List of WhoisField instances

        :return: tuple of status and error message
        """
        return False, _('Not implemented')

    @abstractmethod
    def get_domain_actions(self, domain: Domain) -> List[str]:
        """
        Retrieves available actions for a domain

        :param domain: the domain to get actions for
        :return: list of available actions
        """

    def execute_domain_action(self, domain: Domain, action: str, **kwargs) -> Tuple[bool, str]:
        """
        Executes a specified action for a domain

        :param domain: the domain to perform actions for
        :param action: the action to perform, must be one of the actions defined in DomainActions
        :param kwargs: extra keyword arguments
        :return:
        """

    def get_db_connector(self):
        return RegistrarConnector.objects.get(name=self.name)

    def update_prices(self, tld_name: str) -> None:
        pass
