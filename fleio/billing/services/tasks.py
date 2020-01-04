import logging

from django.conf import settings
from django.db import transaction
from django.db.utils import OperationalError

from fleio.billing.exceptions import ServiceException
from fleio.billing.models import ConfigurableOption
from fleio.billing.models import Product, ProductCycle, Service
from fleio.billing.modules.factory import module_factory
from fleio.billing.settings import ServiceSuspendType
from fleio.celery import app
from fleio.reseller.utils import reseller_suspend_instead_of_terminate

LOG = logging.getLogger(__name__)


@app.task(bind=True, max_retries=settings.TASK_RETRIES,
          autoretry_for=(ServiceException, OperationalError), name='Create service', resource_type='Service')
def create_service(self, service_id, **kwargs):
    del self, kwargs  # unused

    service = Service.objects.get(pk=service_id)
    service_module = module_factory.get_module_instance(service=service)
    result = service_module.create(service=service)
    if result:
        service.set_active()
    return service.id


@app.task(bind=True, max_retries=settings.TASK_RETRIES,
          autoretry_for=(ServiceException, OperationalError), name='Suspend service', resource_type='Service')
def suspend_service(self, service_id, reason, suspend_type=None, **kwargs):
    del self, kwargs  # unused

    service = Service.objects.get(pk=service_id)
    LOG.debug('Suspending service {} for client {} ({})'.format(
        service_id, service.client.name, service.client.id,
    ))

    service_module = module_factory.get_module_instance(service=service)
    result = service_module.suspend(service=service, reason=reason)
    if result:
        service.set_suspended(reason=reason, suspend_type=suspend_type)
    return result


@app.task(bind=True, max_retries=settings.TASK_RETRIES, autoretry_for=(ServiceException, OperationalError),
          name='Resume service', resource_type='Service')
def resume_service(self, service_id, **kwargs):
    del self, kwargs  # unused

    service = Service.objects.get(pk=service_id)
    service_module = module_factory.get_module_instance(service=service)
    result = service_module.resume(service=service)
    if result:
        service.set_active()
        service.client.set_active()
    return result


@app.task(bind=True, max_retries=settings.TASK_RETRIES, autoretry_for=(ServiceException, OperationalError),
          name='Renew service', resource_type='Service')
def renew_service(self, service_id, **kwargs):
    del self, kwargs  # unused

    service = Service.objects.get(pk=service_id)
    service_module = module_factory.get_module_instance(service=service)
    result = service_module.renew(service=service)
    return result


@app.task(bind=False, max_retries=settings.TASK_RETRIES, autoretry_for=(ServiceException, OperationalError),
          name='Change product service', resource_type='Service')
def change_product_service(service_id, product_id, cycle_id, configurable_options):
    product = Product.objects.get(pk=product_id)
    cycle = ProductCycle.objects.get(pk=cycle_id)
    with transaction.atomic():
        service = Service.objects.select_for_update().get(pk=service_id)
        previous_due_date = service.get_previous_due_date()
        service_module = module_factory.get_module_instance(service=service)
        # Update configurable options
        for opt in configurable_options:
            try:
                opt['option'] = ConfigurableOption.objects.get(pk=opt['option'])
            except ConfigurableOption.DoesNotExist:
                continue
            existing_opt = service.configurable_options.filter(option=opt['option']).first()
            if not existing_opt:
                service.configurable_options.create(**opt)
            else:
                if opt['option'].widget == 'yesno' and opt['option_value'] == 'no':
                    service.configurable_options.filter(option=opt['option']).delete()
                else:
                    service.configurable_options.filter(option=opt['option']).update(**opt)
        service.product = product
        service.cycle = cycle
        service.override_price = None  # Disable overridden price if it exists since we upgraded the product
        service.display_name = product.name
        service.update_next_invoice_date(previous_due_date=previous_due_date)
        service.update_next_due_date(previous_due_date=previous_due_date)
        service.save()
        # Set configurable options here
        result = service_module.change_product(service=service)
        service.task = None
        service.save(update_fields=['task'])
    return result


@app.task(bind=True, max_retries=settings.TASK_RETRIES, autoretry_for=(ServiceException, OperationalError),
          name='Change cycle service', resource_type='Service')
def change_cycle_service(self, service_id, cycle_id, configurable_options):
    del self  # unused

    cycle = ProductCycle.objects.get(pk=cycle_id)
    with transaction.atomic():
        service = Service.objects.select_for_update().get(pk=service_id)
        previous_due_date = service.get_previous_due_date()
        service_module = module_factory.get_module_instance(service=service)
        # Update configurable options
        for opt in configurable_options:
            try:
                opt['option'] = ConfigurableOption.objects.get(pk=opt['option'])
            except ConfigurableOption.DoesNotExist:
                continue
            existing_opt = service.configurable_options.filter(option=opt['option']).first()
            if not existing_opt:
                service.configurable_options.create(**opt)
            else:
                if opt['option'].widget == 'yesno' and opt['option_value'] == 'no':
                    service.configurable_options.filter(option=opt['option']).delete()
                else:
                    service.configurable_options.filter(option=opt['option']).update(**opt)

        service.cycle = cycle
        service.override_price = None  # Disable overridden price if it exists since we upgraded the cycle
        service.update_next_invoice_date(previous_due_date=previous_due_date)
        service.update_next_due_date(previous_due_date=previous_due_date)
        service.save()
        result = service_module.change_cycle(service=service)
        service.task = None
        service.save(update_fields=['task'])
    return result


@app.task(max_retries=settings.TASK_RETRIES,
          autoretry_for=(ServiceException, OperationalError), name='Delete service from database',
          resource_type='Service')
def delete_service_from_database(service_id):
    service = Service.objects.filter(id=service_id).first()
    try:
        # TODO: move this to openstack when we make distinction between termination and deletion in billing modules
        if service.openstack_project:
            service.openstack_project.delete()
    except Exception as e:
        del e  # unused
    if service:
        service.delete()


@app.task(bind=True, max_retries=settings.TASK_RETRIES,
          autoretry_for=(ServiceException, OperationalError), name='Terminate service', resource_type='Service')
def terminate_service(self, service_id, cancellation_request_id=None, **kwargs):
    del self, kwargs  # unused

    service = Service.objects.get(pk=service_id)
    service_module = module_factory.get_module_instance(service=service)
    if service.client.billing_settings.suspend_instead_of_terminate or reseller_suspend_instead_of_terminate(
        client=service.client,
    ):
        LOG.info('Suspend instead of terminate is active, will suspend the service {}'.format(service_id))
        result = service_module.suspend(
            service=service,
            reason=ServiceSuspendType.SUSPEND_REASON_TERMINATE_DISABLED,
            suspend_type=ServiceSuspendType.staff
        )
        if result:
            service.set_suspended(
                reason=ServiceSuspendType.SUSPEND_REASON_TERMINATE_DISABLED,
                suspend_type=ServiceSuspendType.staff
            )
    else:
        LOG.info('Service will be terminated: {}'.format(service_id))
        service_module.prepare_delete_task(service=service).apply()
        service.set_terminated(cancellation_request_id=cancellation_request_id)
    return service.id
