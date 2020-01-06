import logging
import decimal

from django.conf import settings
from django.http import HttpResponseRedirect

from fleio.activitylog.utils.activity_helper import activity_helper
from fleio.billing.gateways import exceptions
from fleio.billing.invoicing.tasks import invoice_add_payment
from fleio.billing.invoicing.tasks import invoice_refund_payment
from fleio.billing.serializers import AddTransactionSerializer
from fleio.billing.models import Gateway, Transaction
from fleio.billing.models.transaction import TransactionStatus
from fleio.core.utils import fleio_join_url
from .utils import invoice_id_from_api

LOG = logging.getLogger(__name__)


def process_response(resp):
    gateway = Gateway.objects.get(name='romcard')
    external_id = resp.get('external_id')
    transaction_status = resp.get('transaction_status')
    transaction_error = resp.get('error', False)
    invoice = invoice_id_from_api(resp.get('invoice'))
    transaction_id = None
    if external_id is not None and not transaction_error:
        # Check for duplicate transaction based on external ID and NONCE
        possible_duplicates = Transaction.objects.filter(external_id=external_id,
                                                         gateway=gateway)
        for pdup in possible_duplicates:
            if (pdup.extra.get('RRN') == resp.get('transaction_extra', {}).get('RRN') and
                    pdup.extra.get('NONCE') == resp.get('transaction_extra', {}).get('NONCE')):
                # Dupliocate transaction
                LOG.warning('Romcard duplicate transaction {} ignored'.format(external_id))
                return HttpResponseRedirect(fleio_join_url(settings.FRONTEND_URL, 'billing/invoices'))

        existing_transaction = Transaction.objects.filter(
            external_id=external_id,
            gateway=gateway,
            refunded_transaction__isnull=True
        ).first()
        if existing_transaction:
            transaction_id = existing_transaction.pk
            # Update the transaction status only
            existing_transaction.status = transaction_status
            existing_transaction.save(update_fields=['status'])
        else:
            serializer_data = {'invoice': invoice,
                               'external_id': external_id,
                               'amount': resp['amount'],
                               'currency': resp['currency'],
                               'gateway': gateway.pk,
                               'fee': gateway.get_fee(amount=decimal.Decimal(resp['amount'])),
                               'date_initiated': resp['transaction_date'],
                               'extra': resp['transaction_extra'],
                               'status': resp['transaction_status']}
            tr_ser = AddTransactionSerializer(data=serializer_data)
            if tr_ser.is_valid(raise_exception=False):
                new_transaction = tr_ser.save()
                transaction_id = new_transaction.pk
            else:
                LOG.error('Romcard transaction error: {}'.format(tr_ser.errors))
                raise exceptions.InvoicePaymentException('Transaction error', invoice_id=invoice)

    gateway.log_callback(external_id=external_id,
                         status=resp.get('transaction_status', 'unknown'),
                         data=resp.get('log_data'),
                         error=transaction_error,
                         error_code=resp.get('error_code'),
                         error_info=resp.get('error_info'))
    if transaction_error:
        raise exceptions.InvoicePaymentException(resp.get('error_info', 'error'), invoice_id=invoice)
    else:
        relative_invoice_url = 'billing/invoices/{0}'.format(invoice)
        relative_staff_invoice_url = 'staff/billing/invoices/{0}'.format(invoice)
        if transaction_status == TransactionStatus.PREAUTH:
            activity_helper.start_generic_activity(
                category_name='romcard', activity_class='romcard payment',
                invoice_id=invoice
            )

            invoice_add_payment.delay(invoice_id=invoice,
                                      amount=resp.get('amount'),
                                      currency_code=resp.get('currency'),
                                      transaction_id=transaction_id)

            activity_helper.end_activity()

            return HttpResponseRedirect(fleio_join_url(settings.FRONTEND_URL, relative_invoice_url))
        elif transaction_status == TransactionStatus.CONFIRMED:
            if resp.get('is_recurring', False):
                activity_helper.start_generic_activity(
                    category_name='romcard', activity_class='romcard payment',
                    invoice_id=invoice
                )
                invoice_add_payment.delay(
                    invoice_id=invoice,
                    amount=resp.get('amount'),
                    currency_code=resp.get('currency'),
                    transaction_id=transaction_id
                )
                activity_helper.end_activity()
            Transaction.objects.filter(external_id=external_id,
                                       refunded_transaction__isnull=True).update(status=TransactionStatus.CONFIRMED)
            return HttpResponseRedirect(fleio_join_url(settings.FRONTEND_URL, relative_staff_invoice_url))
        elif transaction_status in (TransactionStatus.REFUNDED, TransactionStatus.PARTIAL_REFUNDED):
            existing_transaction = Transaction.objects.filter(
                external_id=external_id,
                refunded_transaction__isnull=True
            ).first()
            if not existing_transaction:
                LOG.error(
                    'Error when processing transaction that should have RRN (external_id) set to {}'.format(external_id)
                )
                raise exceptions.InvoicePaymentException('Transaction error', invoice_id=invoice)

            new_refund_transaction = {'invoice': invoice,
                                      'external_id': external_id,
                                      'amount': resp.get('amount'),
                                      'currency': resp['currency'],
                                      'gateway': gateway.pk,
                                      'fee': gateway.get_fee(amount=decimal.Decimal(resp['amount'])),
                                      'date_initiated': resp['transaction_date'],
                                      'extra': resp['transaction_extra'],
                                      'refunded_transaction': existing_transaction.pk,
                                      'status': transaction_status}
            tr_ser = AddTransactionSerializer(data=new_refund_transaction)
            if tr_ser.is_valid(raise_exception=False):
                new_transaction = tr_ser.save()
            else:
                LOG.error('Romcard transaction error: {}'.format(tr_ser.errors))
                raise exceptions.InvoicePaymentException('Transaction error', invoice_id=invoice)

            activity_helper.start_generic_activity(
                category_name='romcard', activity_class='romcard payment refund',
                invoice_id=invoice
            )

            invoice_refund_payment.delay(transaction_id=transaction_id,
                                         amount=resp.get('amount'),
                                         to_client_credit=False,
                                         new_transaction_id=new_transaction.pk)

            activity_helper.end_activity()

            return HttpResponseRedirect(fleio_join_url(settings.FRONTEND_URL, relative_staff_invoice_url))
        else:
            LOG.warning('Romcard callback not processed: {}'.format(resp))
            return HttpResponseRedirect(fleio_join_url(settings.FRONTEND_URL, 'billing/invoices'))
