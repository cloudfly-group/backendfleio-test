from datetime import timedelta
import logging
from decimal import Decimal
from typing import List

from django.db import transaction as db_transaction
from django.db.models import QuerySet
from django.utils.timezone import now as utcnow
from django.utils.module_loading import import_string

from fleio.billing import utils
from fleio.billing.exceptions import PaymentException
from fleio.billing.gateways.utils import get_recurring_payment_method_path
from fleio.billing.invoice_utils import InvoiceUtils
from fleio.billing.invoicing.tasks import invoice_create, send_unpaid_invoice_notification
from fleio.billing.invoicing.tasks import invoice_add_payment
from fleio.billing.models import Invoice, OrderItemTypes, RecurringPaymentsOrder
from fleio.billing.models import Journal
from fleio.billing.models import Service
from fleio.billing.models import TaxRule
from fleio.billing.models.journal_sources import JournalSources
from fleio.billing.settings import BillingItemTypes
from fleio.billing.settings import CyclePeriods

from fleio.core.models import Client

LOG = logging.getLogger(__name__)


def get_client_attributes_for_invoice(client: Client):
    client_attributes = ('first_name', 'last_name', 'company', 'address1',
                         'address2', 'city', 'country', 'state', 'zip_code',
                         'phone', 'fax', 'email')
    invoice_client = {}
    for client_attr in client_attributes:
        invoice_client[client_attr] = getattr(client, client_attr, None)
    return invoice_client


class SettlementManager:
    @staticmethod
    def settle_zero_amount_invoice(invoice_id: int):
        invoice = Invoice.objects.get(id=invoice_id)  # type:Invoice
        if invoice.total == 0:
            invoice_add_payment(invoice.id, invoice.total, invoice.currency, from_credit_balance=True)
            return True
        elif invoice.total < 0:
            invoice_add_payment(invoice.id, invoice.total, invoice.currency, to_credit_balance=True)
            return True
        return False

    @staticmethod
    def process_order(order) -> Invoice:
        invoice_client = get_client_attributes_for_invoice(order.client)
        billing_settings = order.client.billing_settings
        with db_transaction.atomic():
            invoice = Invoice.objects.create(client=order.client,
                                             currency=order.currency,
                                             issue_date=utcnow(),
                                             due_date=utcnow(),
                                             **invoice_client)
            if billing_settings.invoicing_option == 'always_fiscal':
                invoice.make_fiscal()

            for item in order.items.all():
                # NOTE(tomo): update the service next due date to be able to show on invoice
                description = None
                if item.service:
                    if item.item_type == OrderItemTypes.service:
                        item.service.update_next_invoice_date()
                        if item.service.next_due_date and item.service.next_due_date != utils.DATETIME_MAX:
                            service_next_due = item.service.get_next_due_date(item.service.next_due_date)
                            if service_next_due and service_next_due != utils.DATETIME_MAX:
                                if item.service.cycle.cycle in [CyclePeriods.month, CyclePeriods.year]:
                                    service_next_due -= timedelta(days=1)
                                datetime_fmt = '%d/%m/%Y'
                                next_due_formatted = item.service.next_due_date.strftime(datetime_fmt)
                                description = '{} {} ({} - {})'.format(item.name,
                                                                       item.description,
                                                                       next_due_formatted,
                                                                       service_next_due.strftime(datetime_fmt))
                    elif item.item_type == OrderItemTypes.serviceUpgrade:
                        if item.service.next_due_date and item.service.next_due_date != utils.DATETIME_MAX:
                            service_next_due = item.service.get_next_due_date(item.service.next_due_date)
                            if service_next_due and service_next_due != utils.DATETIME_MAX:
                                description = '{} {}'.format(item.name, item.description)

                if description is None:
                    description = '{} {}'.format(item.name, item.description)
                invoice_item = invoice.items.create(item_type=item.item_type,
                                                    service=item.service,
                                                    product=item.product,
                                                    cycle=item.cycle,
                                                    amount=item.amount_without_taxes,
                                                    taxed=item.taxable,
                                                    description=description)

                for item_tax in item.taxes.all():
                    invoice_item.taxes.create(name=item_tax.name,
                                              amount=item_tax.amount,
                                              tax_rule=None)

                # NOTE(tomo): configurable option will be linked to invoice items here
                for config_option in item.configurable_options.all():
                    invoice_item.configurable_options.create(option=config_option.option,
                                                             option_value=config_option.option_value,
                                                             quantity=config_option.quantity,
                                                             has_price=config_option.has_price,
                                                             taxable=config_option.taxable,
                                                             unit_price=config_option.unit_price,
                                                             price=config_option.price,
                                                             setup_fee=config_option.setup_fee)

            invoice.update_totals()

            # Update the order invoice
            order.invoice = invoice
            order.save(update_fields=['invoice'])

            # Process zero amount invoice
            if not SettlementManager.settle_zero_amount_invoice(invoice.id):
                if billing_settings.send_notifications_for_unpaid_invoices:
                    send_unpaid_invoice_notification.delay(invoice_id=invoice.id)

            # TODO - #892: see if we should auto pay this invoice based on settings
            # TODO - #892: see how we should avoid invoicing here if not configured
            return invoice

    @staticmethod
    def auto_pay_invoice(recurring_payment_options: QuerySet, invoice_id: str) -> bool:
        # Method that will try to pay the remaining invoice balance if it's more than zero using one or more gateways
        # configured by client in his preferred order.
        charged_successfully = False
        for recurring_payment_option in recurring_payment_options.all().order_by('order'):
            if not charged_successfully:
                method_path = get_recurring_payment_method_path(gateway_name=recurring_payment_option.gateway_name)
                try:
                    recur_payment_method = import_string(method_path)
                except ImportError:
                    LOG.error('Could not get recurring payment method for {}'.format(
                        recurring_payment_option.gateway_name
                    ))
                else:
                    charged_successfully = recur_payment_method(invoice_id=invoice_id)
        return charged_successfully

    @staticmethod
    def process_services(
            client: Client,
            services: List[Service],
            tax_rules: List[TaxRule] = None) -> bool:
        LOG.info('Processing {} services for {}'.format(len(services), client))

        billing_settings = client.billing_settings

        if billing_settings.generate_invoices:
            invoice_id = SettlementManager.create_invoice_for_services(client=client,
                                                                       services=services,
                                                                       tax_rules=tax_rules)
            if billing_settings.auto_settle_usage:
                SettlementManager.settle_invoice_from_client_credit(invoice_id=invoice_id)
                recurring_payment_options = RecurringPaymentsOrder.objects.filter(client=client)
                if recurring_payment_options.count() > 0:
                    # the auto pay invoice will try to pay the remaining balance if it's more than zero
                    SettlementManager.auto_pay_invoice(
                        invoice_id=invoice_id,
                        recurring_payment_options=recurring_payment_options
                    )
            else:
                with db_transaction.atomic():
                    if not SettlementManager.settle_zero_amount_invoice(invoice_id):
                        if billing_settings.send_notifications_for_unpaid_invoices:
                            send_unpaid_invoice_notification.delay(invoice_id=invoice_id)

        else:
            with db_transaction.atomic():
                if billing_settings.auto_settle_usage:
                    SettlementManager.settle_services_usage_from_client_credit(
                        client=client,
                        services=services,
                        tax_rules=tax_rules
                    )
        with db_transaction.atomic():
            if billing_settings.generate_invoices or billing_settings.auto_settle_usage:
                # invoice or settlement was created for service
                if billing_settings.auto_settle_usage:
                    # update next invoice date if we only settle services
                    # if services are invoiced the next invoice date will be updated in invoice services function
                    current_date = utcnow()
                    for service in services:
                        while service.next_invoice_date is None or service.next_invoice_date < current_date:
                            service.update_next_invoice_date()

                return True

        return False

    @staticmethod
    def create_invoice_for_services(
            client: Client,
            services: List[Service],
            tax_rules: List[TaxRule] = None,
            manual_invoice: bool = False,
    ):
        LOG.info('Invoicing {} services for {}'.format(len(services), client))

        invoice_issue_date = utcnow()
        invoice_due_date = invoice_issue_date

        with db_transaction.atomic():  # create invoice and set the service next invoice due atomically
            invoice_items = list()
            for service in services:
                service_next_due = service.next_due_date if service.next_due_date else service.created_at
                while service.next_invoice_date is None or \
                        service.next_invoice_date < invoice_issue_date or manual_invoice:
                    item_taxes = []
                    service_fixed_price = service.get_fixed_price(currency=client.currency)
                    service_fixed_price = utils.cdecimal(service_fixed_price, q='0.01')  # Convert to 2 decimals

                    if service.is_price_overridden:
                        service_dynamic_price = Decimal(0)
                    else:
                        service_dynamic_price = InvoiceUtils.get_dynamic_price_for_service(
                            service,
                            service_next_due,
                        )
                    service_price = service_fixed_price + service_dynamic_price

                    # TODO: taxes are now recalculated on invoice creation in serializer, see if we need this code
                    # calculate taxes for invoice item
                    if service.product.taxable and not client.tax_exempt:
                        if tax_rules:
                            for tax_rule in tax_rules:
                                tax_amount = (service_price * tax_rule.rate) / 100
                                tax_amount = utils.cdecimal(tax_amount, q='.01')
                                item_taxes.append({'name': tax_rule.name,
                                                   'amount': tax_amount,
                                                   'tax_rule': tax_rule.id})

                    service_prev_due = service_next_due
                    service_next_due = service.get_next_due_date(service_next_due)

                    prev_invoice_date = service.next_invoice_date
                    service.update_next_invoice_date(
                        previous_due_date=service_prev_due,
                        manual_invoice=manual_invoice
                    )

                    if manual_invoice and service.next_invoice_date > invoice_issue_date:
                        invoice_due_date = prev_invoice_date if prev_invoice_date else service.next_invoice_date

                    if service_next_due and service_next_due != utils.DATETIME_MAX:
                        if manual_invoice:
                            # construct description to match invoice due date
                            while service_prev_due <= invoice_due_date:
                                service_prev_due = service_next_due
                                service_next_due = service.get_next_due_date(service_next_due)
                                if service_prev_due == service_next_due or service_next_due < invoice_due_date:
                                    # there is an issue within the loop, break to prevent infinite cycle
                                    break

                        service_next_due_display = service_next_due
                        service_prev_due_display = service_prev_due
                        if service.cycle.cycle in [CyclePeriods.month, CyclePeriods.year]:
                            service_next_due_display -= timedelta(days=1)
                        datetime_fmt = '%d/%m/%Y'

                        previous_due_formatted = service_prev_due_display.strftime(datetime_fmt)
                        next_due_formatted = service_next_due_display.strftime(datetime_fmt)

                        description = '{} ({} - {})'.format(
                            service.display_name, previous_due_formatted, next_due_formatted,
                        )
                    else:
                        description = service.display_name

                    invoice_items.append({'amount': service_price,
                                          'description': description,
                                          'item_type': BillingItemTypes.service,
                                          'taxed': service.product.taxable,
                                          'taxes': item_taxes,
                                          'service': service.id})

                    if prev_invoice_date == service.next_invoice_date:
                        # there is an issue within the loop, break to prevent infinite cycle
                        LOG.error('Invoice date not increasing, aborting')
                        break

                    if manual_invoice:
                        # this is a manual invoice generation, stopping
                        break

            invoice_id = invoice_create(
                client=client.id,
                items=invoice_items,
                issue_date=invoice_issue_date,
                currency=client.currency.code,
                due_date=invoice_due_date,
            )

        LOG.info('Invoice {} generated for client {}'.format(invoice_id, client))
        return invoice_id

    @staticmethod
    def settle_services_usage_from_client_credit(
            client: Client,
            services: List[Service],
            tax_rules: List[TaxRule] = None):
        LOG.info('Settling {} services for {}'.format(len(services), client))

        total_due = Decimal(0)
        current_date = utcnow()

        with db_transaction.atomic():  # create invoice and set the service next invoice due atomically
            for service in services:
                while service.next_due_date < current_date:
                    service_fixed_price = service.get_fixed_price(currency=client.currency)
                    service_fixed_price = utils.cdecimal(service_fixed_price, q='0.01')  # Convert to 2 decimals
                    service_dynamic_price = InvoiceUtils.get_dynamic_price_for_service(service, service.next_due_date)
                    service_price = service_fixed_price + service_dynamic_price
                    total_due += service_price

                    # calculate taxes for invoice item
                    if service.product.taxable and not client.tax_exempt:
                        if tax_rules:
                            for tax_rule in tax_rules:
                                tax_amount = (service_price * tax_rule.rate) / 100
                                tax_amount = utils.cdecimal(tax_amount, q='.01')
                                total_due += tax_amount

                    prev_due_date = service.next_due_date
                    InvoiceUtils.settle_dynamic_price_for_service(service, service.next_due_date)
                    service.update_next_due_date()
                    if prev_due_date == service.next_due_date:
                        LOG.error('Next due date is not increasing, aborting')
                        break

            if total_due > 0:
                # settle only if total due is above zero
                client.withdraw_credit(total_due, client.currency)
                client_credit_account = client.credits.get(client=client, currency=client.currency)
                Journal.objects.create(client_credit=client_credit_account,
                                       transaction=None,
                                       source_currency=client.currency,
                                       destination_currency=client.currency,
                                       source=JournalSources.credit,
                                       destination=JournalSources.settlement,
                                       source_amount=total_due,
                                       destination_amount=total_due)

    @staticmethod
    def settle_invoice_from_client_credit(invoice_id):
        LOG.info('Settling invoice {} from client credit'.format(invoice_id))
        invoice = Invoice.objects.get(id=invoice_id)  # type: Invoice
        try:
            invoice_add_payment(
                invoice_id=invoice.id,
                amount=invoice.total,
                currency_code=invoice.currency,
                from_credit_balance=True,
                is_auto_settlement=True,
            )
        except PaymentException as e:
            LOG.error('Failed to automatically pay invoice: {}'.format(e))

    @staticmethod
    def calculate_fixed_price_and_taxes(client: Client, price, taxable: bool):
        """Calculate total price with taxes and return the taxes applied"""
        taxes_applied = {}
        total_price = price

        if taxable:
            tax_rules = TaxRule.for_country_and_state(
                country=client.country_name,
                state=client.state
            ) or []
            for tax_rule in tax_rules:
                tax_amount = (price * tax_rule.rate) / 100
                tax_amount = utils.cdecimal(tax_amount, q='.01')
                if tax_rule.name in taxes_applied:
                    taxes_applied[tax_rule.name] += tax_amount
                else:
                    taxes_applied[tax_rule.name] = tax_amount
                total_price += tax_amount
        return total_price, taxes_applied
