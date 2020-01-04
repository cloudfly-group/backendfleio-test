from django.db import transaction
from django.utils.timezone import now as utcnow
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.translation import ugettext_lazy as _

from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import APIException

from fleio.billing.models import Service
from fleio.billing.models import CancellationRequest
from fleio.billing.models.calcelation_request import CancellationTypes
from fleio.billing.orders.utils import OrderMetadata
from fleio.billing.serializers import CancellationRequestBriefSerializer
from fleio.billing.services import tasks
from fleio.billing.services.serializers import ServiceBriefSerializer, ServiceChangeOptionsSerializer
from fleio.billing.services.serializers import ServiceUpgOptionsSerializer
from fleio.billing.services.service_manager import ServiceManager

from fleio.core.drf import EndUserOnly
from fleio.core.exceptions import APIBadRequest
from fleio.core.filters import CustomFilter


class ServicesViewset(viewsets.ReadOnlyModelViewSet):
    serializer_class = ServiceBriefSerializer
    model = Service
    permission_classes = (EndUserOnly,)
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend, CustomFilter, filters.SearchFilter)
    filter_fields = ('id', 'display_name', 'status')
    ordering_fields = ('display_name', 'created_at', 'status', 'next_due_date')
    search_fields = ('id', 'display_name', 'status')
    ordering = ['display_name']

    def get_queryset(self):
        queryset = Service.objects.available_to_user(self.request.user)
        if self.action == 'list':
            queryset = queryset.filter(product__group__visible=True, product__hide_services=False).all()
        return queryset

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk):
        service = self.get_object()
        if service.cancellation_request:
            raise APIException(_('A cancellation request already exists for this service'))

        serializer = CancellationRequestBriefSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cancellation_type = serializer.validated_data['cancellation_type']
        with transaction.atomic():
            cancel_request = CancellationRequest.objects.create(user=self.request.user,
                                                                reason=serializer.validated_data['reason'],
                                                                cancellation_type=cancellation_type)
            service.cancellation_request = cancel_request
            service.save(update_fields=['cancellation_request'])

        if cancellation_type == CancellationTypes.IMMEDIATE:
            transaction.on_commit(lambda: tasks.terminate_service.delay(pk, cancellation_request_id=cancel_request.pk,
                                                                        user_id=request.user.pk))
        return Response({'detail': _('Cancellation request created')}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def upgrade_options(self, request, pk):
        service = self.get_object()
        serializer_context = {'request': self.request, 'view': self}
        response = ServiceChangeOptionsSerializer(instance=service,
                                                  context=serializer_context).to_representation(service)
        return Response(response)

    @action(detail=True, methods=['post'])
    def upgrade(self, request, pk):
        del pk  # unused
        service = self.get_object()

        if not service.next_invoice_date:
            raise APIBadRequest(detail=_('Unpaid service cannot be upgraded/downgraded'))

        ser = ServiceUpgOptionsSerializer(data=request.data, context={'service': service})
        ser.is_valid(raise_exception=True)
        configurable_options = ser.validated_data.get('configurable_options')
        confirmation = ser.validated_data.get('confirm', False)

        upgrade_summary = ServiceManager.estimate_new_service_cycle_cost(service=service,
                                                                         product=ser.validated_data['product'],
                                                                         cycle=ser.validated_data['cycle'],
                                                                         start_date=utcnow(),
                                                                         configurable_options=configurable_options)
        if confirmation:
            order_metadata = OrderMetadata.from_request(request).to_json()
            invoice = ServiceManager.create_service_upgrade_order(user=request.user,
                                                                  client=request.user.clients.first(),
                                                                  service=service,
                                                                  product=ser.validated_data['product'],
                                                                  cycle=ser.validated_data['cycle'],
                                                                  start_date=utcnow(),
                                                                  configurable_options=configurable_options,
                                                                  metadata=order_metadata)
            return Response({'invoice': invoice.pk})
        else:
            return Response(upgrade_summary)
