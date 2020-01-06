import logging
import operator
import os
import time
from functools import reduce
from typing import Dict, List
from typing import Optional

import bleach
import celery
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.db import transaction
from django.db.models import Q
from django.db.utils import IntegrityError

import fleio.billing.services.tasks as service_tasks
from fleio.billing.models import Order
from fleio.billing.models import Service
from fleio.billing.models import Product
from fleio.billing.models import OrderItemTypes
from fleio.billing.modules.factory import module_factory
from fleio.billing.orders.tasks import order_accept
from fleio.billing.settings import OrderStatus, ProductAutoSetup
from fleio.billing.settings import ServiceStatus
from fleio.celery import app
from fleio.core.antifraud.antifraud import FleioFraudCheck
from fleio.core.filters import CustomFilter
from fleio.core.models import AppUser
from fleio.core.models import Client
from fleio.core.models import UserToClient
from fleio.core.validation_utils import validate_services_limit
from fleio.core.utils import fleio_parse_url
from fleio.emailing import send_email
from fleio.notifications.models import NotificationTemplate
from fleio.reseller.utils import reseller_suspend_instead_of_terminate
from fleiostaff.core.utils import annotate_clients_queryset

LOG = logging.getLogger(__name__)


@app.task(bind=True, max_retries=settings.TASK_RETRIES, name='Delete client from database', resource_type='Client',
          throws=(IntegrityError,))
def delete_client_from_database(self, client_id: int):
    del self  # unused
    with transaction.atomic():
        client = Client.objects.get(id=client_id)  # type: Client

        # delete all users that are associated only with this client
        users_to_client = UserToClient.objects.filter(client=client)
        users_to_delete = [utc.user for utc in users_to_client if utc.user.clients.count() == 1]

        for user in users_to_delete:
            user.delete()

        # delete client
        client.delete()

        # delete user to client
        users_to_client.delete()


@app.task(bind=True, max_retries=settings.TASK_RETRIES, name='Terminate client', resource_type='Client')
def terminate_client(
        self, client_id: int, user_id: Optional[int] = None, delete_all_resources: Optional[bool] = False
):
    del self  # unused
    client = Client.objects.get(id=client_id)  # type: Client

    if client.billing_settings.suspend_instead_of_terminate or reseller_suspend_instead_of_terminate(client=client):
        raise Exception('Terminate client called when suspend instead of terminate is true')

    # delete all services for client
    delete_services_tasks = []

    for service in client.services.all():
        billing_module = module_factory.get_module_instance(service=service)
        if delete_all_resources:
            delete_services_tasks.append(
                celery.chain(
                    billing_module.prepare_delete_task(service=service, user_id=user_id),
                    service_tasks.delete_service_from_database.si(service_id=service.id)
                )
            )
        else:
            delete_services_tasks.append(service_tasks.delete_service_from_database.si(service_id=service.id))

    if len(delete_services_tasks):
        final_chord = celery.group(delete_services_tasks) | delete_client_from_database.si(client_id=client_id)
        celery.chain(
            final_chord
        ).apply_async()
    else:
        delete_client_from_database.delay(client_id=client_id)


@app.task(bind=True, max_retries=settings.TASK_RETRIES, name='Send reset password email', resource_type='User')
def send_reset_password_email(self, user_id):
    """
    Generates a one-use only link for resetting password and sends to the
    user.
    """

    del self  # unused
    user = AppUser.objects.get(pk=user_id)
    # get the notification template based on user language or default notifications language or any language
    # if the others were not found
    try:
        account_notification_template = NotificationTemplate.objects.get(
            name='account.reset.password',
            language=user.language
        )
    except NotificationTemplate.DoesNotExist:
        try:
            default_language = getattr(settings, 'DEFAULT_NOTIFICATION_TEMPLATE_LANGUAGE_CODE')
            account_notification_template = NotificationTemplate.objects.get(
                name='account.reset.password',
                language=default_language
            )
        except NotificationTemplate.DoesNotExist:
            account_notification_template = NotificationTemplate.objects.filter(name='account.reset.password').first()

    email_subject = account_notification_template.title
    email_body = account_notification_template.content

    # TODO(marius): use the user primary client when implemented, not the first()
    if user.clients.first():
        from_email = user.clients.first().billing_settings.sender_email
    else:
        from_email = None

    if user.is_staff:
        reset_password_frontend_page = fleio_parse_url(settings.FRONTEND_URL) + settings.STAFF_FRONTEND_URL_ENDPOINT
    else:
        if user.reseller_resources:
            reset_password_frontend_page = user.reseller_resources.enduser_panel_url
        else:
            reset_password_frontend_page = settings.FRONTEND_URL

    # TODO(Marius): this needs a precise split (if a billing account is in multiple groups)
    if settings.FRONTEND_URL_MAPPING:
        user_client = user.clients.first()
        if user_client:
            client_groups = user_client.groups.all()
            for group in client_groups:
                if group.name in settings.FRONTEND_URL_MAPPING:
                    reset_password_frontend_page = settings.FRONTEND_URL_MAPPING[group.name]
                    break

    to_email = user.email

    context = {
        'frontend_url': fleio_parse_url(reset_password_frontend_page),
        'user_id': user.pk,
        'token': default_token_generator.make_token(user),
        'user': user,
    }
    send_email(from_field=from_email, to_emails=to_email, subject_template=email_subject, body_template=email_body,
               params=context, is_html=True)


@app.task(max_retries=settings.TASK_RETRIES, name='Complete signup', resource_type='Client')
def complete_signup_task(client_id, user_id, product_id, order_metadata=None):
    """Called when the first client is created for a user"""
    client = Client.objects.get(pk=client_id)
    user = AppUser.objects.get(pk=user_id)
    if product_id:
        product = Product.objects.filter(id=product_id).first()
    else:
        product = None
    if product:
        if not validate_services_limit():
            # should actually not get here if limit is reached
            LOG.error('Cannot auto-create service and order because service limit was reached, aborting')
        product_order_params = client.billing_settings.auto_order_service_params
        product_cycle_id = client.billing_settings.auto_order_service_cycle or None
        with transaction.atomic():
            order = Order.objects.create(user=user,
                                         client=client,
                                         currency=client.currency,
                                         status=OrderStatus.pending,
                                         staff_notes='Auto ordered',
                                         metadata=order_metadata)
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
                                             plugin_data=item.plugin_data)
            item.service = service
            item.save(update_fields=['service'])

        if client.billing_settings.fraud_check:
            fraud_result = FleioFraudCheck().check_order(order)
            if fraud_result == FleioFraudCheck.FRAUD_RESULT_STATUS.ACCEPT:
                if product.auto_setup == ProductAutoSetup.on_order:
                    transaction.on_commit(lambda: order_accept.delay(order.id, user_id=user_id))
        else:
            if product.auto_setup == ProductAutoSetup.on_order:
                transaction.on_commit(lambda: order_accept.delay(order.id, user_id=user_id))
    else:
        LOG.warning('Auto create order on signup enabled but no product and cycle are defined')


@app.task(max_retries=0, name='Send mass email')
def send_mass_email(
        from_name_addr: str, subject: str, body: str, send_batch_size: int, send_interval: int,
        filtering: str, search: str, search_fields: str, attachments: Dict[str, str], allowed_variables: List[str],
):
    try:
        queryset = annotate_clients_queryset(Client.objects)
        if filtering:
            queryset = CustomFilter.get_filtered_queryset(queryset, filtering=filtering)
        if search:
            queries = [
                Q(**{'{}__icontains'.format(field_name): search})
                for field_name in search_fields
            ]
            queryset = queryset.filter(reduce(operator.or_, queries))

        current_batch_count = 0
        body = bleach.clean(body, strip=True)
        email_attachments = []
        for attachment_name, (attachment_file_path, content_type) in attachments.items():
            with open(attachment_file_path, 'rb') as attachment_file:
                email_attachments.append((
                    attachment_name, attachment_file.read(), content_type
                ))

        for client in queryset:
            try:
                params = {name: getattr(client, name, '') for name in allowed_variables}
                send_email(
                    from_field=from_name_addr,
                    to_emails=client.email,
                    subject_template=subject,
                    body_template=body,
                    params=params,
                    cc=None,
                    is_html=True,
                    attachments=email_attachments
                )
            except Exception as e:
                del e  # unused
                LOG.exception('Failed to send mail to client {} ({})'.format(client, client.id))
            current_batch_count += 1
            if current_batch_count >= send_batch_size:
                time.sleep(send_interval)
                current_batch_count = 0
    finally:
        for file_name, (file_path, content_type) in attachments.items():
            try:
                os.remove(file_path)
            except Exception as e:
                del e  # unused
