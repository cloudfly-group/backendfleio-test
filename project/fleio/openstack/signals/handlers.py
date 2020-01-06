import json
import logging

from django.conf import settings
from django.db import transaction
from django.dispatch import receiver

from fleio.billing.models import Order, OrderItemTypes, Product, Service
from fleio.billing.orders.tasks import order_accept
from fleio.billing.settings import OrderStatus, ProductAutoSetup, ServiceStatus
from fleio.core.models import AppUser
from fleio.core.signals import client_created
from fleio.core.validation_utils import validate_services_limit
from fleio.notifications import notifier
from fleio.openstack.notification_error_parser import ATTACHMENT_BUILDER_METHOD
from fleio.openstack.notification_error_parser import NotificationErrorParser
from fleio.openstack.signals.signals import openstack_error

LOG = logging.getLogger(__name__)


@receiver(client_created, dispatch_uid='client_created_openstack_callback')
def client_created_callback(sender, **kwargs):
    client = kwargs['client']

    LOG.info("client created invoked for client {}:{}".format(client.id, client.name))

    create_auto_order_service = kwargs.get('create_auto_order_service', False)
    auto_order_service_external_billing_id = kwargs.get('auto_order_service_external_billing_id', None)
    request_user_id = kwargs.get('request_user', None)
    request_user = AppUser.objects.filter(id=request_user_id).first()

    if create_auto_order_service:
        product_id = client.billing_settings.auto_order_service
        product = Product.objects.filter(id=product_id).first()
        if product:
            if not validate_services_limit():
                LOG.error('Cannot auto-create service and order because service limit was reached, aborting')
            product_order_params = client.billing_settings.auto_order_service_params
            product_cycle_id = client.billing_settings.auto_order_service_cycle or None
            with transaction.atomic():
                order = Order.objects.create(user=request_user,
                                             client=client,
                                             currency=client.currency,
                                             status=OrderStatus.pending,
                                             staff_notes='Auto ordered',)
                item = order.items.create(order=order,
                                          item_type=OrderItemTypes.service,
                                          product=product,
                                          name=product.name,
                                          cycle_id=product_cycle_id,
                                          plugin_data=product_order_params,
                                          taxable=(not client.tax_exempt))
                service = Service.objects.create(client=client,
                                                 display_name=item.name,
                                                 product=item.product,
                                                 cycle=item.cycle,
                                                 status=ServiceStatus.pending,
                                                 external_billing_id=auto_order_service_external_billing_id,
                                                 plugin_data=item.plugin_data)
                item.service = service
                item.save(update_fields=['service'])
            if product.auto_setup == ProductAutoSetup.on_order:
                order_accept.delay(order.id, user_id=request_user_id)
    else:
        LOG.info("Auto order service will not be created for client.")


@receiver(openstack_error, dispatch_uid='openstack_error_receiver')
def notify_on_openstack_error(sender, **kwargs):
    event_type = kwargs.get('event_type', None)
    if (not event_type or (event_type not in settings.SEND_OPENSTACK_ERRORS_ON_EVENTS and
                           '*' not in settings.SEND_OPENSTACK_ERRORS_ON_EVENTS)):
        # send notifications only for specified event types
        return
    payload = kwargs.get('payload', None)
    notification_error_parser = NotificationErrorParser(payload=payload, event_type=event_type)
    final_receivers = notification_error_parser.get_notification_receivers()
    if len(final_receivers):
        region = kwargs.get('region', None)
        # timestamp = kwargs.get('timestamp', None)
        error_message = notification_error_parser.get_exception_message()
        args = notification_error_parser.get_request_args()
        formatted_args = json.dumps(args, indent=2, separators=[',', ': '])

        variables = {
            'event_type': event_type,
            'error_message': error_message,
            'region': region,
            'request_args': formatted_args,
        }
        notifier.send(
            name='openstack.error',
            priority=notifier.Notification.PRIORITY_NORMAL,
            variables=variables,
            to_emails=final_receivers,
            attachments_builder=ATTACHMENT_BUILDER_METHOD,
            attachments_builder_args={
                'formatted_args': formatted_args,
                'event_type': event_type,
            }
        )
