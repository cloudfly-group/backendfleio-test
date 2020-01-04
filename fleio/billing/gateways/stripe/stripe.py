import copy
import logging
import json
import stripe
from rest_framework import status

from stripe.error import CardError, StripeError

from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render
from rest_framework.response import Response

from fleio.billing.gateways.stripe.apps import StripeConfig
from fleio.billing.gateways.utils import create_new_recurring_payments_ordering
from fleio.billing.models import Invoice
from fleio.billing.models import Transaction
from fleio.billing.models.transaction import TransactionStatus
from fleio.billing.gateways.decorators import gateway_action
from fleio.billing.gateways.decorators import staff_gateway_action
from fleio.billing.gateways import exceptions
from fleio.core.models import Client
from fleio.core.utils import fleio_join_url
from fleio.billing.gateways.stripe import utils
from fleio.billing.gateways.stripe.operations import process_charge, process_refund
from fleio.billing.gateways.stripe.forms import SetupRecurringPaymentsForm, SimpleInvoicePaymentForm, StripeRefundForm

from .conf import conf
from .models import RecurringPayments

LOG = logging.getLogger(__name__)

REFUNDABLE_TRANSACTION_STATUS = (TransactionStatus.SUCCESS,
                                 TransactionStatus.PREAUTH,
                                 TransactionStatus.PARTIAL_REFUNDED)


def get_refundable_transaction(transaction_id=None, external_id=None):
    """
    Retrieves a refundable transaction from database or raises.
    raises: exceptions.GatewayException
    """
    if transaction_id is None and external_id is None:
        raise exceptions.GatewayException('Transaction id is required')
    try:
        if transaction_id:
            transaction = Transaction.objects.get(id=transaction_id, gateway__name='stripe')
        else:
            transaction = Transaction.objects.get(external_id=external_id, gateway__name='stripe')
    except Transaction.DoesNotExist:
        raise exceptions.GatewayException('Transaction {} does not exist'.format(transaction_id))
    except Transaction.MultipleObjectsReturned:
        raise exceptions.GatewayException('Multiple transactions with id {}'.format(transaction_id))
    if transaction.status not in REFUNDABLE_TRANSACTION_STATUS:
        raise exceptions.GatewayException('Unable to refund transaction with status {}.'.format(transaction.status))
    return transaction


@gateway_action(methods=['GET'])
def pay_invoice(request):
    invoice_id = request.query_params.get('invoice')
    if invoice_id is None:
        raise exceptions.GatewayException("An 'invoice' parameter is required")
    try:
        inv = Invoice.objects.get(pk=invoice_id, client__in=request.user.clients.all())
    except Invoice.DoesNotExist:
        raise exceptions.GatewayException('Invoice {} does not exist'.format(invoice_id))
    if inv.balance <= 0:
        raise exceptions.InvoicePaymentException('Invoice {} is already paid'.format(invoice_id), invoice_id=invoice_id)

    amount = str(inv.balance)
    pay_message = _('Pay {} {} for invoice {}'.format(amount, inv.currency.pk, inv.pk))

    recurring = request.query_params.get('recurring', False)
    recurring = True if (recurring == 'True' or recurring == 'true' or recurring == '1') else False

    if recurring:
        existing_recurrent_payments_config = RecurringPayments.objects.filter(client=inv.client).first()
        if existing_recurrent_payments_config:
            raise exceptions.GatewayException(
                _('Recurrent payments were already configured for stripe.')
            )
        token_form = SetupRecurringPaymentsForm(initial={'invoice': inv.pk})
        stripe.api_key = conf.secret_key
        payment_intent = stripe.PaymentIntent.create(
            amount=utils.convert_amount_to_api(inv.balance, inv.currency.pk),
            currency=inv.currency.pk.lower(),
            setup_future_usage='off_session',
            metadata={"invoice": inv.pk},
        )
        return render(request=request,
                      template_name='stripe/setup_recurring.html',
                      context={'payment_vars': json.dumps({'publicKey': conf.public_key}),
                               'pay_message': pay_message,
                               'client_secret': payment_intent.client_secret,
                               'token_form': token_form})
    token_form = SimpleInvoicePaymentForm(initial={'invoice': inv.pk})
    return render(request=request,
                  template_name='stripe/pay_invoice.html',
                  context={'payment_vars': json.dumps({'publicKey': conf.public_key}),
                           'pay_message': pay_message,
                           'token_form': token_form})


@gateway_action(methods=['POST'])
def charge(request):
    """Endpoint for creating a charge based on a token"""
    token_form = SimpleInvoicePaymentForm(request.POST)
    if not token_form.is_valid():
        raise exceptions.GatewayException(token_form.errors)
    invoice_id = token_form.cleaned_data['invoice']
    charge_token = token_form.cleaned_data['token']
    try:
        inv = Invoice.objects.get(pk=invoice_id, client__in=request.user.clients.all())
    except Invoice.DoesNotExist:
        raise exceptions.InvoicePaymentException('Invoice {} does not exist'.format(invoice_id), invoice_id=invoice_id)
    if inv.balance <= 0:
        raise exceptions.InvoicePaymentException('Invoice {} is already paid'.format(invoice_id), invoice_id=invoice_id)
    stripe.api_key = conf.secret_key
    token_id = charge_token.get('id')
    if token_id is None:
        raise exceptions.InvoicePaymentException('Charge failed', invoice_id=invoice_id)
    try:
        charge_result = stripe.Charge.create(amount=utils.convert_amount_to_api(inv.balance, inv.currency.pk),
                                             currency=inv.currency.pk.lower(),
                                             description=_('Invoice {} payment').format(inv.pk),
                                             metadata={"invoice": inv.pk},
                                             source=token_id,
                                             idempotency_key=None)
    except CardError as e:
        LOG.exception(e)
        body = e.json_body
        err = body.get('error', {})
        raise exceptions.InvoicePaymentException(err.get('message', 'Charge failed'), invoice_id=invoice_id)
    except StripeError as e:
        LOG.exception(e)
        raise exceptions.InvoicePaymentException('Charge failed', invoice_id=invoice_id)
    process_charge(charge=charge_result)
    relative_url = 'billing/invoices/{}'.format(invoice_id)
    return HttpResponseRedirect(fleio_join_url(settings.FRONTEND_URL, relative_url))


@staff_gateway_action(methods=['GET', 'POST'],
                      transaction_statuses=REFUNDABLE_TRANSACTION_STATUS,
                      requires_redirect=True)
def refund(request):
    if request.method == 'GET':
        transaction_id = request.query_params.get('transaction')
        transaction = get_refundable_transaction(transaction_id=transaction_id)
        refund_form = StripeRefundForm(initial={'transaction_id': transaction.external_id})
        return render(request=request,
                      template_name='stripe/refund_prep.html',
                      context={'refund_form': refund_form})
    else:
        # TODO: use request.data for StripeRefundForm when we support partial refunds and choosing amount is possible
        refund_form_data = copy.deepcopy(request.data)
        transaction_id = refund_form_data['transaction_id']
        db_transaction = Transaction.objects.filter(external_id=transaction_id).first()  # type: Transaction
        refund_form_data['amount'] = db_transaction.amount
        refund_form = StripeRefundForm(refund_form_data)
        if refund_form.is_valid():
            stripe.api_key = conf.secret_key
            external_id = refund_form.cleaned_data['transaction_id']
            transaction = get_refundable_transaction(external_id=external_id)
            try:
                re = stripe.Refund.create(charge=external_id,
                                          amount=utils.convert_amount_to_api(amount=refund_form.cleaned_data['amount'],
                                                                             currency=transaction.currency_id),
                                          reason=refund_form.cleaned_data.get('reason', 'requested_by_user'))
            except stripe.error.InvalidRequestError as e:
                LOG.exception(e)
                raise exceptions.GatewayException(e)
            except StripeError as e:
                LOG.exception(e)
                raise exceptions.GatewayException(_('Refund failed'))
            process_refund(re)
            return HttpResponseRedirect(fleio_join_url(settings.FRONTEND_URL, 'staff/billing/journal'))
        else:
            return render(request=request,
                          template_name='stripe/refund_prep.html',
                          context={'refund_form': refund_form})


@gateway_action(methods=['POST'])
def setup_recurring(request):
    invoice_id = request.data.get('invoice', None)
    payment_intent = json.loads(request.data.get('payment_intent', "{}"))
    payment_method = payment_intent.get('payment_method', None)
    if not payment_method:
        raise exceptions.GatewayException(
            _('Cannot process request without enough details. Missing Stripe payment method id.')
        )
    if not invoice_id:
        raise exceptions.GatewayException(_('Missing invoice id.'))
    try:
        db_invoice = Invoice.objects.get(pk=invoice_id, client__in=request.user.clients.all())
    except Invoice.DoesNotExist:
        raise exceptions.GatewayException('Invoice {} does not exist'.format(invoice_id))
    stripe.api_key = conf.secret_key
    client = db_invoice.client  # type: Client
    existing_recurrent_payments_config = RecurringPayments.objects.filter(client=client).first()
    if not existing_recurrent_payments_config:
        try:
            stripe_customer = stripe.Customer.create(
                payment_method=payment_method,
                address=dict(
                    line1=client.address1 if client.address1 else None,
                    city=client.city if client.city else None,
                    country=client.country if client.country else None,
                    state=client.state if client.state else None,
                    postal_code=client.zip_code if client.zip_code else None,
                ),
                email=client.email,
                name=client.name,
                phone=client.phone,
            )
        except Exception as e:
            raise exceptions.GatewayException(_('Could not create customer in Stripe: {}').format(str(e)))
        try:
            recurrent_payments_config = RecurringPayments.objects.create(
                client=client,
                active=True,
                stripe_payment_method=payment_method,
                stripe_customer_id=stripe_customer.id,
            )
            create_new_recurring_payments_ordering(
                client=recurrent_payments_config.client, gateway_app_name=StripeConfig.name
            )
        except Exception as e:
            del e  # unused
    else:
        LOG.error('Client {} has already set up recurrent payments for stripe.'.format(client.id))

    relative_url = 'billing/invoices/{}'.format(invoice_id)
    return HttpResponseRedirect(fleio_join_url(settings.FRONTEND_URL, relative_url))


def recurring_payment(invoice_id):
    try:
        db_invoice = Invoice.objects.get(id=invoice_id)
    except Invoice.DoesNotExist:
        LOG.error('Could not create recurring payment as the invoice does not exist anymore.')
        return False
    amount = db_invoice.balance
    if not (amount > 0):
        LOG.debug('Cannot auto pay invoice that has 0 balance.')
        return False
    client = db_invoice.client  # type: Client
    recurrent_payments_config = RecurringPayments.objects.filter(client=client).first()  # type: RecurringPayments
    if not recurrent_payments_config:
        LOG.debug('This client has no recurrent payments configured for Stripe')
        return False
    secret_data = recurrent_payments_config.get_secret_data()
    stripe.api_key = conf.secret_key
    try:
        payment_intent = stripe.PaymentIntent.create(
            amount=utils.convert_amount_to_api(db_invoice.balance, db_invoice.currency.pk),
            currency=db_invoice.currency.pk.lower(),
            payment_method_types=['card'],
            customer=secret_data.get('stripe_customer_id'),
            payment_method=secret_data.get('stripe_payment_method'),
            metadata={'invoice': db_invoice.pk},
            off_session=True,
            confirm=True
        )
    except Exception as e:
        LOG.error('Error when trying to charge client automatically using stripe: {}'.format(str(e)))
        return False
    if payment_intent.status == 'succeeded':
        # invoice payment processing will be done via Stripe webhook
        return True
    LOG.debug('Auto payment for invoice {} using Stripe did not succeed'.format(db_invoice.id))
    return False


@gateway_action(methods=['POST'])
def callback(request):
    """
    The gateway callback method
    :type request: rest_framework.request.Request
    """
    stripe.api_key = conf.secret_key
    try:
        event = stripe.Webhook.construct_event(
            payload=request.body,
            sig_header=request.META.get('STRIPE_SIGNATURE', request.META.get('HTTP_STRIPE_SIGNATURE')),
            secret=conf.signing_secret
        )
    except Exception as e:
        LOG.error(e)
        raise exceptions.GatewayException('Invalid payload')

    event_dict = event.to_dict()
    if event_dict['type'] == "payment_intent.succeeded":
        intent = event_dict['data']['object']
        charges = intent.get('charges', {})
        charges_list = charges.get('data', [])
        charge_dict = charges_list[len(charges_list) - 1]  # use latest charge
        process_charge(charge_dict)
    elif event_dict['type'] == "payment_intent.payment_failed":
        pass

    return Response({'detail': 'OK'}, status=status.HTTP_200_OK)
