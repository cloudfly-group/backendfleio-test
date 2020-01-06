import logging
import paypalrestsdk
from decimal import Decimal

from django.db import transaction as db_transaction
from django.http import HttpResponseRedirect
from django.utils.timezone import now as utcnow
from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import APIException

from fleio.activitylog.utils.activity_helper import activity_helper
from fleio.billing.gateways import exceptions as gateway_exceptions
from fleio.billing.gateways.decorators import gateway_action, staff_gateway_action
from fleio.billing.invoicing.tasks import invoice_add_payment, invoice_refund_payment
from fleio.billing.serializers import AddTransactionSerializer
from fleio.billing.models import Gateway, Invoice, Transaction
from fleio.billing.models.transaction import TransactionStatus
from fleio.core.utils import fleio_join_url
from fleio.settings import FRONTEND_URL
from .conf import conf

LOG = logging.getLogger(__name__)
gateway = Gateway.objects.get(module_path='paypal')


def configure():
    paypalrestsdk.configure({
        "mode": conf.mode,  # sandbox or live
        "client_id": conf.client_id,
        "client_secret": conf.client_secret})


def create_payment(invoice_id):
    invoice = Invoice.objects.get(id=invoice_id)

    items = []
    total_amount = Decimal(0)

    for item in invoice.items.all():
        total_amount += item.amount
        items.append({
            'name': item.description,
            'sku': item.description,
            'price': str(item.amount),
            'currency': invoice.currency.code,
            'quantity': 1
        })

    if not invoice.subtotal == total_amount:
        raise APIException(detail=_('Invoice price is not equal to sum of item prices.'))

    payment = paypalrestsdk.Payment({
        'intent': 'sale',
        'payer': {
            'payment_method': 'paypal'
        },
        'redirect_urls': {
            'return_url': '%sconfirm_payment?invoice=%s' % (conf.url_base, invoice_id),
            'cancel_url': '%scancel_payment?invoice=%s' % (conf.url_base, invoice_id)
        },
        'transactions': [
            {
                'invoice_number': invoice_id,
                'item_list':
                    {
                        'items': items
                    },
                'amount':
                    {
                        'total': str(invoice.total),
                        'currency': invoice.currency.code,
                        'details': {
                            'subtotal': str(invoice.subtotal),
                            'tax': str(invoice.total - invoice.subtotal)
                        }
                    },
                'description': 'This is the payment transaction description.'
            }
        ]
    })

    if not payment.create():
        raise APIException(detail=format_error(payment))

    return payment


def execute_payment(payment_id, payer_id):
    payment = paypalrestsdk.Payment.find(payment_id)

    if not payment.execute({'payer_id': payer_id}):
        raise APIException(detail=format_error(payment))


def get_payment(payment_id):
    payment = paypalrestsdk.Payment.find(payment_id)

    if payment is None:
        LOG.error('Payment %s not found' % payment_id)
        raise APIException(detail=_('Payment not found.'))

    return payment


def get_approval_url(payment):
    for link in payment.links:
        if link.rel == "approval_url":
            approval_url = str(link.href)
            return approval_url

    raise Exception('Approval url not found.')


def get_invoice_id(payment):
    return payment.transactions[0].invoice_number


def get_sale_id(payment):
    return payment.transactions[0].related_resources[0].sale.id


def get_payment_amount(payment):
    return payment.transactions[0].amount


def get_invoice_url(invoice_id):
    relative_url = 'billing/invoices/%s' % invoice_id
    return fleio_join_url(FRONTEND_URL, relative_url)


def format_error(payment):
    return 'Error: %s - %s' % (payment.error.get('name'), payment.error.get('message'))


@gateway_action(methods=['GET'])
def pay_invoice(request):
    invoice_id = request.query_params.get('invoice')
    try:
        Invoice.objects.get(pk=invoice_id, client__in=request.user.clients.all())  # type: Invoice
    except Invoice.DoesNotExist:
        raise gateway_exceptions.GatewayException(_('Invoice {} does not exist').format(invoice_id))
    try:
        configure()
        payment = create_payment(invoice_id)
    except Exception as create_payment_exception:
        raise gateway_exceptions.InvoicePaymentException(message=str(create_payment_exception), invoice_id=invoice_id)

    return HttpResponseRedirect(get_approval_url(payment))


@gateway_action(methods=['GET'])
def confirm_payment(request):
    # PayPal does a full-page redirect to the return_url that was specified when the payment was created,
    # with PayerID and paymentId appended to the URL.
    payment_id = request.query_params.get('paymentId')
    payer_id = request.query_params.get('PayerID')

    configure()

    payment = get_payment(payment_id)
    invoice_id = get_invoice_id(payment)
    amount = get_payment_amount(payment)

    LOG.info('Payment %s for invoice %s processed' % (payment_id, invoice_id))
    if payment.execute({'payer_id': payer_id}):
        sale_id = get_sale_id(payment)
        sale = paypalrestsdk.Sale.find(sale_id)

        try:
            existing_transaction = Transaction.objects.get(external_id=payment_id,
                                                           gateway=gateway)
            transaction_id = existing_transaction.id
        except Transaction.DoesNotExist:
            serializer_data = {'invoice': invoice_id,
                               'external_id': payment_id,
                               'amount': amount.total,
                               'currency': amount.currency,
                               'gateway': gateway.pk,
                               'fee': sale.transaction_fee.value,
                               'date_initiated': payment.update_time,
                               'extra': None,
                               'status': TransactionStatus.SUCCESS}
            tr_ser = AddTransactionSerializer(data=serializer_data)
            if tr_ser.is_valid(raise_exception=False):
                new_transaction = tr_ser.save()
                transaction_id = new_transaction.id
            else:
                raise gateway_exceptions.InvoicePaymentException(message=tr_ser.errors, invoice_id=invoice_id)
        else:
            # Update the transaction status only
            existing_transaction.status = TransactionStatus.SUCCESS
            existing_transaction.save(update_fields=['status'])

        activity_helper.start_generic_activity(
            category_name='paypal', activity_class='paypal payment',
            invoice_id=invoice_id
        )

        invoice_add_payment.delay(invoice_id=invoice_id,
                                  amount=amount.total,
                                  currency_code=amount.currency,
                                  transaction_id=transaction_id)

        activity_helper.end_activity()
    else:
        raise gateway_exceptions.InvoicePaymentException(message=format_error(payment), invoice_id=invoice_id)

    gateway.log_callback(external_id=payment_id,
                         status=payment.state,
                         data='',
                         error=False,
                         error_code='',
                         error_info='')

    return HttpResponseRedirect(get_invoice_url(invoice_id))


@gateway_action(methods=['GET'])
def cancel_payment(request):
    invoice_id = request.query_params.get('invoice')
    LOG.info('Invoice payment for %s canceled by user.' % invoice_id)

    return HttpResponseRedirect(get_invoice_url(invoice_id))


@staff_gateway_action(display_name=_('Refund'),
                      methods=['POST'],
                      transaction_statuses=[TransactionStatus.SUCCESS],
                      requires_redirect=False)
def refund(request):
    transaction_id = request.data.get('transaction')
    transaction = Transaction.objects.get(id=transaction_id, gateway__name='paypal')
    invoice = transaction.invoice
    payment_id = transaction.external_id

    configure()

    payment = get_payment(payment_id)
    sale_id = get_sale_id(payment)
    sale = paypalrestsdk.Sale.find(sale_id)
    sale.refund({
        'amount': {
            'total': str(transaction.amount),
            'currency': transaction.currency.code
        }})

    # update transaction and invoice status
    activity_helper.start_generic_activity(
        category_name='paypal', activity_class='paypal payment refund',
        invoice_id=invoice.pk
    )

    with db_transaction.atomic():
        new_transaction = Transaction.objects.create(invoice=invoice.pk,
                                                     external_id=payment_id,
                                                     amount=transaction.amount,
                                                     currency=transaction.currency.pk,
                                                     gateway=transaction.gateway.pk,
                                                     fee=0,
                                                     date_initiated=utcnow(),
                                                     extra='',
                                                     refunded_transaction=transaction.pk,
                                                     status=TransactionStatus.SUCCESS)

    db_transaction.on_commit(lambda: invoice_refund_payment.delay(transaction_id=transaction.id,
                                                                  amount=transaction.amount,
                                                                  to_client_credit=False,
                                                                  new_transaction_id=new_transaction.id))

    activity_helper.end_activity()

    return {'status': 'ok'}


'''
# test code
@staff_gateway_action(display_name=_('Error'),
                      methods=['GET'],
                      transaction_statuses=[TransactionStatus.SUCCESS],
                      requires_redirect=True)
def error(request):
    raise Exception('Some exception')
'''
