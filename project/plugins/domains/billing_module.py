from celery.canvas import Signature
from datetime import datetime
from decimal import Decimal
import logging
from typing import Optional
from typing import Tuple

from django.db import transaction
from django.utils.translation import ugettext_lazy as _

from fleio.billing.estimated_usage import EstimatedUsage
from fleio.billing.models import Service
from fleio.billing.modules.base import ModuleBase
from fleio.billing.modules.base import ServiceUsage
from fleio.billing.settings import ServiceSuspendType
from fleio.billing.usage_settings import UsageSettings

from plugins.domains.models import Contact, Domain, Nameserver
from plugins.domains.models.domain import DomainStatus
from plugins.domains.settings import BILLING_MODULE_NAME
from plugins.domains.tasks import delete_domain_task
from plugins.domains.utils.domain import DomainUtils

LOG = logging.getLogger(__name__)


class DomainsModule(ModuleBase):
    module_name = BILLING_MODULE_NAME

    def initialize(self, service: Service) -> bool:
        """Initializes a new service object.
        This should be the first function called on a service.

        Keyword arguments:
            service -- the service to initialize
        Returns:
            True if service was initialized successfully
        """
        LOG.debug('{} initialized called for service {}:{}'.format(self.module_name, service.id, service))

        operation = service.plugin_data.get('operation', None)

        with transaction.atomic():
            domain = Domain.objects.create(
                name=service.plugin_data['name'],
                status=DomainStatus.pending if operation == 'register' else DomainStatus.pending_transfer,
                tld=DomainUtils.get_tld(domain_name=service.plugin_data['name']),
                epp_code=DomainUtils.encode_epp_code(service.plugin_data.get('epp')),
                service=service,
                # TODO: this is now used instead of product data because edit item does not currently knows to update
                # TODO: product data
                registration_period=service.cycle.cycle_multiplier,
            )

            for nameserver in [
                service.plugin_data.get('nameserver1', None),
                service.plugin_data.get('nameserver2', None),
                service.plugin_data.get('nameserver3', None),
                service.plugin_data.get('nameserver4', None),
            ]:
                if nameserver:
                    defaults = {'host_name': nameserver}
                    db_nameserver, created = Nameserver.objects.get_or_create(**defaults, defaults=defaults)
                    domain.nameservers.add(db_nameserver)

            contact_id = service.plugin_data.get('contact_id', None)
            domain.contact = Contact.objects.filter(id=contact_id).first()
            domain.save()

        return True

    def can_accept_order(self, service: Service) -> Tuple[bool, str]:
        LOG.debug('{} can accept order called for service {}:{}'.format(self.module_name, service.id, service))
        if service.domain:
            LOG.debug('Found domain {}, checking status'.format(service.domain.name))
            if service.domain.status == DomainStatus.active:
                return True, ''
            else:
                return False, str(_('Domain {} is not active')).format(service.domain.name)
        else:
            LOG.warning('No domain found for service')
            return True, ''

    def change_product(self, service: Service) -> bool:
        LOG.debug('{} change product called for service {}:{}'.format(self.module_name, service.id, service))
        return False

    def create(self, service: Service) -> bool:
        LOG.debug('{} create called for service {}:{}'.format(self.module_name, service.id, service))
        return False

    def suspend(self, service: Service, reason: str = None, suspend_type: ServiceSuspendType = None, ) -> bool:
        LOG.debug('{} suspend called for service {}:{}'.format(self.module_name, service.id, service))
        return False

    def resume(self, service: Service) -> bool:
        LOG.debug('{} resume called for service {}:{}'.format(self.module_name, service.id, service))
        return False

    def renew(self, service: Service) -> bool:
        LOG.debug('{} renew called for service {}:{}'.format(self.module_name, service.id, service))
        return False

    def change_cycle(self, service: Service) -> bool:
        LOG.debug('{} change cycle called for service {}:{}'.format(self.module_name, service.id, service))
        return False

    def prepare_delete_task(self, service: Service, user_id: Optional[int] = None) -> Optional[Signature]:
        LOG.debug('{} delete called for service {}:{}'.format(self.module_name, service.id, service))
        return delete_domain_task.si(service_id=service.id)

    def get_unsettled_usage(self, service: Service, end_datetime: datetime) -> ServiceUsage:
        LOG.debug('{} get unsettled usage called for service {}:{}'.format(self.module_name, service.id, service))
        return ServiceUsage(Decimal(0))

    def get_unpaid_usage(self, service) -> ServiceUsage:
        LOG.debug('{} get unpaid usage called for service {}:{}'.format(self.module_name, service.id, service))
        return ServiceUsage(Decimal(0))

    def get_estimated_usage(self, service: Service, usage_settings: UsageSettings) -> EstimatedUsage:
        LOG.debug('{} get dynamic price per second called for service {}:{}'.format(
            self.module_name,
            service.id,
            service,
        ))
        return EstimatedUsage()

    def collect_usage(self, service: Service, usage_settings: UsageSettings) -> bool:
        LOG.debug('{} collect usage called for service {}:{}'.format(self.module_name, service.id, service))
        return True

    def reset_usage(self, service: Service) -> bool:
        LOG.debug('{} reset usage called for service {}:{}'.format(self.module_name, service.id, service))
        return True

    def settle_usage(self, service, end_datetime: datetime) -> bool:
        LOG.debug('{} settle usage called for service {}:{}'.format(self.module_name, service.id, service))
        return True

    def get_usage_summary(self, service):
        LOG.debug('{} dynamic usage called for service {}:{}'.format(self.module_name, service.id, service))

    def get_billing_summary(self, service):
        LOG.debug('{} billing summary for service {}:{}'.format(self.module_name, service.id, service))

    def change_pricing_plan(self, service: Service, new_plan_id):
        LOG.debug('{} change pricing plan for service {}:{}'.format(self.module_name, service.id, service))
