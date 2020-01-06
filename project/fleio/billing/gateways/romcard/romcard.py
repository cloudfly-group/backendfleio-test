import logging
import requests
from datetime import datetime

from django.db import IntegrityError
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from fleio.billing.gateways.decorators import gateway_action
from fleio.billing.gateways.decorators import staff_gateway_action
from fleio.billing.gateways import exceptions
from fleio.billing.gateways.romcard.models import RecurringPayments
from fleio.billing.gateways.romcard.utils import get_client_by_invoice_id
from fleio.billing.gateways.utils import create_new_recurring_payments_ordering, get_gateway_name_from_app_name
from fleio.billing.models import Gateway, Transaction
from fleio.billing.models import Invoice
from fleio.billing.models.transaction import TransactionStatus
from fleio.billing.gateways.romcard.apps import RomcardConfig

from . import utils
from .conf import conf
from .operations import process_response
from .serializers import RomcardCallbackSerializer
from .forms import RomcardPayForm, RomcardSubscribeForm
from .forms import RomcardCaptureRefundForm

LOG = logging.getLogger(__name__)


def _remove_recurrent_payments_config(recurrent_payments_config):
    if recurrent_payments_config.first_payment is True:
        recurrent_payments_config.delete()


@gateway_action(methods=['GET'])
def pay_invoice(request):
    invoice_id = request.query_params.get('invoice')
    recurring = request.query_params.get('recurring', False)
    recurring = True if (recurring == 'True' or recurring == 'true' or recurring == '1') else False
    if invoice_id is None:
        raise exceptions.GatewayException("An 'invoice' parameter is required")
    try:
        inv = Invoice.objects.get(pk=invoice_id, client__in=request.user.clients.all())
    except Invoice.DoesNotExist:
        raise exceptions.GatewayException('Invoice {} does not exist'.format(invoice_id))
    if inv.balance <= 0:
        raise exceptions.GatewayException('Invoice {} is already paid'.format(invoice_id))
    trtype = str(utils.TransactionType.PRE_AUTHORIZATION)
    language_code = 'ro' if request.LANGUAGE_CODE == 'ro' else 'en'
    lang = language_code
    description = 'Invoice {}'.format(inv.pk)
    timestamp = utils.generate_timestamp()
    nonce = utils.generate_nonce()
    amount = str(inv.balance)
    api_invoice_id = utils.invoice_id_to_api(invoice_id)
    recur_exp = utils.generate_recur_timestamp(days=conf.recur_exp)
    romcard_gateway = Gateway.objects.filter(
        name=get_gateway_name_from_app_name(gateway_app_name=RomcardConfig.name)
    ).first()
    if not romcard_gateway:
        raise exceptions.GatewayException(_('Could not find the gateway.'))
    args = [conf.encryption_key,
            amount,
            inv.currency.pk,
            api_invoice_id,
            description,
            conf.merchant_name,
            conf.merchant_url,
            conf.merchant_no,
            conf.terminal,
            conf.email,
            trtype, '', '',
            timestamp,
            nonce,
            conf.callback_url]
    if romcard_gateway.recurring_payments_enabled and recurring:
        args.append(conf.recur_days)
        args.append(recur_exp)
    elif romcard_gateway.recurring_payments_enabled:
        args.append('')
        args.append('')
    p_sign = utils.calculate_p_sign(*args)
    fvars = {'AMOUNT': amount,
             'CURRENCY': inv.currency.pk,
             'ORDER': api_invoice_id,
             'DESC': description,
             'MERCH_NAME': conf.merchant_name,
             'MERCH_URL': conf.merchant_url,
             'MERCHANT': conf.merchant_no,
             'TERMINAL': conf.terminal,
             'EMAIL': conf.email,
             'TRTYPE': trtype,
             'COUNTRY': '',
             'MERCH_GMT': '',
             'TIMESTAMP': timestamp,
             'NONCE': nonce,
             'BACKREF': conf.callback_url}
    if romcard_gateway.recurring_payments_enabled:
        fvars['RECUR_FREQ'] = '' if not recurring else conf.recur_days
        fvars['RECUR_EXP'] = '' if not recurring else recur_exp
    fvars['P_SIGN'] = p_sign
    fvars['LANG'] = lang
    if recurring:
        client = get_client_by_invoice_id(invoice_id=invoice_id)
        try:
            RecurringPayments.objects.create(client=client)
        except IntegrityError:
            # already exists for this client
            pass
    else:
        recurrent_payments_config = RecurringPayments.objects.filter(client=inv.client).first()
        if recurrent_payments_config:
            _remove_recurrent_payments_config(recurrent_payments_config)

    if recurring or romcard_gateway.recurring_payments_enabled:
        romcard_form = RomcardSubscribeForm(fvars)
    else:
        romcard_form = RomcardPayForm(fvars)
    romcard_form_action = conf.url
    if romcard_form.is_valid():
        return render(request=request,
                      template_name='romcard/pay_invoice.html',
                      context={'redirect_message': _('Redirecting to RomCard'),
                               'page_title': _('Invoice payment'),
                               'form': romcard_form,
                               'form_action': romcard_form_action})
    else:
        LOG.error('Invalid romcard data: {}'.format(romcard_form.errors))
        raise exceptions.GatewayException('Invalid data provided')


@staff_gateway_action(methods=['GET'],
                      requires_redirect=True,
                      transaction_statuses=(Transaction.TRANSACTION_STATUS.PREAUTH,))
def capture(request):
    transaction_id = request.query_params.get('transaction')
    trans = Transaction.objects.get(id=transaction_id)
    invoice = trans.invoice
    api_invoice_id = utils.invoice_id_to_api(invoice.pk)
    amount = str(trans.amount)
    currency = trans.currency_id
    transaction_extra = trans.extra
    timestamp = utils.generate_timestamp()
    nonce = utils.generate_nonce()
    trtype = utils.TransactionType.SALES_COMPLETION

    p_sign = utils.calculate_p_sign(conf.encryption_key,
                                    api_invoice_id,
                                    amount,
                                    currency,
                                    trans.external_id,
                                    transaction_extra.get('INT_REF'),
                                    trtype,
                                    conf.terminal,
                                    timestamp,
                                    nonce,
                                    conf.callback_url)
    form_vars = {'ORDER': api_invoice_id,
                 'AMOUNT': amount,
                 'CURRENCY': currency,
                 'RRN': trans.external_id,
                 'INT_REF': transaction_extra.get('INT_REF'),
                 'TRTYPE': trtype,
                 'TERMINAL': conf.terminal,
                 'TIMESTAMP': timestamp,
                 'NONCE': nonce,
                 'BACKREF': conf.callback_url,
                 'P_SIGN': p_sign}

    romcard_form = RomcardCaptureRefundForm(form_vars)
    romcard_form_action = conf.url
    if romcard_form.is_valid():
        return render(request=request,
                      template_name='romcard/refund_or_capture.html',
                      context={'redirect_message': _('Redirecting to RomCard'),
                               'page_title': _('Capture payment'),
                               'form': romcard_form,
                               'form_action': romcard_form_action})
    else:
        LOG.error('Invalid romcard data: {}'.format(romcard_form.errors))
        raise exceptions.GatewayException('Invalid romcard data: {}'.format(romcard_form.errors))


def recurring_payment(invoice_id):
    client = get_client_by_invoice_id(invoice_id=invoice_id)
    try:
        invoice = Invoice.objects.get(id=invoice_id)
    except Invoice.DoesNotExist:
        LOG.error('Could not create recurring payment as the invoice does not exist anymore.')
        return False
    amount = invoice.balance
    if not (amount > 0):
        LOG.debug('Cannot auto pay invoice that has 0 balance.')
        return False
    trtype = utils.TransactionType.CREATE_RECURRING_TRANSACTION
    rrn_field_name = 'RECUR_REF'
    timestamp = utils.generate_timestamp()
    nonce = utils.generate_nonce()
    api_invoice_id = utils.invoice_id_to_api(invoice.pk)
    recurring_payments = RecurringPayments.objects.filter(client=client).first()  # type: RecurringPayments
    if not recurring_payments.active:
        return False
    p_sign = utils.calculate_p_sign(conf.encryption_key,
                                    api_invoice_id,
                                    amount,
                                    invoice.currency.code,
                                    recurring_payments.recur_ref,
                                    recurring_payments.int_ref,
                                    trtype,
                                    conf.terminal,
                                    timestamp,
                                    nonce,
                                    conf.callback_url)
    try:
        response = requests.post(url=conf.url, data={
            'ORDER': api_invoice_id,
            'AMOUNT': amount,
            'CURRENCY': invoice.currency.code,
            rrn_field_name: recurring_payments.recur_ref,
            'INT_REF': recurring_payments.int_ref,
            'TRTYPE': trtype,
            'TERMINAL': conf.terminal,
            'TIMESTAMP': timestamp,
            'NONCE': nonce,
            'BACKREF': conf.callback_url,
            'P_SIGN': p_sign
        })
    except Exception as e:
        LOG.exception(str(e))
        return False
    if response.status_code == 200 or response.status_code == 201:
        return True
    return False


@staff_gateway_action(methods=['GET'],
                      requires_redirect=True,
                      transaction_statuses=[Transaction.TRANSACTION_STATUS.PREAUTH,
                                            Transaction.TRANSACTION_STATUS.CONFIRMED,
                                            Transaction.TRANSACTION_STATUS.SUCCESS,
                                            Transaction.TRANSACTION_STATUS.PARTIAL_REFUNDED])
def refund(request):
    transaction_id = request.query_params.get('transaction')
    refund_amount = request.query_params.get('refund_amount')
    trans = Transaction.objects.get(id=transaction_id)
    transaction_amount = trans.amount
    transaction_extra = trans.extra
    api_invoice_id = utils.invoice_id_to_api(trans.invoice_id)
    currency = trans.currency_id
    timestamp = utils.generate_timestamp()
    nonce = utils.generate_nonce()
    assert refund_amount is None or refund_amount <= transaction_amount, ('Refund amount should be less than'
                                                                          ' the transaction amount.')
    is_recurring = transaction_extra.get('is_recurring', False)
    if is_recurring:
        # FIXME: fix refund to recurring transaction
        # recurring_data = RecurringPayments.objects.filter(client=trans.invoice.client).first()
        rrn = transaction_extra.get('RRN', '')
        int_ref = transaction_extra.get('INT_REF', '')
    else:
        rrn = transaction_extra.get('RRN', '')
        int_ref = transaction_extra.get('INT_REF', '')

    if refund_amount and refund_amount < transaction_amount:
        trtype = 25  # partial refund
    else:
        trtype = 24  # full refund
        refund_amount = transaction_amount
    refund_amount = str(refund_amount)
    p_sign = utils.calculate_p_sign(conf.encryption_key,
                                    api_invoice_id,
                                    refund_amount,
                                    currency,
                                    rrn,
                                    int_ref,
                                    trtype,
                                    conf.terminal,
                                    timestamp,
                                    nonce,
                                    conf.callback_url)
    form_vars = dict(ORDER=api_invoice_id,
                     AMOUNT=refund_amount,
                     CURRENCY=currency,
                     RRN=rrn,
                     INT_REF=int_ref,
                     TRTYPE=trtype,
                     TERMINAL=conf.terminal,
                     TIMESTAMP=timestamp,
                     NONCE=nonce,
                     BACKREF=conf.callback_url,
                     P_SIGN=p_sign)
    romcard_form = RomcardCaptureRefundForm(form_vars)
    romcard_form_action = conf.url
    if romcard_form.is_valid():
        return render(request=request,
                      template_name='romcard/refund_or_capture.html',
                      context={'redirect_message': _('Redirecting to RomCard'),
                               'page_title': _('Refund payment'),
                               'form': romcard_form,
                               'form_action': romcard_form_action})
    else:
        LOG.error('Invalid romcard data: {}'.format(romcard_form.errors))
        raise exceptions.GatewayException('Invalid romcard data: {}'.format(romcard_form.errors))


def _set_recurrent_payments_config_active(recurrent_payments_config, rrn, int_ref):
    # will set it as active and add ordering in a successful pre-auth response but only if
    # it wasn't activated in the past
    if recurrent_payments_config.first_payment is True:
        recurrent_payments_config.first_payment = False
        recurrent_payments_config.active = True
        recurrent_payments_config.recur_ref = rrn
        recurrent_payments_config.int_ref = int_ref
        recurrent_payments_config.save()
        create_new_recurring_payments_ordering(
            client=recurrent_payments_config.client, gateway_app_name=RomcardConfig.name
        )


@gateway_action(methods=['GET'])
def callback(request):
    """
    Example of valid request: ?TERMINAL=60000276&TRTYPE=0&ORDER=77696623&AMOUNT=100.00&CURRENCY=EUR&
    DESC=Invoice+77696623&ACTION=0&RC=00&MESSAGE=Approved&RRN=701949280263&INT_REF=7D7AD3F40163150F&
    APPROVAL=8F7F12&TIMESTAMP=20131217152033&NONCE=498ee8fc75b1e15595d87f297c50d6cc&
    P_SIGN=11250DDC1127C73D2A14424D1B88E41F2AC47528
    TRTYPE valid values:
        0 - pre-authorization (just blocking money on credit card)
        21 - sales completion (actually charging money)
        24 - reversal (refunding money on credit card)
        25 - partial refund
        171 - create automatic recurring transaction
    ACTION value values:
        0 - transaction approved
        1 - duplicate transaction
        2 - transaction rejected
        3 - processing error
    """
    ser = RomcardCallbackSerializer(data=request.query_params)
    if not ser.is_valid(raise_exception=False):
        LOG.debug('Gateway callback error: {} for requested parameters: {}'.format(ser.errors,
                                                                                   request.query_params))
        return process_response({'external_id': None,
                                 'transaction_status': 'Gateway sent invalid arguments',
                                 'data': {'errors': ser.errors, 'data': request.query_params},
                                 'error': True,
                                 'error_info': 'Gateway sent invalid arguments'})
    int_ref = ser.validated_data['INT_REF']
    invoice = ser.validated_data['ORDER']
    action = ser.validated_data['ACTION']
    trtype = ser.validated_data['TRTYPE']
    rrn = ser.validated_data['RRN']
    rc_code = ser.validated_data['RC']
    amount_decimal = ser.validated_data['AMOUNT']
    currency = ser.validated_data['CURRENCY']
    timestamp = ser.validated_data['TIMESTAMP']
    timestamp = datetime.strptime(timestamp, '%Y%m%d%H%M%S')
    client = get_client_by_invoice_id(invoice_id=invoice)
    recurring_payments_config = RecurringPayments.objects.filter(client=client).first()  # type: RecurringPayments

    if action == utils.RomcardAction.APPROVED and invoice:
        if trtype == utils.TransactionType.PRE_AUTHORIZATION:
            LOG.debug('Pre authorization success for {}'.format(int_ref))
            fleio_transaction_status = TransactionStatus.PREAUTH
            # Set the recurrent payments configuration as active if this pre-auth was right after first auto-pay
            # configuration request. If it was unsuccessful we delete the recurrent payments configuration so
            # we re-set it at a later time if requested
            if recurring_payments_config:
                _set_recurrent_payments_config_active(
                    recurrent_payments_config=recurring_payments_config,
                    rrn=rrn,
                    int_ref=int_ref
                )
        elif (trtype == utils.TransactionType.SALES_COMPLETION or
              trtype == utils.TransactionType.CREATE_RECURRING_TRANSACTION):
            LOG.debug('Sales complition (capture) success for {}'.format(int_ref))
            fleio_transaction_status = TransactionStatus.CONFIRMED
        elif trtype == utils.TransactionType.REFUND:
            LOG.debug('Refund success for {}'.format(int_ref))
            fleio_transaction_status = TransactionStatus.REFUNDED
        elif trtype == utils.TransactionType.PARTIAL_REFUND:
            LOG.debug('Partial refund success for {}'.format(int_ref))
            fleio_transaction_status = TransactionStatus.PARTIAL_REFUNDED
        else:
            LOG.warning('Unknown Romcard transaction status {}'.format(trtype))
            fleio_transaction_status = TransactionStatus.UNKNOWN

        is_recurring = True if trtype == utils.TransactionType.CREATE_RECURRING_TRANSACTION else False

        transaction_extra = {
            'RRN': ser.validated_data['RRN'],
            'NONCE': ser.validated_data['NONCE'],
            'INT_REF': ser.validated_data['INT_REF'],
            'is_recurring': is_recurring,
        }
        return process_response({
            'invoice': invoice,
            'amount': amount_decimal,
            'currency': currency,
            'external_id': rrn,
            'is_recurring': is_recurring,
            'transaction_date': timestamp,
            'transaction_extra': transaction_extra,
            'transaction_status': fleio_transaction_status,
            'log_data': request.query_params
        })

    else:
        # remove recurrent payments config if it's not active and wasn't activated ever and request failed
        if recurring_payments_config:
            _remove_recurrent_payments_config(recurrent_payments_config=recurring_payments_config)
        message = ser.validated_data.get('MESSAGE')
        LOG.error(msg='Transaction unsuccessfull: {}; {}'.format(action, message))
        return process_response({'invoice': invoice,
                                 'amount': amount_decimal,
                                 'currency': currency,
                                 'error': True,
                                 'error_code': rc_code,
                                 'error_info': message,
                                 'external_id': rrn,
                                 'transaction_date': timestamp,
                                 'transaction_extra': {
                                     'ACTION': action,
                                     'TRTYPE': trtype,
                                     'INT_REF': int_ref,
                                 },
                                 'transaction_status': message,
                                 'log_data': request.query_params})
