from typing import Optional

import celery
import decimal

from django.conf import settings
from django.db import transaction
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from fleio.billing.exceptions import InvoiceException
from fleio.billing.exceptions import PaymentException
from fleio.billing.invoice_utils import InvoiceUtils
from fleio.billing.invoicing.serializers import InvoiceSerializer
from fleio.billing.models import ClientCredit
from fleio.billing.models import Invoice
from fleio.billing.models import Journal
from fleio.billing.models import Transaction
from fleio.billing.models.invoice import InvoiceStatus
from fleio.billing.models.journal_sources import JournalSources
from fleio.billing.models.transaction import TransactionStatus
from fleio.billing.services.tasks import create_service
from fleio.billing.services.tasks import change_cycle_service
from fleio.billing.services.tasks import resume_service
from fleio.billing.services.tasks import change_product_service
from fleio.billing.settings import BillingItemTypes, ServiceTask
from fleio.billing.settings import ProductAutoSetup
from fleio.billing.settings import ServiceStatus
from fleio.billing.settings import ServiceSuspendType

from fleio.celery import app

from fleio.core.models import AppUser
from fleio.core.models import Currency
from fleio.core.utils import fleio_join_url
from fleio.core.plugins.plugin_dispatcher import plugin_dispatcher

from fleio.notifications import notifier
from fleio.notifications.models import Notification
from fleio.notifications.notifier import send_staff_notification


@app.task(max_retries=settings.TASK_RETRIES, throws=(Invoice.DoesNotExist,), name='Process paid invoice',
          resource_type='Invoice')
def process_paid_invoice(invoice_id, **kwargs):
    """When an invoice is completely paid, we process all items"""
    with transaction.atomic():
        invoice = Invoice.objects.select_for_update().get(id=invoice_id)
        # TODO(tomo): Check if invoice.processed_at is not None and raise (meaning it was already processed) ?
        services_tasks = list()
        for item in invoice.items.prefetch_related('service',
                                                   'service__product').filter(item_type=BillingItemTypes.service,
                                                                              service__isnull=False):
            # Update the next due date on active services
            if item.service.status == ServiceStatus.active:
                item.service.update_next_due_date()
            # Run create on new services if enabled or just update the next due date
            elif item.service.status == ServiceStatus.pending:
                item.service.update_next_due_date()
                # FIXME(tomo): if the service remains in pending for 1 cycle, what happens with it if unpaid
                # or if paid after 2 cycles ?
                if (item.service.product.auto_setup == ProductAutoSetup.on_first_payment and
                        item.service.activated_at is None):
                    services_tasks.append(create_service.s(item.service.pk, user_id=kwargs.get('user_id')))
                elif (item.service.product.auto_setup == ProductAutoSetup.on_order and
                        item.service.activated_at is None):
                    # Create services for items that have auto setup on order
                    services_tasks.append(create_service.s(item.service.pk, user_id=kwargs.get('user_id')))
            # Resume suspended services
            elif (item.service.status == ServiceStatus.suspended and
                    item.service.suspend_type == ServiceSuspendType.overdue):
                # NOTE(tomo): Make sure the service does not have any other unpaid invoices before calling resume
                if Invoice.objects.for_service(service=item.service).unpaid().count() == 0:
                    item.service.update_next_due_date()
                    services_tasks.append(resume_service.s(item.service.id, user_id=kwargs.get('user_id')))
        # Process upgrade service items
        for item in invoice.items.prefetch_related('service',
                                                   'product',
                                                   'cycle').filter(item_type=BillingItemTypes.serviceUpgrade,
                                                                   service__isnull=False):
            item.service.task = ServiceTask.changeInProgress
            item.service.save(update_fields=['task'])
            configurable_options = item.configurable_options.values('option', 'option_value', 'quantity', 'has_price',
                                                                    'taxable', 'unit_price', 'price', 'setup_fee')

            if item.service.product == item.product:
                services_tasks.append(change_cycle_service.s(service_id=item.service.id,
                                                             cycle_id=item.cycle.pk,
                                                             configurable_options=configurable_options))
            else:
                services_tasks.append(change_product_service.s(service_id=item.service.id,
                                                               product_id=item.product.pk,
                                                               cycle_id=item.cycle.pk,
                                                               configurable_options=configurable_options))

        if len(services_tasks):
            transaction.on_commit(lambda: celery.group(services_tasks).apply_async())

        # Add to credit balance
        for item in invoice.items.filter(item_type=BillingItemTypes.credit):
            # NOTE(tomo): Process all items containing credit balance additions
            item_total = item.amount
            client_credit_account = invoice.client.credits.deposit(client=invoice.client,
                                                                   currency=invoice.currency,
                                                                   amount=item_total)
            invoice.journalentries.create(client_credit=client_credit_account,
                                          transaction=None,
                                          source=JournalSources.invoice,
                                          destination=JournalSources.credit,
                                          source_currency=invoice.currency,
                                          destination_currency=invoice.currency,
                                          destination_amount=item_total,
                                          source_amount=item_total,
                                          partial=False)
        invoice.processed_at = now()
        invoice.save()

        InvoiceUtils.settle_dynamic_price_for_invoice(invoice)

        if kwargs.get('create_todo', False):
            plugin_dispatcher.call_function(
                'todo',
                'create_todo',
                title=_('Invoice {} payment added').format(invoice.id),
                description=_('Invoice {} for client {} has been paid.').format(
                    invoice.id,
                    invoice.client.id,
                ),
            )


@app.task(
    bind=True,
    max_retries=settings.TASK_RETRIES,
    name='Send new invoice notification',
    resource_type='Invoice'
)
def send_unpaid_invoice_notification(self, invoice_id: int):
    del self  # unused
    invoice = Invoice.objects.get(id=invoice_id)
    relative_url = 'billing/invoices/{}'.format(invoice_id)
    if invoice.client.reseller_resources:
        frontend_url = invoice.client.reseller_resources.enduser_panel_url
    else:
        frontend_url = settings.FRONTEND_URL
    invoice_url = fleio_join_url(frontend_url, relative_url)
    variables = {
        'invoice_id': invoice.id,
        'amount': invoice.total,
        'currency': invoice.currency.code,
        'invoice_url': invoice_url,
        'display_number': invoice.display_number,
    }

    notifier.send(
        client=invoice.client,
        name='billing.invoice.new',
        priority=Notification.PRIORITY_NORMAL,
        variables=variables
    )


# TODO: this should not be a task
@app.task(max_retries=settings.TASK_RETRIES, throws=(InvoiceException,),
          name='Create invoice', resource_type='Billing Account')
def invoice_create(client, items, currency=None, issue_date=None, due_date=None, status=None):
    """
    Creates an invoice for a client.
    :param client: fleio.core.models.Client.id
    :param items: list of dict
                    dict: - amount
                          - description
                          - service
    :param currency: fleio.core.models.Currency
    :param issue_date: datetime.Datetime, the invoice issue date
    :param due_date: datetime.Datetime, the invoice due date
    :param status: str or unicode, a valid Invoice status
    """
    invoice_data = {'client': client,
                    'items': items}
    if currency:
        invoice_data['currency'] = currency
    if issue_date:
        invoice_data['issue_date'] = issue_date
    if due_date:
        invoice_data['due_date'] = due_date
    if status:
        invoice_data['status'] = status
    ser = InvoiceSerializer(data=invoice_data)
    if not ser.is_valid(raise_exception=False):
        raise InvoiceException(ser.errors)
    invoice = ser.save()
    if invoice.client.billing_settings.invoicing_option == 'always_fiscal':
        invoice.make_fiscal()

    return invoice.id


def invoice_add_negative_payment(invoice, amount, currency, user_id: Optional[int] = None):
    """Add a negative payment to an invoice, mainly add the amount to the client credit"""
    user = AppUser.objects.filter(id=user_id).first()
    with transaction.atomic():
        try:
            client_credit_account = invoice.client.credits.select_for_update().get(client=invoice.client,
                                                                                   currency=invoice.currency)
        except ClientCredit.DoesNotExist:
            raise PaymentException('Client {} does not have a {} credit account'.format(invoice.client.id,
                                                                                        invoice.currency.code))
        invoice_balance = invoice.balance
        invoice_credit = decimal.Decimal('0.0')
        if invoice_balance < 0.0 and invoice.is_unpaid():  # NOTE(tomo): Ignores expired/refunded invoices
            invoice_credit = amount if invoice_balance >= amount else invoice_balance

        if invoice_credit < 0:
            client_credit_account.deposit(-invoice_credit)
            invoice.journalentries.create(
                client_credit=client_credit_account,
                transaction=None,
                source=JournalSources.invoice,
                destination=JournalSources.credit,
                source_currency=currency,
                destination_currency=currency,
                destination_amount=-invoice_credit,
                source_amount=-invoice_credit,
                partial=False,
                user=user
            )


def invoice_add_payment_from_credit_balance(
        invoice: Invoice,
        amount,
        currency,
        user_id: Optional[int] = None,
        is_auto_settlement: bool = False,
):
    """Add invoice payment from credit balance"""
    user = AppUser.objects.filter(id=user_id).first()
    with transaction.atomic():
        try:
            client_credit_account = invoice.client.credits.select_for_update().get(client=invoice.client,
                                                                                   currency=invoice.currency)
        except ClientCredit.DoesNotExist:
            raise PaymentException('Client {} does not have a {} credit account'.format(invoice.client.id,
                                                                                        invoice.currency.code))

        invoice_balance = invoice.balance
        if invoice.client.billing_settings.add_tax_for_credit_invoices:
            # remove taxes still to be paid
            invoice_balance = invoice_balance - (invoice.taxes_total - invoice.already_paid_credit_tax)
        invoice_credit = decimal.Decimal('0.0')
        if invoice_balance > 0.0 and invoice.is_unpaid():  # NOTE(tomo): Ignores expired/refunded invoices
            invoice_credit = amount if invoice_balance >= amount else invoice_balance

        if invoice_credit > 0:
            if is_auto_settlement and invoice.client.billing_settings.auto_pay_invoice_only_when_enough_credit:
                # check if enough credit is left after payment
                credit_after_payment = invoice.client.uptodate_credit - invoice_credit
                if credit_after_payment < invoice.client.billing_settings.minim_uptodate_credit_for_invoice_payment:
                    raise PaymentException(
                        'Client {} insufficient funds in {} credit account'.format(
                            invoice.client.id,
                            invoice.currency.code,
                        ),
                    )

            client_credit_account.withdraw(invoice_credit)
            invoice.journalentries.create(
                client_credit=client_credit_account,
                transaction=None,
                source=JournalSources.credit,
                destination=JournalSources.invoice,
                source_currency=currency,
                destination_currency=currency,
                destination_amount=invoice_credit,
                source_amount=invoice_credit,
                partial=False,
                user=user
            )
            if invoice.client.billing_settings.add_tax_for_credit_invoices:
                # when add_tax_for_credit_invoices setting is active, add journal entries that invoice taxes were paid
                # from the credit tax
                if invoice_balance >= amount:
                    # partial payment. calculate the percent of this payment relative to the total amount
                    amount_paid_percent = (amount * 100 / 100) / (invoice.total - invoice.taxes_total)
                    taxes_to_pay = amount_paid_percent * invoice.taxes_total
                else:
                    taxes_to_pay = invoice.taxes_total - invoice.already_paid_credit_tax
                invoice.journalentries.create(
                    client_credit=client_credit_account,
                    transaction=None,
                    source=JournalSources.credit_tax,
                    destination=JournalSources.invoice,
                    source_currency=currency,
                    destination_currency=currency,
                    destination_amount=taxes_to_pay,
                    source_amount=taxes_to_pay,
                    partial=False,
                    user=user
                )


def invoice_add_payment_from_gateway(
        invoice, amount, currency, transaction_id, user_id: Optional[int] = None
):
    """
    Add invoice payment from a gateway transaction.
    This creates the transaction in our database and the specific journal entries.
    It also updates the client credit balance on over-payments usually.
    """
    invoice_balance = invoice.balance
    invoice_credit = decimal.Decimal('0.0')
    if invoice_balance > 0.0 and invoice.is_unpaid():  # NOTE(tomo): Payment goes to unpaid invoices only
        invoice_credit = amount if invoice_balance >= amount else invoice_balance
    # If this is an overpayment or invoice is paid, add the rest to the client's credit balance
    client_credit = amount - invoice_credit if amount > invoice_credit else decimal.Decimal('0.0')
    trans = Transaction.objects.get(pk=transaction_id)
    user = AppUser.objects.filter(id=user_id).first()

    with transaction.atomic():
        if invoice_credit > 0.0:
            invoice.journalentries.create(
                client_credit=None,
                transaction=trans,
                source_currency=currency,
                destination_currency=currency,
                source=JournalSources.transaction,
                destination=JournalSources.invoice,
                source_amount=invoice_credit,
                destination_amount=invoice_credit,
                partial=(client_credit > 0.0),
                user=user
            )
        if client_credit > 0.0:  # NOTE(tomo): overpayment, add to client credit
            client_credit_account = invoice.client.credits.deposit(client=invoice.client,
                                                                   currency=invoice.currency,
                                                                   amount=client_credit)
            invoice.journalentries.create(
                client_credit=client_credit_account,
                transaction=trans,
                source_currency=currency,
                destination_currency=currency,
                source=JournalSources.transaction,
                destination=JournalSources.credit,
                source_amount=client_credit,
                destination_amount=client_credit,
                partial=(invoice_credit > 0.0),
                user=user
            )


@app.task(max_retries=settings.TASK_RETRIES, throws=(Invoice.DoesNotExist, Currency.DoesNotExist, PaymentException),
          name='Add invoice payment', resource_type='Invoice')
def invoice_add_payment(
        invoice_id,
        amount,
        currency_code,
        transaction_id=None,
        from_credit_balance=False,
        to_credit_balance=False,
        user_id: Optional[int] = None,
        is_auto_settlement: bool = False,
        **kwargs
):
    """
    Add a payment to an existing Invoice by registering a transaction,
    updating the journal and the invoice total.

    :param invoice_id: int, invoice ID
    :param transaction_id: int, the transaction id
    :param amount: decimal.Decimal: the amount to add
    :param currency_code: str or unicode: an existing Currency code the payment is issued in
    :param from_credit_balance: bool, if the payment comes from Client credit balance or not
    :param to_credit_balance: bool, if the payment is negative and needs to go to Client credit balance
    :param user_id: int, the id of the user that effectuated the payment
    :param is_auto_settlement: bool, if the payment is an auto payment triggered by settlement manager
    """

    with transaction.atomic():
        invoice = Invoice.objects.select_for_update().get(id=invoice_id)  # NOTE(tomo): Lock invoice here
        currency = Currency.objects.get(code=currency_code)
        try:
            amount = decimal.Decimal(amount)
        except decimal.InvalidOperation as e:
            raise PaymentException('Invalid amount: {}'.format(e))
        if from_credit_balance:
            invoice_add_payment_from_credit_balance(
                invoice=invoice,
                amount=amount,
                currency=currency,
                user_id=user_id,
                is_auto_settlement=is_auto_settlement,
            )
        elif to_credit_balance and amount < 0:
            invoice_add_negative_payment(invoice=invoice, amount=amount, currency=currency,
                                         user_id=user_id)
        else:
            invoice_add_payment_from_gateway(
                invoice=invoice,
                transaction_id=transaction_id,
                amount=amount,
                currency=currency,
                user_id=user_id
            )

        # Check if invoice was paid and start processing the items
        if invoice.balance == 0 and invoice.is_unpaid():
            invoice.set_paid()
            transaction.on_commit(lambda: process_paid_invoice.delay(
                invoice.id,
                user_id=kwargs.get('user_id'),
                create_todo=kwargs.get('create_todo', False)
            ))

        journal_entry = invoice.journal.order_by('-date_added').first()

        send_staff_notification(
            name='staff.new_payment',
            variables={
                'frontend_url': getattr(settings, 'FRONTEND_URL', ''),
                'client_name': invoice.client.name,
                'client_id': invoice.client.id,
                'journal_id': journal_entry.id if journal_entry else ''
            }
        )

    return invoice.id


@app.task(max_retries=settings.TASK_RETRIES, name='Refund invoice payment', resource_type='Transaction')
def invoice_refund_payment(transaction_id, amount, to_client_credit=False, new_transaction_id=None):
    with transaction.atomic():
        existing_transaction = Transaction.objects.get(pk=transaction_id)
        new_transaction = None

        invoice = existing_transaction.invoice
        client = existing_transaction.invoice.client
        amount_decimal = decimal.Decimal(amount)

        if to_client_credit:
            # refund to credit credit, no transaction is needed
            destination = JournalSources.credit
        else:
            # refund to external entity, new transaction is needed
            new_transaction = Transaction.objects.get(pk=new_transaction_id)
            destination = JournalSources.transaction

        (client_credit, created) = client.credits.get_or_create(client=client,
                                                                currency=invoice.currency,
                                                                defaults={'amount': 0})

        # Get the initial destinations of the original transactions
        # If we have an overpayment, we have multiple journal entries. We need to reverse all of them
        existing_transaction_journals = Journal.objects.filter(transaction=existing_transaction)

        # create journal entry for refund - new_transaction will be used here
        # the entries for existing transactions will be modified
        for existing_tr_journal in existing_transaction_journals:
            if to_client_credit and existing_tr_journal.destination == JournalSources.credit:
                # NOTE(tomo): If we refund to client credit, we ignore journals for credit
                # this usually happens on overpayment (two transactions, on on invoice, on to credit)
                continue
            invoice.journalentries.create(client_credit=client_credit,
                                          transaction=new_transaction,
                                          source_currency=invoice.currency,
                                          destination_currency=invoice.currency,
                                          source_amount=existing_tr_journal.destination_amount,
                                          destination_amount=existing_tr_journal.source_amount,
                                          source=existing_tr_journal.destination,
                                          destination=destination)

        # set transaction status to refunded or partial refunded depending on amount
        existing_transaction.status = (TransactionStatus.REFUNDED if amount_decimal >= existing_transaction.amount
                                       else TransactionStatus.PARTIAL_REFUNDED)
        existing_transaction.save(update_fields=['status'])

        # set invoice status to refunded or unpaid depending on balance
        invoice.status = InvoiceStatus.ST_REFUNDED if invoice.balance == invoice.total else InvoiceStatus.ST_UNPAID
        invoice.save(update_fields=['status'])

        if to_client_credit:
            client_credit.deposit(amount=amount_decimal)

        if invoice.is_credit_invoice():
            client_credit.withdraw(amount=amount_decimal)
            invoice.journalentries.create(client_credit=client_credit,
                                          source_currency=invoice.currency,
                                          destination_currency=invoice.currency,
                                          source_amount=amount_decimal,
                                          destination_amount=amount_decimal,
                                          source=JournalSources.credit,
                                          destination=JournalSources.invoice)

        return invoice.id


@app.task(max_retries=settings.TASK_RETRIES, name='Invoice delete transaction', resource_type='Transaction')
def invoice_delete_transaction(transaction_id):
    with transaction.atomic():
        transaction_to_delete = Transaction.objects.get(pk=transaction_id)  # type: Transaction

        client = transaction_to_delete.invoice.client
        (client_credit, created) = client.credits.get_or_create(client=client,
                                                                currency=transaction_to_delete.currency,
                                                                defaults={'amount': 0})

        journal_entries = Journal.objects.filter(transaction=transaction_to_delete).all()

        for journal_entry in journal_entries:  # type: Journal
            if journal_entry.destination == JournalSources.credit:
                client_credit.withdraw(journal_entry.destination_amount)

            if journal_entry.destination == JournalSources.invoice:
                # TODO: see if we should do something here since invoice can change status
                pass

            journal_entry.delete()

        transaction_to_delete.delete()
