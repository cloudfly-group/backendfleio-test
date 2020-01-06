import logging
from decimal import Decimal
from datetime import datetime
from typing import Optional, Tuple

from celery.canvas import Signature
from django.db import transaction
from django.utils.translation import ugettext_lazy as _

from fleio.billing.estimated_usage import EstimatedUsage
from fleio.billing.models import Service, ServiceHostingAccount
from fleio.billing.modules.base import ModuleBase, ServiceUsage
from fleio.billing.settings import ServiceSuspendType
from fleio.billing.usage_settings import UsageSettings
from fleio.servers.models.server_group import GroupPlacementChoices
from .whmapi import Client
from .utils import get_server_settings
from .utils import get_least_full_server
from .utils import get_available_server_in_order
from .utils import generate_username
from .utils import get_whmclient_from_service
from .tasks import delete_cpanel_account

LOG = logging.getLogger(__name__)


class CpanelBillingModule(ModuleBase):
    module_name = 'Cpanel Module'

    def initialize(self, service: Service) -> bool:
        """Initializes a new service object.
        This should be the first function called on a service.

        Keyword arguments:
            service -- the service to initialize
        Returns:
            True if service was initialized successfully
        """
        LOG.debug('{} initialized called for service {}:{}'.format(self.module_name, service.id, service))
        return True

    def can_accept_order(self, service: Service) -> Tuple[bool, str]:
        try:
            module_settings = service.product.cpanelserver_product_settings
        except Exception as e:
            LOG.exception('Exception when attempting to get cpanel server product settings: {}'.format(e))
        else:
            if module_settings:
                del module_settings  # unused, retrieved only for test
                return True, ''

        return False, _('CPanel server product is not properly configured.')

    def prepare_delete_task(self, service: Service, user_id: Optional[int] = None) -> Optional[Signature]:
        return delete_cpanel_account.si(service_id=service.pk)

    def resume(self, service: Service) -> bool:
        whmapi = get_whmclient_from_service(service=service)
        whmapi.request('unsuspendacct', user=service.hosting_account.username)
        return True

    def suspend(self, service: Service, reason: str = None, suspend_type: ServiceSuspendType = None) -> bool:
        whmapi = get_whmclient_from_service(service=service)
        dissallowun = (suspend_type == ServiceSuspendType.SUSPEND_REASON_STAFF)
        whmapi.request('suspendacct',
                       user=service.hosting_account.username,
                       reason=reason,
                       dissallowun=dissallowun)
        return True

    def create(self, service: Service) -> bool:
        module_settings = service.product.cpanelserver_product_settings
        cpanel_template = module_settings.default_plan
        domain = service.configurable_options.filter(option__name='domain_name').first()  # configurable option
        if domain and domain.option_value:
            domain_name = domain.option_value
            service.display_name = _('{} hosting').format(domain_name)
            service.save(update_fields=['display_name'])
        else:
            LOG.error('Unable to create cPanel account without a domain name.'
                      ' Did you setup the configurable option with internal name domain_name ?')
            return False
        # dedicated IP or not
        dedicated_ip = 'n'
        ip_option = service.configurable_options.filter(option__name='dedicated_ip').first()
        if ip_option and ip_option.option_value and ip_option.option_value == 'yes':
            dedicated_ip = 'y'
        server_group = module_settings.server_group
        if server_group.placement == GroupPlacementChoices.LEAST_FULL:
            cpanel_server = get_least_full_server(server_group=module_settings.server_group)
        else:
            cpanel_server = get_available_server_in_order(server_group=module_settings.server_group)
        if not cpanel_server:
            LOG.error('No available cPanel/WHM servers found')
            return False
        account_username = generate_username(domain_name)
        try:
            server_settings = get_server_settings(cpanel_server)
        except Exception as e:
            LOG.error('Unable to load cPanel server settings: {}'.format(e))
            return False
        whmapi = Client(username=server_settings['username'],
                        hostname=server_settings['hostname'],
                        access_hash=server_settings['key'])
        with transaction.atomic():
            ServiceHostingAccount.objects.create(account_id=domain_name,
                                                 username=account_username,
                                                 package_name=cpanel_template,
                                                 server=cpanel_server,
                                                 service=service)
            whmapi.request('createacct',
                           username=account_username,
                           domain=domain_name,
                           plan=cpanel_template,
                           ip=dedicated_ip)
            # TODO(tomo): Set the dedicated IP on acc from the whmapi responseq
        return True

    def renew(self, service: Service) -> bool:
        pass

    def change_product(self, service: Service) -> bool:
        whmapi = get_whmclient_from_service(service=service)
        whmapi.request(command='changepackage',
                       user=service.hosting_account.username,
                       pkg=service.product.cpanelserver_product_settings.default_plan)
        return True

    def change_cycle(self, service: Service) -> bool:
        return True

    def get_unsettled_usage(self, service: Service, end_datetime: datetime) -> ServiceUsage:
        return ServiceUsage(Decimal(0))

    def get_unpaid_usage(self, service: Service) -> ServiceUsage:
        return ServiceUsage(Decimal(0))

    def get_estimated_usage(self, service: Service, usage_settings: UsageSettings) -> EstimatedUsage:
        return EstimatedUsage()

    def collect_usage(self, service: Service, usage_settings: UsageSettings) -> bool:
        return True

    def reset_usage(self, service: Service) -> bool:
        return True

    def settle_usage(self, service: Service, end_datetime: datetime) -> bool:
        return True

    def get_usage_summary(self, service: Service):
        pass

    def get_billing_summary(self, service: Service):
        pass

    def change_pricing_plan(self, service: Service, new_plan_id):
        pass
