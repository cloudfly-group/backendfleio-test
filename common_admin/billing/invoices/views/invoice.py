import logging
from io import BytesIO

from django.conf import settings
from django.db import transaction as db_transaction
from django.http import HttpResponse
from django.utils.module_loading import import_string
from django.utils.timezone import now as utcnow
from django.utils.translation import ugettext_lazy as _
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from fleio.activitylog.utils.activity_helper import activity_helper
from fleio.billing.invoicing.pdf import pdf_invoice
from fleio.billing.invoicing.tasks import invoice_refund_payment
from fleio.billing.models import Gateway
from fleio.billing.models import Invoice
from fleio.billing.models import Journal
from fleio.billing.models import Transaction
from fleio.billing.models.invoice import InvoiceStatus
from fleio.billing.models.journal_sources import JournalSources
from fleio.billing.models.transaction import TransactionStatus
from fleio.billing.serializers import AddTransactionSerializer
from fleio.core.drf import SuperUserOnly
from fleio.core.models import Currency
from fleiostaff.billing.invoicing.serializers import StaffAddInvoicePaymentSerializer
from fleiostaff.billing.invoicing.serializers import StaffInvoiceBriefSerializer
from fleiostaff.billing.invoicing.serializers import StaffInvoiceDetailSerializer
from fleiostaff.billing.invoicing.serializers import StaffInvoiceSerializer

LOG = logging.getLogger(__name__)


class AdminInvoiceViewSet(ModelViewSet):
    permission_classes = (SuperUserOnly,)

    def get_queryset(self):
        return Invoice.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return StaffInvoiceDetailSerializer
        elif self.action in ('create', 'update',):
            return StaffInvoiceSerializer
        else:
            return StaffInvoiceBriefSerializer

    def perform_create(self, serializer):
        client = serializer.validated_data.get('client', None)
        if not client:
            raise APIException(_('No valid client was received'))
        currency = client.currency
        invoice = serializer.save(currency=currency)  # type: Invoice

        if invoice.client.billing_settings.invoicing_option == 'always_fiscal':
            invoice.make_fiscal()

        if invoice.status == InvoiceStatus.ST_PAID or invoice.balance == 0:
            # makes sure fiscal number is set and doesn't allow to issue an unpaid invoice with 0 balance
            # (automatically sets it as paid in this case)
            invoice.set_paid()

    @action(detail=True, methods=['GET'])
    def payment_options(self, request, pk):
        del request, pk  # unused
        self.get_object()
        gateways = Gateway.objects.visible_to_staff()
        currencies = Currency.objects.all()
        default_currency = Currency.objects.filter(is_default=True).first()
        response = {'gateways': [{'name': gw.name, 'display_name': gw.display_name, 'id': gw.id} for gw in gateways],
                    'currencies': [{'code': currency.code} for currency in currencies],
                    'defaultGateway': 0,
                    'defaultCurrency': default_currency.code}
        return Response(response)

    @action(detail=True, methods=['POST'])
    def add_payment_to_invoice(self, request, pk):
        del pk  # unused
        self.get_object()
        serializer = StaffAddInvoicePaymentSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        activity_helper.add_current_activity_params(
            amount=serializer.validated_data['amount'],
            currency_code=serializer.validated_data['currency'].code,
        )
        return Response({'detail': _('Payment added')})

    @action(detail=True, methods=['POST'])
    def perform_refund(self, request, pk):
        del pk  # unused
        invoice = self.get_object()
        transaction_id = request.data.get('transaction')
        refund_to_credit = request.data.get('refund_to_credit')
        amount = request.data.get('amount')
        external_id = request.data.get('external_id')
        refund_manually = request.data.get('refund_manually')
        existing_transaction = Transaction.objects.get(pk=transaction_id)
        new_transaction = None

        if not existing_transaction.is_refundable():
            raise APIException(detail=_('Transaction not in a refundable state'), code=400)

        if refund_manually:
            serializer_data = {'invoice': invoice.pk,
                               'external_id': external_id,
                               'amount': amount,
                               'currency': invoice.currency.code,
                               'gateway': existing_transaction.gateway.pk,
                               'fee': 0,
                               'date_initiated': utcnow(),
                               'extra': '',
                               'refunded_transaction': existing_transaction.pk,
                               'status': TransactionStatus.SUCCESS}
            tr_ser = AddTransactionSerializer(data=serializer_data)
            tr_ser.is_valid(raise_exception=True)
            new_transaction = tr_ser.save()

        invoice_refund_payment.delay(transaction_id=transaction_id,
                                     amount=amount,
                                     to_client_credit=refund_to_credit,
                                     new_transaction_id=(
                                         None if new_transaction is None
                                         else new_transaction.pk))

        return Response({'detail': _('Payment refund initiated')})

    @action(detail=True, methods=['POST'])
    def perform_delete(self, request, pk):
        del request, pk  # unused
        invoice = self.get_object()
        transactions_count = Transaction.objects.filter(invoice=invoice).count()

        if transactions_count > 0:
            raise APIException(_('Cannot delete invoice with associated transactions'), code=400)

        with db_transaction.atomic():
            for journal_entry in invoice.journalentries.all():  # type: Journal
                assert type(journal_entry) is Journal
                if journal_entry.source == JournalSources.credit:
                    # refund credit
                    invoice.client.add_credit(journal_entry.source_amount, journal_entry.source_currency)
                    journal_entry.delete()

            invoice.delete()

        return Response({'detail': _('Invoice deleted')})

    @action(detail=False, methods=['get'])
    def summary(self, request):
        del request  # unused
        invoices = Invoice.objects.all()
        invoice_info = {
            'paid': invoices.filter(status='Paid').count(),
            'unpaid': invoices.filter(status='Unpaid').count(),
            'cancelled': invoices.filter(status='Cancelled').count(),
            'refunded': invoices.filter(status='Refunded').count()
        }
        return Response(invoice_info)

    @action(detail=True, methods=['GET'])
    def download(self, request, pk):
        invoice = self.get_object()
        invoice_number = str(invoice.display_number).strip()
        invoice_file_name = 'invoice_{}.pdf'.format(invoice_number.replace(' ', '_'))
        response = HttpResponse()
        response['Content-Type'] = 'application/pdf'
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(invoice_file_name)
        pdf_file = BytesIO()
        # Add invoice taxes and total/subtotal
        invoice_totals = [{'name': _('Subtotal ({})').format(invoice.currency), 'value': invoice.subtotal}]
        for tax in invoice.taxes:
            invoice_totals.append({'name': tax.get('name'), 'value': tax.get('amount')})
        invoice_totals.append({'name': _('Total ({})').format(invoice.currency), 'value': invoice.total})

        # NOTE(tomo): text on invoice can also be customised using the para tag
        # Ex: invoice_status = '<para color="#ff880000">{}</para>'.format(invoice_status)
        # See the reportlab userguide for a full list of tag attributes
        try:
            try:
                customer_invoice_details_getter = import_string(getattr(settings, 'INVOICE_CUSTOMER_DETAILS_GETTER'))
            except ImportError:
                customer_details = None
            else:
                customer_details = customer_invoice_details_getter(invoice)
            invoice_statuses_dict = dict((key, translated) for key, translated in InvoiceStatus.PAYMENT_STATUSES)
            if invoice.is_fiscal:
                invoice_issue_date = invoice.fiscal_date.date() if invoice.fiscal_date else None
                invoice_due_date = invoice.fiscal_due_date.date() if invoice.fiscal_due_date else None
            else:
                invoice_issue_date = invoice.issue_date.date() if invoice.issue_date else None
                invoice_due_date = invoice.due_date.date() if invoice.due_date else None

            pdf_invoice(pdf_file=pdf_file,
                        invoice_display_number=invoice.name,
                        invoice_status=invoice_statuses_dict[invoice.status],
                        invoice_issue_date=invoice_issue_date,
                        invoice_due_date=invoice_due_date,
                        customer_details=customer_details if customer_details else invoice.client.long_name,
                        company_details=invoice.client.billing_settings.company_info,
                        invoice_items=[{'description': item.description,
                                        'quantity': 1,
                                        'unit_price': item.amount,
                                        'cost': item.amount,
                                        'options': [{'quantity': opt.quantity,
                                                     'unit_price': opt.unit_price,
                                                     'price': opt.price,
                                                     'display': opt.display} for opt in item.configurable_options.all()]
                                        } for item in invoice.items.all()],
                        invoice_totals=invoice_totals,
                        invoice_currency=invoice.currency.code,
                        invoice_lang=request.user.language if request.user.language else 'en')
        except Exception as e:
            LOG.exception(e)
            return Response(status=500, data={'details': 'Unable to download invoice'})
        else:
            response.write(pdf_file.getvalue())
            pdf_file.close()
        return response
