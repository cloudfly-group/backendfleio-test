from celery.canvas import Signature
from datetime import datetime
from decimal import Decimal
import logging
from typing import Optional
from typing import Tuple

from fleio.billing.estimated_usage import EstimatedUsage
from fleio.billing.models import Service
from fleio.billing.settings import ServiceSuspendType
from fleio.billing.usage_settings import UsageSettings

LOG = logging.getLogger(__name__)


# TODO: move this in a better location
class ServiceUsage(object):
    def __init__(self, total_cost: Decimal):
        self.total_cost = total_cost

    def __add__(self, other: 'ServiceUsage'):
        return ServiceUsage(self.total_cost + other.total_cost)


# TODO: move this in a better location
class BillingError(Exception):
    pass


# TODO: define return types for all methods
class ModuleBase(object):
    module_name = "Module Base"

    def __init__(self, reseller_usage: bool = False):
        self.reseller_usage = reseller_usage

    def initialize(self, service: Service) -> bool:
        """Initializes a new service object.
        This should be the first function called on a service.

        Keyword arguments:
            service -- the service to initialize
        Returns:
            True if service was initialized successfully
        """
        raise NotImplementedError()

    def can_accept_order(self, service: Service) -> Tuple[bool, str]:
        del self, service  # unused
        """
        Check if we can accept an order for the specified service.
        It is not mandatory to implement this in derived classes.

        :param service: the service to check
        :return: True if order can be accepted
        """
        return True, ''

    def create(self, service: Service) -> bool:
        raise NotImplementedError()

    def suspend(self, service: Service, reason: str = None, suspend_type: ServiceSuspendType = None, ) -> bool:
        raise NotImplementedError()

    def resume(self, service: Service) -> bool:
        raise NotImplementedError()

    def renew(self, service: Service) -> bool:
        raise NotImplementedError()

    def change_product(self, service: Service) -> bool:
        raise NotImplementedError()

    def change_cycle(self, service: Service) -> bool:
        raise NotImplementedError()

    def prepare_delete_task(self, service: Service, user_id: Optional[int] = None) -> Optional[Signature]:
        raise NotImplementedError()

    def get_unsettled_usage(self, service: Service, end_datetime: datetime) -> ServiceUsage:
        raise NotImplementedError()

    def get_unpaid_usage(self, service: Service) -> ServiceUsage:
        raise NotImplementedError()

    def get_estimated_usage(self, service: Service, usage_settings: UsageSettings) -> EstimatedUsage:
        raise NotImplementedError()

    def collect_usage(self, service: Service, usage_settings: UsageSettings) -> bool:
        raise NotImplementedError()

    def reset_usage(self, service: Service) -> bool:
        raise NotImplementedError()

    def settle_usage(self, service: Service, end_datetime: datetime) -> bool:
        raise NotImplementedError()

    def get_usage_summary(self, service: Service):
        raise NotImplementedError()

    def get_billing_summary(self, service: Service):
        raise NotImplementedError()

    def get_service_report(self, service, start_date, end_date):
        return {}

    def get_service_unsettled_periods(self, service: Service):
        return []

    def change_pricing_plan(self, service: Service, new_plan_id):
        raise NotImplementedError()
