import logging

from dateutil.relativedelta import relativedelta
from typing import List
from typing import Tuple

from django.utils.timezone import now as utcnow
from django.utils.translation import ugettext_lazy as _

from fleio.core.plugins.plugin_dispatcher import plugin_dispatcher
from plugins.domains.models import Domain, TLD
from plugins.domains.models.domain import DomainStatus

from .connector_configuration import ConnectorConfiguration
from .registrar_connector_base import DomainActions, WhoisField
from .registrar_connector_base import RegistrarConnectorBase


LOG = logging.getLogger(__name__)


class TODORegistrarConnector(RegistrarConnectorBase):
    name = 'TODO connector'

    def __init__(self):
        self.configuration = ConnectorConfiguration(name='todo')

    def get_custom_fields_for_tld(self, tld: TLD):
        return self.configuration.custom_fields[tld.name]

    def get_whois_data(self, domain: Domain):
        return [
            WhoisField(name='name', value='Domain Owner', required=True, label=_('Domain owner')),
            WhoisField(name='address', value='3585 Silver Lagoon Landing', required=False, label=_('Street address')),
            WhoisField(name='email', value='email_address@example.com', required=False, label=_('Email address')),
        ]

    def set_whois_data(self, domain: Domain, whois_data: List[WhoisField]) -> Tuple[bool, str]:
        plugin_dispatcher.call_function(
            'todo',
            'create_todo',
            title=_('Whois data updated for domain {}').format(domain.name),
            description=_('Whois data for domain {} was updated to: \n{}.').format(
                domain.name,
                '\n'.join([str(whois_field) for whois_field in whois_data])
            ),
        )

        return True, _('Whois data updated')

    def get_domain_actions(self, domain: Domain) -> List[str]:
        if domain.status == DomainStatus.pending:
            return [DomainActions.register, DomainActions.release_domain]

        if domain.status == DomainStatus.pending_transfer:
            return [DomainActions.transfer, DomainActions.release_domain]

        if domain.status == DomainStatus.unmanaged:
            return [DomainActions.transfer]

        if domain.status == DomainStatus.active:
            return [
                DomainActions.renew,
                DomainActions.get_epp_code,
                DomainActions.modify_contact,
                DomainActions.request_delete,
                DomainActions.registrar_unlock if domain.registrar_locked else DomainActions.registrar_lock,
            ]

        if domain.status == DomainStatus.expired:
            return [DomainActions.register]

        if domain.status == DomainStatus.cancelled:
            return [DomainActions.register]

        if domain.status == DomainStatus.grace:
            return [DomainActions.register]

        if domain.status == DomainStatus.transferred_away:
            return [DomainActions.request_delete]

        LOG.error('Get action called for unsupported domain status {}'.format(domain.status))

    def execute_domain_action(self, domain: Domain, action: str, **kwargs) -> Tuple[bool, str]:
        if action == DomainActions.register:
            domain_registered = self.register_domain(domain=domain)
            message = _('Domain registered successfully') if domain_registered else _('Failed to register domain')
            return domain_registered, message

        if action == DomainActions.transfer:
            domain_transferred = self.transfer_domain(domain=domain)
            message = _('Domain transferred successfully') if domain_transferred else _('Failed to transfer domain')
            return domain_transferred, message

        if action == DomainActions.renew:
            domain_renewed = self.renew_domain(domain=domain)
            message = _('Domain renewed successfully') if domain_renewed else _('Failed to renewed domain')
            return domain_renewed, message

        if action == DomainActions.registrar_lock:
            domain_locked = self.registrar_lock(domain=domain)
            message = _(
                'Registrar lock activated successfully'
            ) if domain_locked else _(
                'Failed to activate registrar lock domain'
            )
            return domain_locked, message

        if action == DomainActions.registrar_unlock:
            domain_unlocked = self.registrar_unlock(domain=domain)
            message = _(
                'Registrar lock deactivated successfully'
            ) if domain_unlocked else _(
                'Failed to deactivate registrar lock domain'
            )
            return domain_unlocked, message

        if action == DomainActions.update_nameservers:
            nameservers_updated = self.update_nameservers(domain=domain)
            message = _(
                'Nameservers updated successfully'
            ) if nameservers_updated else _(
                'Failed to update nameservers for domain'
            )
            return nameservers_updated, message

        if action in [
            DomainActions.get_epp_code,
            DomainActions.modify_contact,
            DomainActions.request_delete,
            DomainActions.release_domain,
        ]:
            return False, _('Action is not implemented yet')

        return False, _('Action is not supported for current domain status')

    @staticmethod
    def register_domain(domain: Domain) -> bool:
        if domain.status != DomainStatus.pending:
            return False

        domain.registration_date = utcnow().date()
        domain.expiry_date = domain.registration_date + relativedelta(years=domain.registration_period)
        domain.status = DomainStatus.active
        domain.save()

        plugin_dispatcher.call_function(
            'todo',
            'create_todo',
            title=_('New domain register {} order').format(domain.name),
            description=_('A new order to register domain {} has been placed.').format(domain.name),
        )

        return True

    @staticmethod
    def transfer_domain(domain: Domain):
        if domain.status != DomainStatus.pending_transfer:
            return False

        domain.status = DomainStatus.active
        domain.save()

        plugin_dispatcher.call_function(
            'todo',
            'create_todo',
            title=_('New domain transfer {} order').format(domain.name),
            description=_('A new order to transfer domain {} has been placed.').format(domain.name),
        )

        return True

    @staticmethod
    def renew_domain(domain: Domain):
        if domain.status != DomainStatus.active:
            return False

        domain.expiry_date = domain.expiry_date + relativedelta(years=domain.registration_period)
        domain.status = DomainStatus.active
        domain.save()

        plugin_dispatcher.call_function(
            'todo',
            'create_todo',
            title=_('New domain renew {} order').format(domain.name),
            description=_('A new order to renew domain {} has been placed.').format(domain.name),
        )

        return True

    @staticmethod
    def registrar_lock(domain: Domain):
        if domain.status != DomainStatus.active and not domain.registrar_locked:
            return False

        domain.registrar_locked = True
        domain.save()

        plugin_dispatcher.call_function(
            'todo',
            'create_todo',
            title=_('Registrar lock activated for domain {}').format(domain.name),
            description=_('Registrar lock has been activated for domain {}.').format(domain.name),
        )

        return True

    @staticmethod
    def registrar_unlock(domain: Domain):
        if domain.status != DomainStatus.active and domain.registrar_locked:
            return False

        domain.registrar_locked = False
        domain.save()

        plugin_dispatcher.call_function(
            'todo',
            'create_todo',
            title=_('Registrar lock deactivated for domain {}').format(domain.name),
            description=_('Registrar lock has been deactivated for domain {}.').format(domain.name),
        )

        return True

    @staticmethod
    def update_nameservers(domain: Domain):
        plugin_dispatcher.call_function(
            'todo',
            'create_todo',
            title=_('Nameservers updated for domain {}').format(domain.name),
            description=_('Nameservers have been updated for domain {}.').format(domain.name),
        )

        return True

    def update_prices(self, tld_name: str):
        pass
