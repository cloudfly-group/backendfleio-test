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


# This class will be used when get module instance from module factory is called for a non registered module
class NullModule(ModuleBase):
    module_name = "Null module"

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

    def change_product(self, service: Service) -> bool:
        LOG.debug('{} change product called for service {}:{}'.format(self.module_name, service.id, service))
        return False

    def change_cycle(self, service: Service) -> bool:
        LOG.debug('{} change cycle called for service {}:{}'.format(self.module_name, service.id, service))
        return False

    def prepare_delete_task(self, service: Service, user_id: Optional[int] = None) -> Optional[Signature]:
        LOG.debug('{} delete called for service {}:{}'.format(self.module_name, service.id, service))
        return delete_service_resources_placeholder.si()

    def get_unsettled_usage(self, service: Service, end_datetime: datetime) -> ServiceUsage:
        LOG.debug('{} get unsettled usage called for service {}:{}'.format(self.module_name, service.id, service))
        return ServiceUsage(Decimal(0))

    def get_unpaid_usage(self, service) -> ServiceUsage:
        LOG.debug('{} get unpaid usage called for service {}:{}'.format(self.module_name, service.id, service))
        return ServiceUsage(Decimal(0))

    def get_estimated_usage(self, service: Service, usage_settings: UsageSettings) -> EstimatedUsage:
        LOG.debug(
            '{} get dynamic price per second called for service {}:{}'.format(self.module_name, service.id, service)
        )
        return EstimatedUsage()

    def collect_usage(self, service: Service, usage_settings: UsageSettings) -> bool:
        LOG.debug('{} collect usage called for service {}:{}'.format(self.module_name, service.id, service))
        return False

    def reset_usage(self, service: Service) -> bool:
        LOG.debug('{} reset usage called for service {}:{}'.format(self.module_name, service.id, service))
        return False

    def settle_usage(self, service, end_datetime: datetime) -> bool:
        LOG.debug('{} settle usage called for service {}:{}'.format(self.module_name, service.id, service))
        return False

    def get_usage_summary(self, service):
        LOG.debug('{} dynamic usage called for service {}:{}'.format(self.module_name, service.id, service))

    def get_billing_summary(self, service):
        LOG.debug('{} billing summary for service {}:{}'.format(self.module_name, service.id, service))

    def change_pricing_plan(self, service: Service, new_plan_id):
        LOG.debug('{} change pricing plan for service {}:{}'.format(self.module_name, service.id, service))
