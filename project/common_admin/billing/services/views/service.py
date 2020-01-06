import celery
from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import now as utcnow
from django.utils.translation import ugettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from fleio.billing.models import Service
from fleio.billing.models import TaxRule
from fleio.billing.modules.factory import module_factory
from fleio.billing.orders.utils import OrderMetadata
from fleio.billing.services import tasks
from fleio.billing.services.serializers import ServiceChangeOptionsSerializer
from fleio.billing.services.serializers import ServiceUpgOptionsSerializer
from fleio.billing.services.service_manager import ServiceManager
from fleio.billing.settings import ProductType
from fleio.billing.settings import ServiceStatus
from fleio.billing.settings import ServiceSuspendType
from fleio.billing.settlement_manager import SettlementManager
from fleio.core.drf import SuperUserOnly
from fleio.core.exceptions import APIBadRequest
from fleio.core.features import staff_active_features
from fleio.core.filters import CustomFilter
from fleio.reseller.utils import reseller_suspend_instead_of_terminate
from fleiostaff.billing.services.serializers import StaffHostingAccountSerializer
from fleiostaff.billing.services.serializers import StaffServiceDetailsSerializer
from fleiostaff.billing.services.serializers import StaffServiceSerializer
from fleiostaff.billing.services.serializers import StaffServiceUpdateSerializer


class AdminServiceViewSet(viewsets.ModelViewSet):
    permission_classes = (SuperUserOnly, )
    serializer_class = StaffServiceSerializer
    model = Service
    queryset = Service.objects.all()
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend, CustomFilter, filters.SearchFilter)
    filter_fields = ('id', 'display_name', 'client', 'status')
    ordering_fields = ('id', 'display_name', 'client', 'created_at', 'status', 'next_due_date')
    search_fields = ('id', 'display_name', 'client__first_name', 'client__last_name', 'status')
    ordering = ['display_name']

    def get_serializer_class(self):
        if self.action == 'update':
            return StaffServiceUpdateSerializer
        elif self.action == 'retrieve':
            return StaffServiceDetailsSerializer
        else:
            return self.serializer_class

    def get_queryset(self):
        if self.action == 'list':
            return self.queryset.filter(product__group__visible=True).all()

        return self.queryset

    @action(detail=True, methods=['post'])
    def activate(self, request, pk):
        service = self.get_object()
        if service.status in [
            ServiceStatus.pending,
            ServiceStatus.fraud,
            ServiceStatus.canceled,
            ServiceStatus.terminated,
        ]:
            if (service.product and service.product.product_type == ProductType.openstack and
                    service.status == ServiceStatus.terminated):
                return Response({
                    'detail': _(
                        'Re-activating a terminated openstack service is not supported. '
                        'Create a new one from client page.'
                    )
                }, status=status.HTTP_400_BAD_REQUEST)
            tasks.create_service.delay(pk, user_id=request.user.pk)
            return Response(
                {
                    'detail': _('Create in progress')
                },
                status=status.HTTP_202_ACCEPTED,
            )
        else:
            return Response(
                {
                    'detail': _('Service resources already exists.')
                },
                status=status.HTTP_403_FORBIDDEN,
            )

    @action(detail=True, methods=['post'])
    def resume(self, request, pk):
        service = self.get_object()
        if service.status in [ServiceStatus.suspended]:
            tasks.resume_service.delay(pk, user_id=request.user.pk)
            return Response(
                {
                    'detail': _('Resume in progress')
                },
                status=status.HTTP_202_ACCEPTED,
            )
        else:
            return Response(
                {
                    'detail': _('Service is not suspended')
                },
                status=status.HTTP_403_FORBIDDEN,
            )

    @action(detail=True, methods=['post'])
    def suspend(self, request, pk):
        service = self.get_object()
        if service.status in [ServiceStatus.active]:
            tasks.suspend_service.delay(pk, reason='Suspend from Frontend', user_id=request.user.pk)
            return Response(
                {
                    'detail': _('Suspend in progress')
                },
                status=status.HTTP_202_ACCEPTED,
            )
        else:
            return Response(
                {
                    'detail': _('Service is not active')
                },
                status=status.HTTP_403_FORBIDDEN,
            )

    @action(detail=True, methods=['post'])
    def terminate(self, request, pk):
        service = self.get_object()  # type: Service
        if service.status not in [ServiceStatus.active, ServiceStatus.suspended]:
            return Response(
                {
                    'detail': _('Service is not active or suspended')
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        if service.client.billing_settings.suspend_instead_of_terminate or reseller_suspend_instead_of_terminate(
            client=service.client,
        ):
            if service.status == ServiceStatus.active:
                tasks.suspend_service.delay(
                    service_id=service.id,
                    reason=ServiceSuspendType.SUSPEND_REASON_TERMINATE_DISABLED,
                    suspend_type=ServiceSuspendType.staff,
                )
                return Response(
                    {
                        'detail': _('Suspend instead of terminate is enabled for the client. Suspending service.')
                    },
                    status=status.HTTP_202_ACCEPTED,
                )
            else:
                return Response(
                    {
                        'detail': _(
                            'Suspend instead of terminate is enabled for the client and service is not active.'
                        )
                    },
                    status=status.HTTP_202_ACCEPTED,
                )
        else:
            tasks.terminate_service.delay(pk, user_id=request.user.pk)
            return Response(
                {
                    'detail': _('Terminate in progress')
                },
                status=status.HTTP_202_ACCEPTED,
            )

    def destroy(self, request, *args, **kwargs):
        service = self.get_object()
        if service.client.billing_settings.suspend_instead_of_terminate or reseller_suspend_instead_of_terminate(
            client=service.client,
        ):
            if self.request.query_params.get('delete_associated_resources', 'false') == 'true':
                tasks.suspend_service.delay(
                    service_id=service.id,
                    reason=ServiceSuspendType.SUSPEND_REASON_TERMINATE_DISABLED,
                    suspend_type=ServiceSuspendType.staff,
                )
                return Response(
                    {
                        'detail': _('Suspend instead of terminate is enabled for the client. Suspending service.')
                    },
                    status=status.HTTP_202_ACCEPTED
                )
            else:
                return Response(
                    {'detail': _('Suspend instead of terminate is enabled for the client, service not deleted.')},
                    status=status.HTTP_403_FORBIDDEN
                )
        else:
            if self.request.query_params.get('delete_associated_resources', 'false') == 'true':
                billing_module = module_factory.get_module_instance(service=service)
                delete_task = billing_module.prepare_delete_task(service=service, user_id=request.user.id)
                celery.chain(
                    delete_task,
                    tasks.delete_service_from_database.si(service_id=service.id)
                ).apply_async()
                return Response(
                    {'detail': _('Delete in progress.')},
                    status=status.HTTP_202_ACCEPTED
                )
            else:
                if service.status in [
                    ServiceStatus.terminated,
                    ServiceStatus.canceled,
                    ServiceStatus.pending,
                    ServiceStatus.fraud
                ]:
                    tasks.delete_service_from_database.si(service_id=service.id).apply_async()
                    return Response(
                        {'detail': _('Delete in progress.')},
                        status=status.HTTP_202_ACCEPTED
                    )
                else:
                    return Response(
                        {
                            'detail': _('Cannot delete service with active resources, terminate service first.')
                        },
                        status=status.HTTP_403_FORBIDDEN
                    )

    @action(detail=True, methods=['put'])
    def update_hosting_account(self, request, pk):
        del pk  # unused
        service = self.get_object()
        try:
            hosting_account = service.hosting_account
        except ObjectDoesNotExist:
            return Response({'detail': 'Service has no hosting account associated'})
        serializer = StaffHostingAccountSerializer(instance=hosting_account, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'Hosting account updated'})

    @action(detail=True, methods=['get'])
    def upgrade_options(self, request, pk):
        del request, pk  # unused
        service = self.get_object()
        serializer_context = {'request': self.request, 'view': self}
        response = ServiceChangeOptionsSerializer(instance=service,
                                                  context=serializer_context).to_representation(service)
        return Response(response)

    @action(detail=True, methods=['post'])
    def upgrade(self, request, pk):
        del pk  # unused
        service = self.get_object()
        ser = ServiceUpgOptionsSerializer(data=request.data, context={'service': service})
        ser.is_valid(raise_exception=True)
        configurable_options = ser.validated_data.get('configurable_options')
        upgrade_summary = ServiceManager.estimate_new_service_cycle_cost(service=service,
                                                                         product=ser.validated_data['product'],
                                                                         cycle=ser.validated_data['cycle'],
                                                                         start_date=utcnow(),
                                                                         configurable_options=configurable_options)
        if ser.validated_data.get('confirm', False):
            order_metadata = OrderMetadata.from_request(request).to_json()
            invoice = ServiceManager.create_service_upgrade_order(user=service.client.users.first(),
                                                                  client=service.client,
                                                                  service=service,
                                                                  product=ser.validated_data['product'],
                                                                  cycle=ser.validated_data['cycle'],
                                                                  start_date=utcnow(),
                                                                  configurable_options=configurable_options,
                                                                  metadata=order_metadata)
            return Response({'invoice': invoice.pk})
        else:
            return Response(upgrade_summary)

    @action(detail=True, methods=['post'])
    def invoice(self, request, pk):
        del request, pk  # unused
        service = self.get_object()

        SettlementManager.create_invoice_for_services(
            client=service.client,
            services=[service],
            tax_rules=TaxRule.for_country_and_state(
                country=service.client.country,
                state=service.client.state,
            ),
            manual_invoice=True,
        )

        return Response({'detail': _('Invoice issued')})

    @action(detail=True, methods=['post'])
    def update_billing_plan(self, request, pk):
        del pk  # unused
        if not staff_active_features.is_enabled('openstack.plans'):
            raise APIBadRequest(detail=_('Cannot update os plan because openstack plans feature is disabled'))
        service = self.get_object()  # type: Service
        if service.status in [
            ServiceStatus.terminated,
            ServiceStatus.canceled,
            ServiceStatus.fraud
        ]:
            raise APIBadRequest(_('Cannot change pricing plan for service in this state.'))
        new_plan_id = request.data.get('plan')
        billing_module = module_factory.get_module_instance(service=service)
        billing_module.change_pricing_plan(service=service, new_plan_id=new_plan_id)
        return Response({'detail': _('Pricing plan updated')})
