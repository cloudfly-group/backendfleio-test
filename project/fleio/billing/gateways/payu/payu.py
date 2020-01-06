import requests
import json
import logging
import decimal

from ipware.ip import get_ip

from django.http import HttpResponseRedirect
from django.utils.timezone import now as utcnow
from django.utils.translation import ugettext_lazy as _

from rest_framework.response import Response

from fleio.activitylog.utils.activity_helper import activity_helper
from fleio.billing.models.transaction import TransactionStatus
from fleio.billing.serializers import AddTransactionSerializer
from fleio.core.models import Client

from fleio.billing.gateways.decorators import gateway_action, staff_gateway_action
from fleio.billing.gateways import exceptions as gateway_exceptions
from fleio.billing.models import Gateway, Invoice, Transaction
from fleio.billing.invoicing.tasks import invoice_add_payment, invoice_refund_payment

from .utils import PayUTransactionStatus, PayUUtils
from .conf import conf


LOG = logging.getLogger(__name__)


class PayUClient:
    def __init__(self, invoice_id=None, request=None):
        self.invoice_id = invoice_id
        self.request = request

    @staticmethod
    def get_access_token():
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.post(conf.authorization_url, data={
            'grant_type': 'client_credentials',
            'client_id': conf.client_id,
            'client_secret': conf.client_secret,
        }, headers=headers)
        if response.status_code == 200 or response.status_code == 201:
            return json.loads(response.text)
        raise Exception('Could not get access token')

    def create_order(self):
        if not self.invoice_id:
            raise Exception('Cannot process request without invoice details.')
        db_invoice = Invoice.objects.filter(id=self.invoice_id).first()  # type: Invoice
        if not db_invoice:
            raise Exception('Cannot process request for invoice that does not exist.')
        if not self.request:
            raise Exception('Cannot create order without having a request.')
        db_client = db_invoice.client  # type: Client
        token_data = self.get_access_token()
        # compose request data
        request_data = {
            'notifyUrl': conf.notify_url,
            'customerIp': get_ip(self.request),
            'extOrderId': PayUUtils.generate_external_order_id(invoice_id=db_invoice.id),
            'merchantPosId': conf.merchant_pos_id,
            'description': 'Invoice {}'.format(self.invoice_id),
            'currencyCode': db_invoice.currency.pk,
            'totalAmount': str(PayUUtils.get_fleio_amount_in_payu_amount(amount=db_invoice.balance)),
            'buyer': {
                'email': db_client.email,
                'phone': db_client.phone,
                'firstName': db_client.first_name,
                'lastName': db_client.last_name,
            },
            'products': [{
                'name': item.item_type,
                'unitPrice': str(PayUUtils.get_fleio_amount_in_payu_amount(amount=item.amount)),
                'quantity': '1',
            } for item in db_invoice.items.all()],
            'payMethods': {
                'payMethod': {
                    'type': 'PBL',
                    'value': 'c',
                }
            }
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(token_data['access_token'])
        }
        response = requests.post(conf.orders_url, data=json.dumps(request_data), headers=headers)
        if response.status_code == 200 or response.status_code == 201:
            return HttpResponseRedirect(response.url)
        error_details = json.loads(response.text)
        error_details_status = error_details.get('status')
        raise Exception('Could not create order. {}'.format(error_details_status.get('statusDesc')))

    def capture_order(self, transaction_external_id: str):
        token_data = self.get_access_token()
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(token_data['access_token'])
        }
        data = {
            'orderId': transaction_external_id,
            'orderStatus': 'COMPLETED'
        }
        return requests.put(
            url='{}/{}/status'.format(conf.orders_url, transaction_external_id),
            data=json.dumps(data),
            headers=headers
        )

    def refund(self, transaction_external_id: str):
        token_data = self.get_access_token()
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(token_data['access_token'])
        }
        data = {
            'refund': {
                'description': 'Refund'
            }
        }
        return requests.post(
            url='{}/{}/refunds'.format(conf.orders_url, transaction_external_id),
            data=json.dumps(data),
            headers=headers
        )

    def cancel(self, transaction_external_id: str):
        token_data = self.get_access_token()
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(token_data['access_token'])
        }
        return requests.delete(url='{}/{}'.format(conf.orders_url, transaction_external_id), headers=headers)


@gateway_action(methods=['GET'])
def pay_invoice(request):
    invoice_id = request.query_params.get('invoice')
    try:
        Invoice.objects.get(pk=invoice_id, client__in=request.user.clients.all())  # type: Invoice
    except Invoice.DoesNotExist:
        raise gateway_exceptions.GatewayException(_('Invoice {} does not exist').format(invoice_id))
    try:
        payu_client = PayUClient(invoice_id=invoice_id, request=request)
        return payu_client.create_order()
    except Exception as create_payment_exception:
        raise gateway_exceptions.InvoicePaymentException(message=str(create_payment_exception), invoice_id=invoice_id)


@staff_gateway_action(
    methods=['GET'], requires_redirect=True, transaction_statuses=(Transaction.TRANSACTION_STATUS.PREAUTH,)
)
def capture(request):
    transaction_id = request.query_params.get('transaction')
    transaction = Transaction.objects.get(id=transaction_id)
    invoice = transaction.invoice
    payu_client = PayUClient(invoice_id=invoice.id, request=request)

    try:
        response = payu_client.capture_order(transaction_external_id=transaction.external_id)
    except Exception as e:
        raise gateway_exceptions.GatewayException('Invalid payu capture: {}'.format(str(e)))
    if response.status_code == 200 or response.status_code == 201:
        transaction.status = TransactionStatus.CONFIRMED
        try:
            transaction.save()
        except Exception as e:
            # do nothing if it's being updated on the callback
            del e  # unused
        return Response({'detail': 'Ok'})
    response_text = json.loads(response.text)
    status = response_text.get('status')
    status_desc = status.get('statusDesc')
    raise Exception('Could not make capture action. {}'.format(status_desc if status_desc else ''))


@staff_gateway_action(
    methods=['GET'], requires_redirect=True,
    transaction_statuses=(Transaction.TRANSACTION_STATUS.CONFIRMED, Transaction.TRANSACTION_STATUS.PREAUTH)
)
def refund(request):
    gateway = Gateway.objects.get(name='payu')
    transaction_id = request.query_params.get('transaction')
    transaction = Transaction.objects.get(id=transaction_id)
    invoice = transaction.invoice
    payu_client = PayUClient(invoice_id=invoice.id, request=request)
    if transaction.status == Transaction.TRANSACTION_STATUS.CONFIRMED:
        # do a refund for transaction status confirmed
        try:
            response = payu_client.refund(transaction_external_id=transaction.external_id)
        except Exception as e:
            raise gateway_exceptions.GatewayException('Invalid payu refund action: {}'.format(str(e)))
        if response.status_code == 200 or response.status_code == 201:
            response_text = json.loads(response.text)
            refund_data = response_text.get('refund', {})
            new_refund_transaction = {
                'invoice': invoice.id,
                'external_id': transaction.external_id,
                'amount': str(PayUUtils.get_payu_amount_in_fleio_amount(refund_data.get('amount'))),
                'currency': refund_data.get('currencyCode'),
                'gateway': gateway.pk,
                'fee': gateway.get_fee(amount=decimal.Decimal(transaction.amount)),
                'date_initiated': refund_data.get('creationDateTime'),
                'extra': {
                    'refundId': refund_data.get('refundId'),
                    'extRefundId': refund_data.get('extRefundId'),
                },
                'refunded_transaction': transaction.pk,
                'status': TransactionStatus.REFUNDED
            }
            transaction_serializer = AddTransactionSerializer(data=new_refund_transaction)
            if transaction_serializer.is_valid(raise_exception=False):
                new_transaction = transaction_serializer.save()
                activity_helper.start_generic_activity(
                    category_name='payu', activity_class='payu payment refund',
                    invoice_id=invoice.id
                )

                invoice_refund_payment.delay(transaction_id=transaction_id,
                                             amount=PayUUtils.get_payu_amount_in_fleio_amount(
                                                 refund_data.get('amount')),
                                             to_client_credit=False,
                                             new_transaction_id=new_transaction.pk)

                activity_helper.end_activity()
            else:
                LOG.error('PayU transaction error: {}'.format(transaction_serializer.errors))
                raise gateway_exceptions.InvoicePaymentException('Transaction error', invoice_id=invoice.id)
            return Response({'detail': 'Ok'})
    else:
        # do a cancellation request for when transaction was not yet confirmed
        try:
            payu_client.cancel(transaction_external_id=transaction.external_id)
        except Exception as e:
            raise gateway_exceptions.GatewayException('Invalid payu refund action: {}'.format(str(e)))
        return Response({'detail': 'Ok'})
    response_text = json.loads(response.text)
    status = response_text.get('status')
    status_desc = status.get('statusDesc')
    raise Exception('Could not make capture action. {}'.format(status_desc if status_desc else ''))


@gateway_action(methods=['GET', 'POST'])
def callback(request):
    if not PayUUtils.validate_open_payu_signature(
            open_payu_signature=request.headers.get('OpenPayu-Signature', None),
            body=request.body,
    ):
        raise gateway_exceptions.GatewayException('Did not receive or received invalid OpenPayu-Signature')
    gateway = Gateway.objects.get(name='payu')
    order_details = request.data.get('order', None)
    if not order_details:
        raise Exception('No order details')
    external_id = order_details.get('orderId')
    invoice_id = PayUUtils.get_invoice_id_from_external_order_id(external_order_id=order_details.get('extOrderId'))
    transaction_status = order_details.get('status')
    total_amount = PayUUtils.get_payu_amount_in_fleio_amount(amount=order_details.get('totalAmount'))
    if order_details.get('status') == PayUTransactionStatus.canceled:
        # process refund for pre auth transaction
        existing_transaction = Transaction.objects.filter(
            external_id=external_id,
            gateway=gateway,
            refunded_transaction__isnull=True
        ).first()
        if not existing_transaction:
            raise gateway_exceptions.GatewayException(
                'Could not process cancellation notification because there is no transaction to refund'
            )
        new_refund_transaction = {
            'invoice': invoice_id,
            'external_id': external_id,
            'amount': str(total_amount),
            'currency': order_details.get('currencyCode'),
            'gateway': gateway.pk,
            'fee': gateway.get_fee(amount=decimal.Decimal(total_amount)),
            'date_initiated': utcnow(),
            'extra': {},
            'refunded_transaction': existing_transaction.pk,
            'status': TransactionStatus.REFUNDED
        }
        transaction_serializer = AddTransactionSerializer(data=new_refund_transaction)
        if transaction_serializer.is_valid(raise_exception=False):
            new_transaction = transaction_serializer.save()
            activity_helper.start_generic_activity(
                category_name='payu', activity_class='payu payment refund',
                invoice_id=existing_transaction.invoice.id
            )

            invoice_refund_payment.delay(transaction_id=existing_transaction.id,
                                         amount=total_amount,
                                         to_client_credit=False,
                                         new_transaction_id=new_transaction.pk)

            activity_helper.end_activity()
        else:
            LOG.error('PayU transaction error: {}'.format(transaction_serializer.errors))
            raise gateway_exceptions.GatewayException(
                'Could not process cancellation notification because serialized data is invalid'
            )
        return Response({'detail': 'Ok'})
    # process pre-auth, confirmation notifications
    existing_transaction = Transaction.objects.filter(
        external_id=external_id,
        gateway=gateway,
        refunded_transaction__isnull=True
    ).first()
    if existing_transaction:
        # Update the transaction status and mark invoice as paid (still needs capture if automatic capture is not
        # enabled in PayU) if client successfully made the payment
        existing_transaction.status = PayUTransactionStatus.to_transaction_model_status.get(transaction_status)
        existing_transaction.save(update_fields=['status'])
        if (transaction_status == PayUTransactionStatus.waiting_for_confirmation or
                (transaction_status == PayUTransactionStatus.completed and existing_transaction.invoice and
                 existing_transaction.invoice.is_unpaid())):
            activity_helper.start_generic_activity(
                category_name='payu', activity_class='payu payment',
                invoice_id=invoice_id
            )
            invoice_add_payment.delay(
                invoice_id=invoice_id,
                amount=total_amount,
                currency_code=order_details.get('currencyCode'),
                transaction_id=existing_transaction.id
            )
            activity_helper.end_activity()
        return Response({'detail': 'Ok'})
    elif transaction_status == PayUTransactionStatus.pending:
        serializer_data = {
            'invoice': invoice_id,
            'external_id': external_id,
            'amount': total_amount,
            'currency': order_details.get('currencyCode'),
            'gateway': gateway.pk,
            'fee': gateway.get_fee(amount=decimal.Decimal(total_amount)),
            'date_initiated': order_details.get('orderCreateDate'),
            'extra': {},
            'status': PayUTransactionStatus.to_transaction_model_status.get(transaction_status)
        }
        add_transaction_serializer = AddTransactionSerializer(data=serializer_data)
        if add_transaction_serializer.is_valid(raise_exception=False):
            add_transaction_serializer.save()
        else:
            LOG.error('PayU transaction error: {}'.format(add_transaction_serializer.errors))
            raise gateway_exceptions.InvoicePaymentException('Transaction error', invoice_id=invoice_id)
    return Response({'detail': 'Ok'})
