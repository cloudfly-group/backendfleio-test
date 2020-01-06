from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.response import Response

from fleio.billing.client_operations import ClientOperations
from fleio.billing.models import Invoice
from fleio.billing.models import Service
from fleio.billing.models.invoice import InvoiceStatus
from fleio.billing.serializers import ClientCreditMinSerializer
from fleio.billing.services.serializers import ServiceBriefSerializer
from fleio.core.drf import EndUserOnly
from fleio.core.features import active_features


@api_view(['GET'])
@permission_classes([EndUserOnly])
def billing_summary_view(request):
    client = request.user.clients.first()
    client_operations = ClientOperations(client=client)
    unpaid_usage = client_operations.client_usage.unpaid_usage
    uptodate_credit = client_operations.uptodate_credit
    other_credit = client.credits.exclude(currency=client.currency)
    services = ServiceBriefSerializer(many=True).to_representation(
        Service.objects.available_to_user(request.user))
    summary = {
        'credits': ClientCreditMinSerializer(instance=other_credit, many=True).data,
        'uptodate_credit': uptodate_credit,
        'billing_currency': client.currency.code,
        'unpaid_usage': unpaid_usage,
        'services': services,
    }

    if active_features.is_enabled('billing.invoices'):
        invoices_count = Invoice.objects.filter(client=client).count()
        unpaid_invoices_count = Invoice.objects.filter(client=client, status=InvoiceStatus.ST_UNPAID).count()
        paid_invoices_count = Invoice.objects.filter(client=client, status=InvoiceStatus.ST_PAID).count()
        summary['invoices_details'] = dict(
            invoices_count=invoices_count,
            unpaid_invoices_count=unpaid_invoices_count,
            paid_invoices_count=paid_invoices_count,
        )

    return Response(summary)
