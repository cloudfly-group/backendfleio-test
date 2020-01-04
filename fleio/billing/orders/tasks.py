import celery

from fleio.celery import app
from fleio.billing.models import Order
from fleio.billing.settings import OrderStatus, ProductAutoSetup, ServiceStatus
from fleio.billing.services.tasks import create_service


@app.task(throws=(Order.DoesNotExist, ), name='Process order items', resource_type='Order')
def process_order_items(order_id, **kwargs):
    order = Order.objects.get(id=order_id)

    # Process auto setup items on first order
    setup_on_order_tasks = list()
    for order_item in order.items.filter(service__isnull=False):
        setup_on_order_tasks.append(create_service.s(order_item.service_id, user_id=kwargs.get('user_id')))
    if len(setup_on_order_tasks):
        celery.group(setup_on_order_tasks).apply_async()


@app.task(throws=(Order.DoesNotExist, ), name='Accept order', resource_type='Order')
def order_accept(order_id, **kwargs):
    order = Order.objects.get(id=order_id)

    if order.status == OrderStatus.pending:
        # Process auto setup items on first order
        setup_on_order_accept = list()
        for order_item in order.items.filter(service__product__auto_setup__in=(ProductAutoSetup.manual,
                                                                               ProductAutoSetup.on_order),
                                             service__status=ServiceStatus.pending):
            setup_on_order_accept.append(create_service.s(order_item.service_id, user_id=kwargs.get('user_id')))
        if len(setup_on_order_accept):
            celery.group(setup_on_order_accept).apply_async()
    order.status = OrderStatus.completed
    order.save(update_fields=['status'])
