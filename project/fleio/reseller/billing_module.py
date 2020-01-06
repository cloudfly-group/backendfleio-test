import datetime
import logging
from decimal import Decimal
from typing import Optional
from typing import Tuple

import celery
from celery.canvas import Signature

from fleio.billing.estimated_usage import EstimatedUsage
from fleio.billing.models import Service
from fleio.billing.modules.base import ModuleBase
from fleio.billing.modules.base import ServiceUsage
from fleio.billing.modules.factory import module_factory
from fleio.billing.services import tasks as service_tasks
from fleio.billing.settings import ServiceSuspendType
from fleio.billing.usage_settings import UsageSettings
from fleio.conf.models import Configuration
from fleio.core.models import Client
from fleio.core.models import ClientStatus
from fleio.osbilling.models import PricingPlan
from fleio.reseller.models import ResellerResources
from fleio.reseller.tasks import delete_reseller_service_resources
from fleio.reseller.utils import filter_queryset_for_client

LOG = logging.getLogger(__name__)


class ResellerBillingModule(ModuleBase):
    module_name = "Reseller Module"

    def initialize(self, service: Service) -> bool:
        LOG.debug('{} initialize called for service {}:{}'.format(self.module_name, service.id, service))

        return True

    def can_accept_order(self, service: Service) -> Tuple[bool, str]:
        LOG.debug('{} can_accept_order called for service {}:{}'.format(self.module_name, service.id, service))

        return True, ''

    def create(self, service: Service) -> bool:
        LOG.debug('{} create called for service {}:{}'.format(self.module_name, service.id, service))

        reseller_resources = ResellerResources.objects.create(
            service=service,
            plan=PricingPlan.objects.get_default_or_any_or_create(currency=service.client.currency)
        )
        Configuration.objects.create(
            reseller_resources=reseller_resources,
            name='default',
            is_default=True,
        )

        return True

    def suspend(self, service: Service, reason: str = None, suspend_type: ServiceSuspendType = None, ) -> bool:
        LOG.debug('{} suspend called for service {}:{}'.format(self.module_name, service.id, service))

        # suspend all clients associated with this service's reseller
        for reseller_client in filter_queryset_for_client(queryset=Client.objects, client=service.client).all():
            LOG.debug('Suspending client {}'.format(reseller_client))
            suspend_service_tasks = list()
            for service in reseller_client.services.active():
                if suspend_type == ServiceSuspendType.overdue and service.is_suspend_overridden():
                    # do not suspend services with suspend overridden
                    continue
                suspend_service_tasks.append(service_tasks.suspend_service.s(
                    service.id, reason,
                    suspend_type=suspend_type
                ))

            celery.group(suspend_service_tasks).apply_async()

            reseller_client.status = ClientStatus.suspended
            reseller_client.save(update_fields=['status'])
            LOG.debug('Client suspended')

        return True

    def resume(self, service: Service) -> bool:
        LOG.debug('{} resume called for service {}:{}'.format(self.module_name, service.id, service))

        # suspend all clients associated with this service's reseller
        for reseller_client in filter_queryset_for_client(queryset=Client.objects, client=service.client).all():
            LOG.debug('Resuming client {}'.format(reseller_client))
            resume_service_tasks = list()
            for service in reseller_client.services.suspended(suspend_type=service.suspend_type):
                resume_service_tasks.append(service_tasks.resume_service.s(service.id))

            celery.group(resume_service_tasks).apply_async()

            reseller_client.status = ClientStatus.active
            reseller_client.save(update_fields=['status'])
            LOG.debug('Client resumed')

        return True

    def renew(self, service: Service) -> bool:
        LOG.debug('{} renew called for service {}:{}'.format(self.module_name, service.id, service))

        # TODO: implement
        return False

    def change_product(self, service: Service) -> bool:
        LOG.debug('{} change_product called for service {}:{}'.format(self.module_name, service.id, service))

        # TODO: implement
        return False

    def change_cycle(self, service: Service) -> bool:
        LOG.debug('{} change_cycle called for service {}:{}'.format(self.module_name, service.id, service))

        # TODO: implement
        return True

    def prepare_delete_task(self, service: Service, user_id: Optional[int] = None) -> Optional[Signature]:
        LOG.debug('{} prepare_delete_task called for service {}:{}'.format(self.module_name, service.id, service))

        return delete_reseller_service_resources.si(service_id=service.id)

    def get_unsettled_usage(self, service: Service, end_datetime: datetime) -> ServiceUsage:
        LOG.debug('{} get_unsettled_usage called for service {}:{}'.format(self.module_name, service.id, service))

        service_usage = ServiceUsage(total_cost=Decimal('0.00'))
        for reseller_client in filter_queryset_for_client(queryset=Client.objects, client=service.client).all():
            for client_service in reseller_client.services.all():
                service_module = module_factory.get_module_instance(service=client_service, reseller_usage=True)
                service_usage = service_usage + service_module.get_unsettled_usage(
                    service=client_service, end_datetime=end_datetime,
                )

        return service_usage

    def get_unpaid_usage(self, service: Service) -> ServiceUsage:
        LOG.debug('{} get_unpaid_usage called for service {}:{}'.format(self.module_name, service.id, service))

        service_usage = ServiceUsage(total_cost=Decimal('0.00'))
        for reseller_client in filter_queryset_for_client(queryset=Client.objects, client=service.client).all():
            for client_service in reseller_client.services.all():
                service_module = module_factory.get_module_instance(service=client_service, reseller_usage=True)
                service_usage = service_usage + service_module.get_unpaid_usage(
                    service=client_service,
                )

        return service_usage

    def get_estimated_usage(self, service: Service, usage_settings: UsageSettings) -> EstimatedUsage:
        LOG.debug('{} get_estimated_usage called for service {}:{}'.format(self.module_name, service.id, service))

        estimated_usage = EstimatedUsage()
        for reseller_client in filter_queryset_for_client(queryset=Client.objects, client=service.client).all():
            for client_service in reseller_client.services.all():
                service_module = module_factory.get_module_instance(service=client_service, reseller_usage=True)
                estimated_usage = estimated_usage + service_module.get_estimated_usage(
                    service=client_service, usage_settings=usage_settings,
                )

        return estimated_usage

    def collect_usage(self, service: Service, usage_settings: UsageSettings) -> bool:
        LOG.debug('{} collect_usage called for service {}:{}'.format(self.module_name, service.id, service))

        # nothing to do here, usage is calculated automatically
        return True

    def reset_usage(self, service: Service) -> bool:
        LOG.debug('{} reset_usage called for service {}:{}'.format(self.module_name, service.id, service))

        for reseller_client in filter_queryset_for_client(queryset=Client.objects, client=service.client).all():
            for client_service in reseller_client.services.all():
                service_module = module_factory.get_module_instance(service=client_service, reseller_usage=True)
                service_module.reset_usage()

        return True

    def settle_usage(self, service: Service, end_datetime: datetime) -> bool:
        LOG.debug('{} settle_usage called for service {}:{}'.format(self.module_name, service.id, service))

        for reseller_client in filter_queryset_for_client(queryset=Client.objects, client=service.client).all():
            for client_service in reseller_client.services.all():
                service_module = module_factory.get_module_instance(service=client_service, reseller_usage=True)
                service_module.settle_usage(service=client_service, end_datetime=end_datetime)

        return False

    def get_usage_summary(self, service: Service):
        LOG.debug('{} get_usage_summary called for service {}:{}'.format(self.module_name, service.id, service))

        #  TODO: investigate if this is needed, usage summary can be retrieved for each client

    def get_billing_summary(self, service: Service):
        LOG.debug('{} get_billing_summary called for service {}:{}'.format(self.module_name, service.id, service))

        # TODO: investigate if this is needed, billing summary can be retrieved for each client

    def get_service_report(self, service, start_date, end_date):
        LOG.debug('{} get_service_report called for service {}:{}'.format(self.module_name, service.id, service))

        # TODO: implement
        return {'name': 'OpenStack resources report', 'locations': {}, 'service': None, 'location_cost': {}}

    def get_service_unsettled_periods(self, service: Service):
        LOG.debug('{} get_service_unsettled_periods called for service {}:{}'.format(
            self.module_name, service.id, service,
        ))
        # TODO: investigate if this is needed, unsettled periods can be retrieved for each client
        return []

    def change_pricing_plan(self, service: Service, new_plan_id):
        LOG.debug('{} change_pricing_plan called for service {}:{}'.format(self.module_name, service.id, service))
