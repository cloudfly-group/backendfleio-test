import decimal

from django.conf import settings
from django.db import transaction
from django.utils.timezone import now as utcnow
from django.utils.translation import ugettext_lazy as _

from fleio.billing.models import FleioCart
from fleio.billing.models import Order
from fleio.billing.models import OrderItem  # noqa
from fleio.billing.models import OrderItemTypes
from fleio.billing.models import Service
from fleio.billing.models import TaxRule
from fleio.billing.modules.base import BillingError
from fleio.billing.modules.factory import module_factory
from fleio.billing.settings import OrderStatus
from fleio.billing.settings import ServiceStatus
from fleio.billing.settlement_manager import SettlementManager
from fleio.billing.utils import cdecimal
from fleio.core.exceptions import APIBadRequest
from fleio.core.validation_utils import validate_services_limit
from fleio.notifications.notifier import send_staff_notification


def create_order_from_cart(cart: FleioCart):
    with transaction.atomic():
        order = Order.objects.create(user=cart.user,
                                     client=cart.client,
                                     currency=cart.currency,
                                     client_notes='',
                                     metadata=cart.metadata,
                                     status=OrderStatus.pending)
        cart.items.update(order=order, cart=None)
        for item in order.items.filter(item_type=OrderItemTypes.service):
            # Create services for all items of type service
            create_service_for_item(item)

        SettlementManager.process_order(order=order)
        if order.client.reseller_resources:
            frontend_url = order.client.reseller_resources.enduser_panel_url
        else:
            frontend_url = getattr(settings, 'FRONTEND_URL', '')

        send_staff_notification(
            name='staff.new_order',
            variables={
                'frontend_url': frontend_url,
                'client_name': cart.client.name,
                'client_id': cart.client.id,
                'order_id': order.id,
            }
        )
        return order


def create_service_for_item(item):
    try:
        if not validate_services_limit():
            raise APIBadRequest(
                _('Failed to create service, please contact support'),
            )
        with transaction.atomic():
            service = Service.objects.create(client=item.order.client,
                                             display_name=item.name,
                                             product=item.product,
                                             cycle=item.cycle,
                                             status=ServiceStatus.pending,
                                             next_due_date=utcnow(),
                                             plugin_data=item.plugin_data,
                                             domain_name=item.domain_name)
            for config_option in item.configurable_options.all():
                service.configurable_options.create(option=config_option.option,
                                                    option_value=config_option.option_value,
                                                    quantity=config_option.quantity,
                                                    has_price=config_option.has_price,
                                                    taxable=config_option.taxable,
                                                    price=config_option.price,
                                                    unit_price=config_option.unit_price,
                                                    setup_fee=config_option.setup_fee)
            billing_module = module_factory.get_module_instance(service=service)
            if not billing_module.initialize(service=service):
                raise BillingError(_('Failed to initialize service'))
    except BillingError:
        # failed to initialize service
        # TODO: see what action should we take here
        pass
    else:
        item.service = service
        item.save(update_fields=['service'])


def get_order_item_prices(cart, product, quantity, cycle=None):
    """Get the prices for an order item, when adding one to the cart or updating it"""
    zero = decimal.Decimal('0.00')
    setup_fee = zero
    fixed_price = zero
    if cycle:
        if cycle.setup_fee:
            if cycle.setup_fee_entire_quantity:
                price = cycle.setup_fee
            else:
                price = cycle.setup_fee * quantity
            setup_fee = price
        if cycle.fixed_price:
            fixed_price = cycle.fixed_price * quantity
    fixed_price = fixed_price
    setup_fee = setup_fee
    if cart and cart.client and not cart.client.tax_exempt and product.taxable:
        taxable = True
    else:
        taxable = False
    return fixed_price, setup_fee, taxable


def get_client_taxes_amount_by_price(price, client=None, taxable=False):
    if client is None or client.tax_exempt or not taxable:
        # If this is a tax exempted client, just return
        # or item not taxable, continue to the next one
        return []
    taxes = []
    tax_rules = TaxRule.for_country_and_state(country=client.country_name, state=client.state)
    for tax_rule in tax_rules:
        tax_amount = cdecimal(price * (tax_rule.rate / 100), q='0.01')
        tax_name = tax_rule.name
        taxes.append({'name': tax_name, 'amount': tax_amount})
    return taxes
