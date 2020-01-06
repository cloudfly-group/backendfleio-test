import json
import logging
import datetime
import decimal

from django.utils.translation import ugettext_lazy as _

from fleio.activitylog.utils.activity_helper import activity_helper
from fleio.billing.invoicing.tasks import invoice_add_payment
from fleio.billing.serializers import AddTransactionSerializer
from fleio.billing.models import Gateway
from fleio.billing.models import Transaction
from fleio.billing.models.transaction import TransactionStatus
from fleio.billing.invoicing.tasks import invoice_refund_payment
from fleio.billing.gateways import exceptions
from . import utils


LOG = logging.getLogger(__name__)


def charge_status(charge):
    if charge.status == 'succeeded':
        if charge.paid:
            if charge.captured:
                return TransactionStatus.SUCCESS
            elif not charge.captured:
                return TransactionStatus.PREAUTH
            elif charge.amount_refunded:
                if charge.refunded:
                    return TransactionStatus.REFUNDED
                else:
                    return TransactionStatus.PARTIAL_REFUNDED
    elif charge.status == 'failed':
        return TransactionStatus.FAILURE


def refund_status(refund):
    if refund.status == 'succeeded':
        return TransactionStatus.SUCCESS
    elif refund.status == 'failed':
        return TransactionStatus.FAILURE
    elif refund.status == 'pending':
        return TransactionStatus.WAITING
    elif refund.status == 'canceled':
        return TransactionStatus.CANCELED
    else:
        return TransactionStatus.UNKNOWN


def process_charge(charge):
    """Process a charge result"""
    gateway = Gateway.objects.get(name='stripe')
    external_id = charge.id
    transaction_id = None
    transaction_status = charge_status(charge)
    invoice_id = charge.metadata.get('invoice')
    if external_id is not None:
        try:
            existing_transaction = Transaction.objects.get(external_id=external_id,
                                                           gateway=gateway)
            transaction_id = existing_transaction.id
        except Transaction.DoesNotExist:
            real_amount = utils.convert_amount_from_api(charge.amount, charge.currency)
            serializer_data = {'invoice': invoice_id,
                               'external_id': external_id,
                               'amount': real_amount,
                               'currency': charge.currency.upper(),
                               'gateway': gateway.pk,
                               'fee': gateway.get_fee(amount=real_amount),
                               'date_initiated': datetime.datetime.fromtimestamp(charge.created),
                               'extra': {},
                               'status': transaction_status}
            tr_ser = AddTransactionSerializer(data=serializer_data)
            if tr_ser.is_valid(raise_exception=False):
                new_transaction = tr_ser.save()
                transaction_id = new_transaction.id
            else:
                LOG.error('Could not process charge for stripe: {}'.format(json.dumps(tr_ser.errors)))
                raise exceptions.InvoicePaymentException(
                    'Could not process charge for invoice {}.', invoice_id=invoice_id
                )
        else:
            # Update the transaction status only
            existing_transaction.status = transaction_status
            existing_transaction.save(update_fields=['status'])
    gateway.log_callback(external_id=external_id,
                         status=charge.status,
                         data=charge,
                         error=(charge.status == 'failed'),
                         error_code=charge.failure_code,
                         error_info=charge.failure_message)
    if transaction_status == TransactionStatus.FAILURE:
        raise exceptions.GatewayException(charge.failure_message or 'error')
    else:
        if transaction_status == TransactionStatus.SUCCESS:
            activity_helper.start_generic_activity(
                category_name='stripe', activity_class='stripe payment',
                invoice_id=invoice_id
            )

            invoice_add_payment.delay(invoice_id=invoice_id,
                                      amount=utils.convert_amount_from_api(charge.amount, charge.currency),
                                      currency_code=charge.currency.upper(),
                                      transaction_id=transaction_id)

            activity_helper.end_activity()


def process_refund(refund):
    # FIXME(tomo): This does not support partial refunds
    # Partial refunds should be allowed if the invoice balance is higher than the requested amount
    # Right now, creating a partial refund will set the transaction to refunded even if you refund
    # less than the payment value.
    gateway = Gateway.objects.get(name='stripe')
    external_id = refund.id
    existing_transaction_id = None
    invoice_id = None
    if refund.status == 'succeeded':
        if external_id is not None:
            try:
                existing_transaction = Transaction.objects.get(external_id=refund.charge,
                                                               gateway=gateway)
                existing_transaction_id = existing_transaction.pk
                invoice_id = existing_transaction.invoice_id
            except Transaction.DoesNotExist:
                raise exceptions.GatewayException('Transaction does not exist')
            else:
                existing_transaction.status = TransactionStatus.REFUNDED
                existing_transaction.save(update_fields=['status'])
        gateway.log_callback(external_id=external_id,
                             status=refund.status,
                             data=refund,
                             error=False)
        # Create a new refund transaction
        real_amount = utils.convert_amount_from_api(refund.amount, refund.currency)
        created_date = datetime.datetime.fromtimestamp(refund.created)
        new_transaction_status = TransactionStatus.REFUNDED
        new_refund_transaction = {'invoice': invoice_id,
                                  'external_id': external_id,
                                  'amount': real_amount,
                                  'currency': refund.currency,
                                  'gateway': gateway.pk,
                                  'fee': gateway.get_fee(amount=decimal.Decimal(real_amount)),
                                  'date_initiated': created_date,
                                  'extra': {'balance_transaction': refund.balance_transaction},
                                  'refunded_transaction': existing_transaction_id,
                                  'status': new_transaction_status}
        tr_ser = AddTransactionSerializer(data=new_refund_transaction)
        if tr_ser.is_valid(raise_exception=False):
            new_transaction = tr_ser.save()
            new_transaction_id = new_transaction.id

            activity_helper.start_generic_activity(
                category_name='stripe', activity_class='stripe payment refund',
                invoice_id=invoice_id
            )

            invoice_refund_payment.delay(transaction_id=new_transaction.refunded_transaction.pk,
                                         amount=utils.convert_amount_from_api(refund.amount, refund.currency),
                                         to_client_credit=False,
                                         new_transaction_id=new_transaction_id)

            activity_helper.end_activity()
        else:
            LOG.error(tr_ser.errors)
            raise exceptions.InvoicePaymentException('Unable to process refund', invoice_id=invoice_id)
    elif refund.status == 'failed':
        gateway.log_callback(external_id=external_id,
                             status=refund.status,
                             data=refund,
                             error=(refund.status == 'failed'),
                             error_info=refund.failure_reason)
        raise exceptions.GatewayException(_('Refund for transaction {} failed').format(external_id))
