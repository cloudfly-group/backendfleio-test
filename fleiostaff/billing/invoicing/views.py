import logging

from django.utils.translation import ugettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response

from common_admin.billing.invoices.views.invoice import AdminInvoiceViewSet
from fleio.activitylog.utils.decorators import log_staff_activity
from fleio.billing.models import Invoice
from fleio.billing.models import Service
from fleio.billing.models.invoice import InvoiceStatus
from fleio.billing.settings import BillingItemTypes
from fleio.core.drf import StaffOnly
from fleio.core.filters import CustomFilter
from fleiostaff.billing.services.serializers import StaffServiceSerializer

LOG = logging.getLogger(__name__)


@log_staff_activity(
    category_name='billing', object_name='invoice',
    additional_activities={
        'perform_delete': _('Staff user {username} ({user_id}) deleted invoice ({object_id}).'),
        'perform_refund': _('Staff user {username} ({user_id}) refunded invoice ({object_id}).'),
        'add_payment_to_invoice': _(
            'Staff user {username} ({user_id}) added a payment of {amount} {currency_code} to invoice ({object_id}).'
        ),
    }
)
class StaffInvoiceViewSet(AdminInvoiceViewSet):
    model = Invoice
    permission_classes = (StaffOnly,)
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend, CustomFilter, filters.SearchFilter)
    filter_fields = ('status', 'client', 'id')
    ordering_fields = ('issue_date', 'due_date', 'status', 'client',)
    search_fields = ('id', 'first_name', 'last_name', 'status', 'total', 'email', 'company', 'number')
    ordering = ['id']

    def get_queryset(self):
        return super().get_queryset().filter(client__reseller_resources__isnull=True)

    @action(detail=True, methods=['GET'])
    def create_options(self, request, pk):
        del request, pk  # unused
        invoice_item_types = dict(BillingItemTypes.CHOICES)
        invoice = self.get_object()
        services = Service.objects.filter(client=invoice.client)
        service_serializer = StaffServiceSerializer(services, many=True)
        return Response({'invoice_item_types': invoice_item_types,
                         'services': service_serializer.data})

    @action(detail=False, methods=['GET'])
    def invoice_create_options(self, request):
        del request  # unused
        invoice_item_types = dict(BillingItemTypes.CHOICES)
        invoice_statuses = InvoiceStatus.PAYMENT_STATUSES
        return Response({
            'invoice_item_types': invoice_item_types,
            'invoice_statuses': invoice_statuses,
        })
