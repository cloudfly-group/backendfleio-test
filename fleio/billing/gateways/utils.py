import inspect
import logging

from django.apps import apps
from django.db import IntegrityError

from fleio.billing.models import RecurringPaymentsOrder, Transaction
from fleio.billing.models import Gateway

LOG = logging.getLogger(__name__)

GATEWAY_TABLE_UPDATED = False

GATEWAY_NAME_PREFIX = 'fleio.billing.gateways.'

ACTION_MAP = {}

ACTION_MAP_UPDATED = False


def get_recurring_payments_model_path(gateway_name: str):
    return '{}{}.models.RecurringPayments'.format(GATEWAY_NAME_PREFIX, gateway_name)


def get_recurring_payment_method_path(gateway_name: str):
    return '{}{}.{}.recurring_payment'.format(GATEWAY_NAME_PREFIX, gateway_name, gateway_name)


def get_gateway_name_from_app_name(gateway_app_name: str):
    name = gateway_app_name.replace(GATEWAY_NAME_PREFIX, '')
    return name


def create_new_recurring_payments_ordering(client, gateway_app_name):
    order = 1
    other_ordering = RecurringPaymentsOrder.objects.filter(client=client).order_by('order').last()
    if other_ordering:
        order = other_ordering.order + 1
    try:
        return RecurringPaymentsOrder.objects.create(
            client=client,
            gateway_name=gateway_app_name.replace(GATEWAY_NAME_PREFIX, ''),
            order=order,
        )
    except IntegrityError:
        return None


def update_action_map():
    global ACTION_MAP, ACTION_MAP_UPDATED

    if ACTION_MAP_UPDATED:
        return

    update_gateways_table()

    for gateway in Gateway.objects.enabled():
        gateway_module = gateway.module
        if gateway_module is None:
            continue

        module_functions = inspect.getmembers(gateway_module, inspect.isfunction)

        actions_lists = {}

        for gateway_function in module_functions:
            func_name = gateway_function[0]
            func = gateway_function[1]
            if hasattr(func, 'staff_action') and func.staff_action:
                for transaction_status in func.transaction_statuses:
                    actions_lists.setdefault(transaction_status, [])
                    actions_lists[transaction_status].append({
                        'name': func_name,
                        'display': func.display_name,
                        'redirect': func.requires_redirect,
                        'gateway': gateway.name
                    })

        gateway_entry = {'gateway': gateway.name, 'action_lists': actions_lists}

        ACTION_MAP[gateway.name] = gateway_entry

    ACTION_MAP_UPDATED = True


def get_transaction_actions(transaction: Transaction) -> dict:
    update_action_map()
    gateway = transaction.gateway
    gateway_entry = ACTION_MAP.get(gateway.name)

    if gateway_entry is None:
        return {}

    action_list = gateway_entry.get('action_lists').get(transaction.status)

    if action_list is None:
        action_list = {}

    return action_list


def update_gateways_table():
    global GATEWAY_TABLE_UPDATED
    if GATEWAY_TABLE_UPDATED:
        return

    LOG.debug('Searching apps for billing gateways...')

    for app in apps.get_app_configs():
        if not app.name.startswith(GATEWAY_NAME_PREFIX):
            continue

        if not app.fleio_module_type == 'payment_gateway':
            continue

        try:
            LOG.debug('Processing app ''{}'''.format(app.name))
            name = app.name.replace(GATEWAY_NAME_PREFIX, '')
            existing_gateway = Gateway.objects.filter(name=name).first()

            if existing_gateway is None:
                Gateway.objects.create(
                    name=name,
                    display_name=app.verbose_name,
                    module_path=name,
                    module_settings=app.module_settings)
            else:
                existing_gateway.module_settings = app.module_settings
                existing_gateway.save()
        except Exception as ex:
            LOG.exception(ex)

    # TODO: remove non existing gateways from database
    GATEWAY_TABLE_UPDATED = True
