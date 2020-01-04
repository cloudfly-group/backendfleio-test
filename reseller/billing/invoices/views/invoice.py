import logging

from django.utils.translation import ugettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response

from common_admin.billing.invoices.views.invoice import AdminInvoiceViewSet
from fleio.activitylog.utils.decorators import log_reseller_activity
from fleio.billing.models import Invoice
from fleio.billing.models import Service
from fleio.billing.models.invoice import InvoiceStatus
from fleio.billing.settings import BillingItemTypes
from fleio.core.drf import CustomPermissions
from fleio.core.drf import ResellerOnly
from fleio.core.filters import CustomFilter
from fleio.reseller.utils import user_reseller_resources
from fleiostaff.billing.services.serializers import StaffServiceSerializer

LOG = logging.getLogger(__name__)


@log_reseller_activity(
    category_name='billing', object_name='invoice',
    additional_activities={
        'perform_delete': _('Reseller user {username} ({user_id}) deleted invoice ({object_id}).'),
        'perform_refund': _('Reseller user {username} ({user_id}) refunded invoice ({object_id}).'),
        'add_payment_to_invoice': _(
            'Reseller user {username} ({user_id}) added a payment of {amount} {currency_code} to invoice ({object_id}).'
        ),
    }
)
class ResellerInvoiceViewSet(AdminInvoiceViewSet):
    model = Invoice
    permission_classes = (CustomPermissions, ResellerOnly,)
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend, CustomFilter, filters.SearchFilter)
    filter_fields = ('status', 'client', 'id')
    ordering_fields = ('issue_date', 'due_date', 'status', 'client',)
    search_fields = ('id', 'first_name', 'last_name', 'status', 'total', 'email', 'company', 'number')
    ordering = ['id']

    def get_queryset(self):
        reseller_resources = user_reseller_resources(user=self.request.user)
        queryset = super().get_queryset().filter(
            client__reseller_resources=reseller_resources
        )

        return queryset

    @action(detail=False, methods=['GET'])
    def create_options(self, request):
        del request  # unused
        invoice_item_types = dict(BillingItemTypes.CHOICES)
        invoice_statuses = InvoiceStatus.PAYMENT_STATUSES
        return Response({
            'invoice_item_types': invoice_item_types,
            'invoice_statuses': invoice_statuses,
            'services': [],
        })

    @action(detail=False, methods=['get'])
    def summary(self, request):
        del request  # unused
        reseller_resources = user_reseller_resources(self.request.user)
        invoices = Invoice.objects.filter(client__reseller_resources=reseller_resources)
        invoice_info = {
            'paid': invoices.filter(status='Paid').count(),
            'unpaid': invoices.filter(status='Unpaid').count(),
            'cancelled': invoices.filter(status='Cancelled').count(),
            'refunded': invoices.filter(status='Refunded').count()
        }
        return Response(invoice_info)

    @action(detail=True, methods=['GET'])
    def invoice_edit_options(self, request, pk):
        del request  # unused
        invoice_item_types = dict(BillingItemTypes.CHOICES)
        invoice = self.get_object()
        services = Service.objects.filter(client=invoice.client)
        service_serializer = StaffServiceSerializer(services, many=True)
        invoice_statuses = InvoiceStatus.PAYMENT_STATUSES
        return Response({
            'invoice_item_types': invoice_item_types,
            'services': service_serializer.data,
            'invoice_statuses': invoice_statuses,
        })
