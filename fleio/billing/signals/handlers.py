import logging
from decimal import Decimal

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from fleio.billing.client_operations import ClientOperations
from fleio.billing.models import ClientCredit, Journal
from fleio.billing.models.journal_sources import JournalSources

from fleio.core.models import get_default_currency
from fleio.core.models import Client
from fleio.core.models import ClientStatus
from fleio.osbilling.price_calculator.monetary_amount import MonetaryAmount

LOG = logging.getLogger(__name__)


@receiver(post_save, sender=Client, dispatch_uid='billing_client_post_save_callback')
def client_post_save_callback(**kwargs):
    """Automatically create a ClientCredit account when a new Client is created"""
    client = kwargs.get('instance')  # type: Client
    client_created = kwargs.get('created', False)
    if client_created:
        # NOTE(tomo): Automatically create a ClientBilling record and PricingPlan if none defined
        ClientCredit.objects.create(client=client, currency=client.currency, amount=0)
        # Set the client as tax exempt if in EU and setting is True
        if (client.billing_settings.auto_eu_tax_exemption is True and client.country in settings.EU_COUNTRIES and
                client.vat_id):
            # WARNING(tomo): this needs to apply to client created only, otherwise an infinite cycle will occur
            client.tax_exempt = True
            client.save(update_fields=['tax_exempt'])


@receiver(post_save, sender=ClientCredit, dispatch_uid='billing_client_credit_post_save_callback')
def client_credit_post_save_callback(sender, instance: ClientCredit, **kwargs):
    # if a client credit is created or updated maybe credit is enough to resume client if it was suspended
    LOG.debug('Client credit post save callback invoked by {}'.format(sender))

    client = instance.client
    billing_settings = client.billing_settings

    created = kwargs.get('created', False)
    if created:
        if billing_settings.client_initial_credit > 0:
            default_currency = get_default_currency()
            monetary_amount = MonetaryAmount(
                value=Decimal(billing_settings.client_initial_credit),
                currency=default_currency,
            )
            destination_amount = monetary_amount.get_value_in_currency(currency=client.currency)
            client.add_credit(
                amount=destination_amount,
                currency=client.currency
            )
            Journal.objects.create(
                client_credit=instance,
                transaction=None,
                source_currency=default_currency,
                destination_currency=client.currency,
                source=JournalSources.staff,
                destination=JournalSources.credit,
                source_amount=billing_settings.client_initial_credit,
                destination_amount=destination_amount
            )

    if billing_settings.auto_resume_client_on_credit_update:
        client_operations = ClientOperations(client)
        client_operations.update_usage(skip_collecting=True)
        if client.status == ClientStatus.suspended:
            client_operations.evaluate_and_resume_if_enough_credit()
