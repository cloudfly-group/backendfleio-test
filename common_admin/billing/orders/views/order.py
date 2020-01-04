from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_202_ACCEPTED
from rest_framework.status import HTTP_422_UNPROCESSABLE_ENTITY

from fleio.billing.models import Order
from fleio.billing.models.invoice import InvoiceStatus
from fleio.billing.modules.factory import module_factory
from fleio.billing.orders.tasks import order_accept
from fleio.billing.settings import OrderStatus
from fleio.billing.settings import ServiceStatus
from fleio.core.drf import SuperUserOnly
from fleio.core.filters import CustomFilter
from fleiostaff.billing.orders.serializers import StaffOrderSerializer


class AdminOrderViewSet(viewsets.ModelViewSet):
    permission_classes = (SuperUserOnly,)
    serializer_class = StaffOrderSerializer
    model = Order
    queryset = StaffOrderSerializer.Meta.model.objects.all()
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend, CustomFilter, filters.SearchFilter)
    filter_fields = ('id', 'order_date', 'status', 'client_notes', 'staff_notes')
    ordering_fields = ('id', 'client', 'user', 'order_date', 'status')
    search_fields = ('id', 'client__first_name', 'client__last_name',
                     'status', 'client_notes', 'staff_notes', 'user__username')
    ordering = ['-id']

    @action(detail=True, methods=['POST'])
    def accept(self, request: Request, pk) -> Response:
        del pk  # unused
        order = self.get_object()
        can_accept = True
        messages = []
        for item in order.items.all():
            if item.service:
                billing_module = module_factory.get_module_instance(service=item.service)
                can_accept_service, message = billing_module.can_accept_order(service=item.service)
                can_accept = can_accept and can_accept_service
                if not can_accept_service:
                    messages.append(message)
        if can_accept:
            order_accept.delay(order.id, user_id=request.user.pk)
            return Response({'detail': 'Accepted'}, status=HTTP_202_ACCEPTED)
        else:
            return Response(
                {
                    'detail': 'Cannot accept order',
                    'messages': messages
                },
                status=HTTP_422_UNPROCESSABLE_ENTITY,
            )

    @action(detail=True, methods=['POST'])
    def verify(self, request: Request, pk) -> Response:
        del request, pk  # unused
        order = self.get_object()
        order.status = OrderStatus.verified
        order.save(update_fields=['status'])
        return Response({'detail': 'Accepted'}, status=HTTP_202_ACCEPTED)

    @action(detail=True, methods=['POST'])
    def cancel(self, request, pk):
        del request, pk  # unused
        order = self.get_object()
        order.status = OrderStatus.cancelled
        order.save(update_fields=['status'])
        for item in order.items.all():
            if item.service and item.service.status == ServiceStatus.pending:
                item.service.set_status(new_status=ServiceStatus.canceled)

        if order.invoice and order.invoice.is_unpaid():
            order.invoice.set_status(new_status=InvoiceStatus.ST_CANCELLED)

        return Response({'detail': 'Accepted'}, status=HTTP_202_ACCEPTED)

    @action(detail=True, methods=['POST'])
    def pending(self, request, pk):
        del request, pk  # unused
        order = self.get_object()
        order.status = OrderStatus.pending
        order.save(update_fields=['status'])
        return Response({'detail': 'Accepted'}, status=HTTP_202_ACCEPTED)

    @action(detail=True, methods=['POST'])
    def delete(self, request, pk):
        del request, pk  # unused
        order = self.get_object()
        order.delete()
        return Response({'detail': 'Accepted'}, status=HTTP_202_ACCEPTED)
