from celery.canvas import Signature
from datetime import datetime
from decimal import Decimal
import logging
from typing import Optional

from fleio.billing.estimated_usage import EstimatedUsage
from fleio.billing.models import Service
from fleio.billing.modules.base import ModuleBase
from fleio.billing.modules.base import ServiceUsage
from fleio.billing.settings import ServiceSuspendType
from fleio.billing.usage_settings import UsageSettings

from .utils import delete_service_resources_placeholder

LOG = logging.getLogger(__name__)


class UniversalModule(ModuleBase):
    module_name = "Universal Module"

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

    def create(self, service: Service) -> bool:
        LOG.debug('Universal module create called for service {}:{}'.format(service.id, service))
        return True

    def suspend(self, service: Service, reason: str = None, suspend_type: ServiceSuspendType = None) -> bool:
        LOG.debug('Universal module suspend called for service {}:{}'.format(service.id, service))
        return True

    def resume(self, service: Service) -> bool:
        LOG.debug('Universal module resume called for service {}:{}'.format(service.id, service))
        return True

    def renew(self, service: Service) -> bool:
        LOG.debug('Universal module renew called for service {}:{}'.format(service.id, service))
        return True

    def change_product(self, service: Service) -> bool:
        LOG.debug('Universal module change product called for service {}:{}'.format(service.id, service))
        return True

    def change_cycle(self, service: Service) -> bool:
        LOG.debug('Universal module change cycle called for service {}:{}'.format(service.id, service))
        return True

    def prepare_delete_task(self, service: Service, user_id: Optional[int] = None) -> Optional[Signature]:
        LOG.debug('Universal module delete called for service {}:{}'.format(service.id, service))
        return delete_service_resources_placeholder.si()

    def get_unsettled_usage(self, service: Service, end_datetime: datetime) -> ServiceUsage:
        LOG.debug('Universal module get unsettled usage called for service {}:{}'.format(service.id, service))
        return ServiceUsage(Decimal(0))

    def get_unpaid_usage(self, service) -> ServiceUsage:
        LOG.debug('Universal module get unpaid usage called for service {}:{}'.format(service.id, service))
        return ServiceUsage(Decimal(0))

    def get_estimated_usage(self, service: Service, usage_settings: UsageSettings) -> EstimatedUsage:
        LOG.debug('Universal module get dynamic price per second called for service {}:{}'.format(service.id, service))
        return EstimatedUsage()

    def collect_usage(self, service: Service, usage_settings: UsageSettings) -> bool:
        LOG.debug('Universal module collect usage called for service {}:{}'.format(service.id, service))
        return True

    def reset_usage(self, service: Service) -> bool:
        LOG.debug('Universal module reset usage called for service {}:{}'.format(service.id, service))
        return True

    def settle_usage(self, service, end_datetime: datetime) -> bool:
        LOG.debug('Universal module settle usage called for service {}:{}'.format(service.id, service))
        return True

    def get_usage_summary(self, service):
        LOG.debug('Universal module dynamic usage called for service {}:{}'.format(service.id, service))

    def get_billing_summary(self, service):
        LOG.debug('Universal module billing summary for service {}:{}'.format(service.id, service))

    def change_pricing_plan(self, service: Service, new_plan_id):
        LOG.debug('Universal module change pricing plan for service {}:{}'.format(service.id, service))
