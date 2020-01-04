import logging

from django.conf import settings
from django.utils.module_loading import import_string
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.status import HTTP_202_ACCEPTED, HTTP_409_CONFLICT

from fleio.activitylog.utils.decorators import log_enduser_activity
from fleio.billing import utils
from fleio.billing.models.invoice import InvoiceStatus
from fleio.billing.operations import get_invoice_payment_options
from fleio.core.drf import EndUserOnly
from fleio.core.models import Client
from fleio.core.models import get_default_currency
from fleio.core.filters import CustomFilter
from fleio.billing.invoicing import tasks
from fleio.billing.models import Invoice, TaxRule
from fleio.billing.models import ClientCredit
from fleio.billing.settings import BillingItemTypes
from .serializers import InvoiceBriefSerializer, InvoiceDetailSerializer
from fleio.billing.serializers import AddCreditSerializer
from fleio.billing.invoicing.pdf import pdf_invoice
from io import BytesIO

LOG = logging.getLogger(__name__)


@log_enduser_activity(
    category_name='billing', object_name='invoice',
    additional_activities={
        'pay_from_credit_balance': _('User {username} ({user_id}) paid invoice {object_id} using credit.'),
    }
)
class InvoiceViewSet(viewsets.ReadOnlyModelViewSet):
    model = Invoice
    permission_classes = (EndUserOnly,)
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend, CustomFilter, filters.SearchFilter)
    filter_fields = ('status', 'client', 'id')
    ordering_fields = ('issue_date', 'due_date', 'status', 'client',)
    search_fields = ('id', 'first_name', 'last_name', 'status', 'due_date', 'number')
    ordering = ['id']

    def get_queryset(self):
        return Invoice.objects.filter(client__in=self.request.user.clients.all())

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return InvoiceDetailSerializer
        else:
            return InvoiceBriefSerializer

    @action(detail=False, methods=['POST'])
    def add_credit_invoice(self, request):
        serializer = AddCreditSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        try:
            client = request.user.clients.get(pk=serializer.validated_data['client'])
        except Client.DoesNotExist:
            raise ValidationError({'client': _('Client not found')})
        credit = serializer.validated_data['credit']
        # Look for unpaid invoices already containing credit addition
        credit_invoices_unpaid = Invoice.objects.filter(client=client).unpaid().for_credit()
        if credit_invoices_unpaid.count() > 0:
            raise ValidationError({'detail': _('An unpaid credit invoice already exists')})
        item_description_msg = _('Add {} {} to credit balance').format(credit, client.currency.code)
        item_taxes = []
        if client.billing_settings.add_tax_for_credit_invoices and not client.tax_exempt:
            client_tax_rules = TaxRule.for_country_and_state(
                country=client.country_name,
                state=client.state
            )
            if client_tax_rules:
                for tax_rule in client_tax_rules:
                    tax_amount = (credit * tax_rule.rate) / 100
                    tax_amount = utils.cdecimal(tax_amount, q='.01')
                    item_taxes.append({'name': tax_rule.name,
                                       'amount': tax_amount,
                                       'tax_rule': tax_rule.id})
        invoice_id = tasks.invoice_create(
            client.pk,
            items=[{
                'item_type': BillingItemTypes.credit,
                'amount': credit,
                'description': item_description_msg,
                'taxed': True if len(item_taxes) else False,
                'taxes': item_taxes,
            }],
            currency=client.currency.code,
            issue_date=now().isoformat(),
            due_date=now().isoformat()
        )
        return Response({'id': invoice_id})

    @action(detail=True, methods=['GET'])
    def payment_options(self, request, pk):
        invoice = self.get_object()
        return Response(get_invoice_payment_options(invoice=invoice))

    @action(detail=True, methods=['POST'])
    def pay_from_credit_balance(self, request, pk):
        invoice = self.get_object()
        if invoice.is_credit_invoice():
            # NOTE(tomo): do not allow payment from credit balance if this is a credit invoice
            return Response({'detail': _('Unable to pay a credit invoice with credit')}, status=HTTP_409_CONFLICT)
        if not invoice.is_unpaid():
            # NOTE(tomo): only unpaid invoices should be allowed
            return Response({'detail': _('Only unpaid invoices can be paid from credit')}, status=HTTP_409_CONFLICT)

        invoice_has_default_currency = True if invoice.currency.code == get_default_currency().code else False
        if not invoice_has_default_currency:
            try:
                credit_balance = invoice.client.credits.get(currency=invoice.currency).amount
            except ClientCredit.DoesNotExist as e:
                LOG.error(e)
                credit_balance = 0
        else:
            credit_balance = invoice.client.uptodate_credit
        if credit_balance <= 0:
            return Response({'detail': _('Not enough credit')}, status=HTTP_409_CONFLICT)

        invoice_balance = invoice.balance
        # don't allow payment if the remaining credit (only for up to date credit in default currency) will be less
        # than the minimum specified in client's configuration after paying the invoice
        if invoice_has_default_currency:
            min_credit_to_be_left = invoice.client.billing_settings.minim_uptodate_credit_for_invoice_payment
            not_enough_credit_response = Response(
                data={'detail': _('You should have at least {} {} credit left after making a payment')
                      .format(min_credit_to_be_left, invoice.client.currency)},
                status=HTTP_409_CONFLICT
            )
            if credit_balance >= invoice_balance:
                if credit_balance - invoice_balance < min_credit_to_be_left:
                    return not_enough_credit_response
            elif min_credit_to_be_left > 0:
                return not_enough_credit_response

        amount = 0

        if invoice_balance >= credit_balance > 0:
            amount = credit_balance
        elif credit_balance > invoice_balance > 0:
            amount = invoice_balance

        currency_code = invoice.client.currency.code
        tasks.invoice_add_payment.delay(
            invoice.id,
            amount=amount,
            currency_code=currency_code,
            from_credit_balance=True,
            user_id=request.user.pk,
            create_todo=invoice.client.billing_settings.create_todo_on_invoice_payment,
        )

        return Response({'detail': _('Adding {} {} to invoice'.format(amount, currency_code))},
                        status=HTTP_202_ACCEPTED)

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

        # NOTE(tomo): text on invoice can also be customise using the para tag
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
