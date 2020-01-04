import decimal

from django.conf import settings
from django.db.models import ObjectDoesNotExist
from fleio.billing.models import Gateway


def get_invoice_payment_options(invoice):
    """Get all available payment options for an invoice"""
    # FIXME(tomo): Take into account the currencies supported by the payment gateways
    available_gateways = None
    credit_balance = None
    if invoice.is_unpaid():
        # NOTE(tomo): Allow only unpaid invoices to be paid
        client = invoice.client
        if not invoice.is_credit_invoice():
            try:
                credit_balance = client.credits.filter(amount__gt=0).values('currency', 'amount')
            except ObjectDoesNotExist:
                credit_balance = decimal.Decimal('0.00')
        available_gateways = Gateway.objects.visible_to_user().values(
            'id', 'name', 'display_name', 'recurring_payments_enabled', 'instructions'
        )
        recur_conditions = {}
        for gateway in available_gateways:
            instructions = gateway.get('instructions')
            if instructions is None or instructions == '':
                instructions = getattr(settings, 'RECURRENT_PAYMENTS_TERMS_AND_CO_DEFAULT')
            recur_conditions[gateway['name']] = instructions
        return {
            'gateways': available_gateways,
            'creditBalance': credit_balance,
            'recur_conditions': recur_conditions,
        }
    else:
        return {'gateways': available_gateways, 'creditBalance': credit_balance}
