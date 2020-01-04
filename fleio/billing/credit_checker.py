import decimal

from fleio.billing.client_operations import ClientOperations
from fleio.core.models import Client


def check_if_enough_credit(client: Client, update_uptodate_credit: bool = False):
    if client.has_billing_agreement:
        required_credit = decimal.Decimal(client.billing_settings.credit_required_with_agreement)
    else:
        required_credit = decimal.Decimal(client.billing_settings.credit_required)

    if client.reseller_resources:
        reseller = client.reseller_resources.service.client
        if reseller.has_billing_agreement:
            required_credit = max(required_credit, decimal.Decimal(
                reseller.billing_settings.credit_required_with_agreement
            ))
        else:
            required_credit = max(required_credit, decimal.Decimal(
                reseller.billing_settings.credit_required
            ))

    if update_uptodate_credit:
        client_operations = ClientOperations(client=client)
        client_operations.update_usage()
        uptodate_credit = client_operations.uptodate_credit
    else:
        uptodate_credit = client.get_uptodate_credit()
    # TODO(tomo): Make sure the remaining_balance is converted to the default currency
    if uptodate_credit <= required_credit:
        return False

    return True
