import decimal
import logging
from lxml import objectify
from collections import OrderedDict

import requests

from django.conf import settings
from rest_framework.response import Response

from fleio.activitylog.utils.activity_helper import activity_helper
from fleio.billing.gateways.decorators import gateway_action, staff_gateway_action
from fleio.billing.gateways import exceptions as gateway_exceptions
from fleio.billing.gateways import exceptions
from fleio.billing.gateways.payuro.apps import PayURoConfig
from fleio.billing.gateways.payuro.error_code_meaning import CAPTURE_ERROR_CODE_MEANINGS, REFUND_ERROR_CODE_MEANINGS
from fleio.billing.gateways.utils import create_new_recurring_payments_ordering
from fleio.billing.models.transaction import Transaction, TransactionStatus
from fleio.billing.gateways.payuro.models import RecurringPayments

from fleio.billing.invoicing.tasks import invoice_add_payment, invoice_refund_payment

from django.utils.timezone import now as utcnow
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render

from fleio.billing.models import Gateway, Invoice
from fleio.billing.serializers import AddTransactionSerializer
from fleio.core.models import Client
from fleio.core.utils import fleio_join_url
from .conf import conf
from .utils import PayURoUtils

LOG = logging.getLogger(__name__)


CREATE_ORDER_URL = conf.url + 'order/lu.php'
CAPTURE_ORDER_URL = conf.url + 'order/idn.php'
REFUND_ORDER_URL = conf.url + 'order/irn.php'
PAY_ON_TIME_URL = conf.url + 'order/alu/v3'


class PayUROOrderStatus:
    preauth = 'PAYMENT_AUTHORIZED'

    to_fleio_transaction_status = {
        preauth: TransactionStatus.PREAUTH,
    }


@gateway_action(methods=['GET'])
def pay_invoice(request):
    invoice_id = request.query_params.get('invoice')
    recurring = request.query_params.get('recurring', False)
    recurring = True if (recurring == 'True' or recurring == 'true' or recurring == '1') else False
    if invoice_id is None:
        raise exceptions.GatewayException(_('Missing invoice parameter.'))
    try:
        db_invoice = Invoice.objects.get(pk=invoice_id, client__in=request.user.clients.all())  # type: Invoice
    except Invoice.DoesNotExist:
        raise exceptions.GatewayException(_('Invoice {} does not exist').format(invoice_id))
    if db_invoice.balance <= 0:
        raise exceptions.GatewayException(_('Invoice {} is already paid').format(invoice_id))
    client = db_invoice.client  # type: Client
    now = utcnow()
    # params
    order_ref = '{}'.format(db_invoice.id)
    order_date = now.strftime('%Y-%m-%d %H-%M-%S')
    multi_items = True if db_invoice.items.count() > 1 else False
    order_pname = ['{}'.format(item.item_type) for item in db_invoice.items.all()]
    if multi_items:
        order_pcode = []
        counter = 1
        for item in db_invoice.items.all():
            order_pcode.append('{}{}'.format(item.item_type, str(counter)))
            counter = counter + 1
    else:
        order_pcode = ['{}'.format(item.item_type) for item in db_invoice.items.all()]
    order_pinfo = ['{}'.format(item.item_type) for item in db_invoice.items.all()]
    order_price = [str(item.amount) for item in db_invoice.items.all()]
    order_price_type = ['GROSS' for x in db_invoice.items.all()]
    order_qty = ['1' for x in db_invoice.items.all()]
    order_vat = ['0' for x in db_invoice.items.all()]
    pay_method = 'CCVISAMC'
    order_shipping = ''
    discount = '0'
    client_phone = client.phone if client.phone else '-'
    client_country = client.country.upper() if client.country else ''
    language = request.user.language.upper() if request.user.language else 'RO'
    testorder = conf.testorder
    back_ref = fleio_join_url(settings.FRONTEND_URL, 'billing/invoices')

    order_hash = PayURoUtils.calculate_signature(params=[
        conf.merchant, order_ref, order_date, order_pname, order_pcode, order_pinfo, order_price, order_qty,
        order_vat, order_shipping, db_invoice.currency.code, discount, pay_method, order_price_type, testorder
    ])

    return render(
        request=request,
        template_name='payuro/pay_invoice.html',
        context={
            'redirect_message': _('Redirecting to PayU'),
            'page_title': _('Invoice payment'),
            'form_action': CREATE_ORDER_URL,
            # inputs
            'MERCHANT': conf.merchant,
            'ORDER_REF': order_ref,
            'ORDER_DATE': order_date,
            'MULTI_ITEMS': multi_items,
            'ORDER_PNAME': order_pname if len(order_pname) > 1 else order_pname[0],
            'ORDER_PCODE': order_pcode if len(order_pcode) > 1 else order_pcode[0],
            'ORDER_PINFO': order_pinfo if len(order_pinfo) > 1 else order_pinfo[0],
            'ORDER_PRICE': order_price if len(order_price) > 1 else order_price[0],
            'ORDER_PRICE_TYPE': order_price_type if len(order_price_type) > 1 else order_price_type[0],
            'ORDER_QTY': order_qty if len(order_qty) > 1 else order_qty[0],
            'ORDER_VAT': order_vat if len(order_vat) > 1 else order_vat[0],
            'PRICES_CURRENCY': db_invoice.currency.code,
            'PAY_METHOD': pay_method,
            'ORDER_SHIPPING': order_shipping,
            'TESTORDER': testorder,
            'DISCOUNT': discount,
            'BILL_FNAME': client.first_name,
            'BILL_LNAME': client.last_name,
            'BILL_EMAIL': client.email,
            'BILL_PHONE': client_phone,
            'BILL_COUNTRYCODE': client_country,
            'LANGUAGE': language,
            'BACK_REF': back_ref,
            'ORDER_HASH': str(order_hash, encoding='utf-8'),
            'RECURRING': True if recurring else False,
        }
    )


@staff_gateway_action(
    methods=['GET'], requires_redirect=True, transaction_statuses=(TransactionStatus.PREAUTH,)
)
def capture(request):
    transaction_id = request.query_params.get('transaction')
    transaction = Transaction.objects.get(id=transaction_id)
    now = utcnow()
    data = {
        'MERCHANT': conf.merchant,
        'ORDER_REF': transaction.external_id,
        'ORDER_AMOUNT': str(transaction.amount),
        'ORDER_CURRENCY': transaction.currency.code,
        'IDN_DATE': now.strftime('%Y-%m-%d %H:%M:%S'),

    }
    # TODO: from python 3.6 use **data instead of getting each value as keys are ordered in the dict
    order_hash = PayURoUtils.calculate_signature([
        data.get('MERCHANT'), data.get('ORDER_REF'), data.get('ORDER_AMOUNT'), data.get('ORDER_CURRENCY'),
        data.get('IDN_DATE')
    ])
    data['ORDER_HASH'] = order_hash
    response = requests.post(
        url=CAPTURE_ORDER_URL,
        data=data
    )
    if response.status_code == 200 or response.status_code == 201:
        response_text = response.text
        response_text = response_text.replace('<EPAYMENT>', '')
        response_params = response_text.split('|')
        order_ref = response_params[0]
        response_code = response_params[1]
        if response_code == '1':
            existing_transaction = Transaction.objects.filter(external_id=order_ref).first()
            if existing_transaction:
                existing_transaction.status = TransactionStatus.CONFIRMED
                existing_transaction.save(update_fields=['status'])
            else:
                raise gateway_exceptions.GatewayException(
                    _('Could not find existing transaction to mark as captured in db.')
                )
        else:
            raise gateway_exceptions.GatewayException(
                _('Could not perform capture action. Details: {}').format(
                    CAPTURE_ERROR_CODE_MEANINGS.get(response_code)
                )
            )
    else:
        raise gateway_exceptions.GatewayException(_('Error when making request to capture transaction.'))
    return Response({'detail': _('Ok')})


@staff_gateway_action(
    methods=['GET'], requires_redirect=True,
    transaction_statuses=(Transaction.TRANSACTION_STATUS.CONFIRMED, Transaction.TRANSACTION_STATUS.PREAUTH)
)
def refund(request):
    gateway = Gateway.objects.get(name='payuro')
    transaction_id = request.query_params.get('transaction')
    transaction = Transaction.objects.get(id=transaction_id)
    invoice = transaction.invoice
    now = utcnow()
    data = {
        'MERCHANT': conf.merchant,
        'ORDER_REF': transaction.external_id,
        'ORDER_AMOUNT': str(transaction.amount),
        'ORDER_CURRENCY': transaction.currency.code,
        'IRN_DATE': now.strftime('%Y-%m-%d %H:%M:%S'),
        'AMOUNT': str(transaction.amount),

    }
    # TODO: from python 3.6 use **data instead of getting each value as keys are ordered in the dict
    order_hash = PayURoUtils.calculate_signature([
        data.get('MERCHANT'), data.get('ORDER_REF'), data.get('ORDER_AMOUNT'), data.get('ORDER_CURRENCY'),
        data.get('IRN_DATE'), data.get('AMOUNT')
    ])
    data['ORDER_HASH'] = order_hash
    response = requests.post(
        url=REFUND_ORDER_URL,
        data=data
    )
    if response.status_code == 200 or response.status_code == 201:
        response_text = response.text
        response_text = response_text.replace('<EPAYMENT>', '')
        response_params = response_text.split('|')
        order_ref = response_params[0]
        response_code = response_params[1]
        if response_code == '1':
            existing_transaction = Transaction.objects.filter(external_id=order_ref).first()
            if existing_transaction:
                new_refund_transaction = {
                    'invoice': invoice.id,
                    'external_id': transaction.external_id,
                    'amount': str(transaction.amount),
                    'currency': transaction.currency.code,
                    'gateway': gateway.pk,
                    'fee': gateway.get_fee(amount=decimal.Decimal(transaction.amount)),
                    'date_initiated': now,
                    'extra': {},
                    'refunded_transaction': transaction.pk,
                    'status': TransactionStatus.REFUNDED
                }
                transaction_serializer = AddTransactionSerializer(data=new_refund_transaction)
                if transaction_serializer.is_valid(raise_exception=False):
                    new_transaction = transaction_serializer.save()
                    activity_helper.start_generic_activity(
                        category_name='payuro', activity_class='payuro payment refund',
                        invoice_id=invoice.id
                    )

                    invoice_refund_payment.delay(transaction_id=transaction_id,
                                                 amount=transaction.amount,
                                                 to_client_credit=False,
                                                 new_transaction_id=new_transaction.pk)

                    activity_helper.end_activity()
                else:
                    LOG.error(_('PayU Ro transaction error: {}').format(transaction_serializer.errors))
                    raise gateway_exceptions.GatewayException(
                        _('Transaction error {}').format(transaction_serializer.errors)
                    )

            else:
                raise gateway_exceptions.GatewayException(
                    _('Could not find existing transaction to mark as captured in db.')
                )
        else:
            raise gateway_exceptions.GatewayException(
                _('Could not perform capture action. Details: {}').format(REFUND_ERROR_CODE_MEANINGS.get(response_code))
            )
    else:
        raise gateway_exceptions.GatewayException(_('Error when making request to capture transaction.'))
    return Response({'detail': _('Ok')})


@gateway_action(methods=['GET', 'POST'])
def callback(request):
    request_body = request.body
    if not PayURoUtils.verify_hash(request_body):
        raise gateway_exceptions.GatewayException(_('Did not receive or received invalid signature.'))
    gateway = Gateway.objects.get(name='payuro')
    invoice_id = request.data.get('REFNOEXT', None)
    if not invoice_id:
        raise gateway_exceptions.GatewayException(_('Missing fleio invoice id.'))
    external_id = request.data.get('REFNO')
    total_amount = request.data.get('IPN_TOTALGENERAL', None)
    currency = request.data.get('CURRENCY')
    status = request.data.get('ORDERSTATUS')
    invoice = Invoice.objects.get(id=invoice_id)
    if 'TOKEN_HASH' in request.data:
        try:
            recurrent_payments_config = RecurringPayments.objects.create(
                client=invoice.client,
                active=True,
                token_hash=request.data['TOKEN_HASH'],
                ipn_cc_mask=request.data['IPN_CC_MASK'],
                ipn_cc_exp_date=request.data['IPN_CC_EXP_DATE'],
            )
            create_new_recurring_payments_ordering(
                client=recurrent_payments_config.client, gateway_app_name=PayURoConfig.name
            )
        except Exception as e:
            del e  # unused
            pass
    if status == PayUROOrderStatus.preauth:
        transaction_status = PayUROOrderStatus.to_fleio_transaction_status[PayUROOrderStatus.preauth]
        serializer_data = {
            'invoice': invoice_id,
            'external_id': external_id,
            'amount': total_amount,
            'currency': currency,
            'gateway': gateway.pk,
            'fee': gateway.get_fee(amount=decimal.Decimal(total_amount)),
            'date_initiated': request.data.get('SALEDATE'),
            'extra': {},
            'status': transaction_status
        }
        add_transaction_serializer = AddTransactionSerializer(data=serializer_data)
        if add_transaction_serializer.is_valid(raise_exception=False):
            db_transaction = add_transaction_serializer.save()
            activity_helper.start_generic_activity(
                category_name='payuro', activity_class='payuro payment',
                invoice_id=invoice_id
            )
            invoice_add_payment.delay(
                invoice_id=invoice_id,
                amount=total_amount,
                currency_code=currency,
                transaction_id=db_transaction.id
            )
            activity_helper.end_activity()

        else:
            LOG.error(_('PayU Ro transaction error: {}').format(add_transaction_serializer.errors))
            raise gateway_exceptions.GatewayException('Add transaction error')

    ipn_response = PayURoUtils.build_ipn_response(params=request_body)
    return Response({'detail': ipn_response})


def etree_to_dict(element):
    return {
        'REFNO': str(element.REFNO),
        'RETURN_CODE': str(element.RETURN_CODE),
        'STATUS': str(element.STATUS)
    }


def recurring_payment(invoice_id):
    try:
        db_invoice = Invoice.objects.get(id=invoice_id)  # type: Invoice
    except Invoice.DoesNotExist:
        LOG.error('Could not create recurring payment as the invoice does not exist anymore.')
        return False
    client = db_invoice.client
    amount = db_invoice.balance
    if not (amount > 0):
        LOG.debug('Cannot auto pay invoice that has 0 balance.')
        return False

    try:
        # params
        order_ref = '{}'.format(db_invoice.id)
        multi_items = True if db_invoice.items.count() > 1 else False
        order_pname = ['{}'.format(item.item_type) for item in db_invoice.items.all()]
        if multi_items:
            order_pcode = []
            counter = 1
            for item in db_invoice.items.all():
                order_pcode.append('{}{}'.format(item.item_type, str(counter)))
                counter = counter + 1
        else:
            order_pcode = ['{}'.format(item.item_type) for item in db_invoice.items.all()]
        order_pinfo = ['{}'.format(item.item_type) for item in db_invoice.items.all()]
        order_price = [str(item.amount) for item in db_invoice.items.all()]
        order_price_type = ['GROSS' for x in db_invoice.items.all()]
        order_qty = ['1' for x in db_invoice.items.all()]
        order_vat = ['0' for x in db_invoice.items.all()]
        pay_method = 'CCVISAMC'
        order_shipping = ''
        discount = '0'
        client_phone = client.phone if client.phone else '-'
        client_country = client.country.upper() if client.country else ''
        testorder = conf.testorder
        back_ref = fleio_join_url(settings.FRONTEND_URL, 'billing/invoices')

        recurrent_payments_config = RecurringPayments.objects.filter(
            client=client,
            active=True,
        ).first()  # type: RecurringPayments
        if not recurrent_payments_config:
            LOG.error(
                'Cannot automatically pay invoice {} as client has no recurrent payment options active.'.format(
                    db_invoice.id
                )
            )
            return False
        secret_data = recurrent_payments_config.get_secret_data()
        now = utcnow()
        order_date = now.strftime('%Y-%m-%d %H:%M:%S')
        data = {
            'MERCHANT': conf.merchant,
            'ORDER_REF': order_ref,
            'ORDER_DATE': order_date,
            'ORDER_PNAME[]': order_pname if len(order_pname) > 1 else order_pname[0],
            'ORDER_PCODE[]': order_pcode if len(order_pcode) > 1 else order_pcode[0],
            'ORDER_PINFO[]': order_pinfo if len(order_pinfo) > 1 else order_pinfo[0],
            'ORDER_PRICE[]': order_price if len(order_price) > 1 else order_price[0],
            'ORDER_PRICE_TYPE[]': order_price_type if len(order_price_type) > 1 else order_price_type[0],
            'ORDER_QTY[]': order_qty if len(order_qty) > 1 else order_qty[0],
            'ORDER_VAT[]': order_vat if len(order_vat) > 1 else order_vat[0],
            'PRICES_CURRENCY': db_invoice.currency.code,
            'PAY_METHOD': pay_method,
            'ORDER_SHIPPING': order_shipping,
            'TESTORDER': testorder,
            'DISCOUNT': discount,
            'BILL_FNAME': client.first_name,
            'BILL_LNAME': client.last_name,
            'BILL_EMAIL': client.email,
            'BILL_PHONE': client_phone,
            'BILL_COUNTRYCODE': client_country,
            'BACK_REF': back_ref,
            'CC_CVV': '',
            'CC_TOKEN': secret_data.get('token_hash'),
            'LU_TOKEN_TYPE': 'PAY_ON_TIME',
        }
        ordered_data = OrderedDict(sorted(data.items()))
        hash_params = []
        for key, value in ordered_data.items():
            hash_params.append(value)
        order_hash = PayURoUtils.calculate_signature(params=hash_params)
        ordered_data['ORDER_HASH'] = str(order_hash, encoding='utf-8'),
        response = requests.post(url=PAY_ON_TIME_URL, data=ordered_data)
        response_dict = etree_to_dict(objectify.fromstring(response.content))
        if response_dict.get('STATUS') == 'SUCCESS' and response_dict.get('RETURN_CODE') == 'AUTHORIZED':
            return True  # notification will be received
        else:
            LOG.error('Could not make automatic payment for invoice {}. Details: {}'.format(
                db_invoice.id, response_dict.get('RETURN_CODE')
            ))
    except Exception as e:
        LOG.exception(str(e))
        return False
    if response.status_code == 200 or response.status_code == 201:
        return True
    return False
