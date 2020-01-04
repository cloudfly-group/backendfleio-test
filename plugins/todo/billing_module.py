from celery.canvas import Signature
from datetime import datetime
from decimal import Decimal
import logging
from typing import Optional

from django.utils.translation import ugettext_lazy as _

from fleio.billing.estimated_usage import EstimatedUsage
from fleio.billing.models import Service
from fleio.billing.modules.base import ModuleBase
from fleio.billing.modules.base import ServiceUsage
from fleio.billing.settings import ServiceSuspendType
from fleio.billing.usage_settings import UsageSettings

from plugins.todo import models
from plugins.todo.tasks import add_todo_for_delete_service

LOG = logging.getLogger(__name__)


class TodoModule(ModuleBase):
    module_name = "TODO Module"

    def initialize(self, service: Service) -> bool:
        """Initializes a new service object.
        This should be the first function called on a service.

        Keyword arguments:
            service -- the service to initialize
        Returns:
            True if service was initialized successfully
        """
        LOG.debug('TODO module initialized called for service {}:{}'.format(service.id, service))
        return True

    def create(self, service: Service) -> bool:
        LOG.debug('TODO module create called for service {}:{}'.format(service.id, service))

        if hasattr(service.product, 'todo_settings'):
            todo_settings = service.product.todo_settings  # type: models.TODOProductSettings
        else:
            todo_settings = None

        if todo_settings and todo_settings.add_todo_on_create:
            models.TODO.objects.add_todo(
                title=_('Service created'),
                description=_('Service {} was created').format(service),
                assigned_to=todo_settings.todo_user
            )
        return True

    def suspend(self, service: Service, reason: str = None, suspend_type: ServiceSuspendType = None, ) -> bool:
        LOG.debug('TODO module suspend called for service {}:{}'.format(service.id, service))
        if hasattr(service.product, 'todo_settings'):
            todo_settings = service.product.todo_settings  # type: models.TODOProductSettings
        else:
            todo_settings = None

        if todo_settings and todo_settings.add_todo_on_suspend:
            models.TODO.objects.add_todo(
                title=_('Service suspended'),
                description=_('Service {} was suspended').format(service),
                assigned_to=todo_settings.todo_user
            )
        return True

    def resume(self, service: Service) -> bool:
        LOG.debug('TODO module resume called for service {}:{}'.format(service.id, service))
        if hasattr(service.product, 'todo_settings'):
            todo_settings = service.product.todo_settings  # type: models.TODOProductSettings
        else:
            todo_settings = None

        if todo_settings and todo_settings.add_todo_on_resume:
            models.TODO.objects.add_todo(
                title=_('Service resumed'),
                description=_('Service {} was resumed').format(service),
                assigned_to=todo_settings.todo_user
            )
        return True

    def renew(self, service: Service) -> bool:
        LOG.debug('TODO module renew called for service {}:{}'.format(service.id, service))
        if hasattr(service.product, 'todo_settings'):
            todo_settings = service.product.todo_settings  # type: models.TODOProductSettings
        else:
            todo_settings = None

        if todo_settings and todo_settings.add_todo_on_renew:
            models.TODO.objects.add_todo(
                title=_('Service renewed'),
                description=_('Service was renewed').format(service),
                assigned_to=todo_settings.todo_user
            )
        return True

    def change_product(self, service: Service) -> bool:
        LOG.debug('TODO module change product called for service {}:{}'.format(service.id, service))
        if hasattr(service.product, 'todo_settings'):
            todo_settings = service.product.todo_settings  # type: models.TODOProductSettings
        else:
            todo_settings = None

        models.TODO.objects.add_todo(
            title=_('Service changed product'),
            description=_('Service product was changed for service {}').format(service),
            assigned_to=todo_settings.todo_user
        )
        return True

    def change_cycle(self, service: Service) -> bool:
        LOG.debug('TODO module change cycle called for service {}:{}'.format(service.id, service))
        if hasattr(service.product, 'todo_settings'):
            todo_settings = service.product.todo_settings  # type: models.TODOProductSettings
        else:
            todo_settings = None

        if todo_settings and todo_settings.add_todo_on_change_cycle:
            models.TODO.objects.add_todo(
                title=_('Service changed cycle'),
                description=_('Service cycle was changed for {}').format(service),
                assigned_to=todo_settings.todo_user
            )
        return True

    def prepare_delete_task(self, service: Service, user_id: Optional[int] = None) -> Optional[Signature]:
        LOG.debug('TODO module delete called for service {}:{}'.format(service.id, service))
        return add_todo_for_delete_service.si(service_id=service.id)

    def get_unsettled_usage(self, service: Service, end_datetime: datetime) -> ServiceUsage:
        LOG.debug('TODO module get unsettled usage called for service {}:{}'.format(service.id, service))
        return ServiceUsage(Decimal(0))

    def get_unpaid_usage(self, service) -> ServiceUsage:
        LOG.debug('TODO module get unpaid usage called for service {}:{}'.format(service.id, service))
        return ServiceUsage(Decimal(0))

    def get_estimated_usage(self, service: Service, usage_settings: UsageSettings) -> EstimatedUsage:
        LOG.debug('TODO module get dynamic price per second called for service {}:{}'.format(service.id, service))
        return EstimatedUsage()

    def collect_usage(self, service: Service, usage_settings: UsageSettings) -> bool:
        LOG.debug('TODO module collect usage called for service {}:{}'.format(service.id, service))
        return True

    def reset_usage(self, service: Service) -> bool:
        LOG.debug('TODO module reset usage called for service {}:{}'.format(service.id, service))
        return True

    def settle_usage(self, service, end_datetime: datetime) -> bool:
        LOG.debug('TODO module settle usage called for service {}:{}'.format(service.id, service))
        return True

    def get_usage_summary(self, service):
        LOG.debug('TODO module dynamic usage called for service {}:{}'.format(service.id, service))

    def get_billing_summary(self, service):
        LOG.debug('TODO module billing summary for service {}:{}'.format(service.id, service))

    def change_pricing_plan(self, service: Service, new_plan_id):
        LOG.debug('{} change pricing plan for service {}:{}'.format(self.module_name, service.id, service))
