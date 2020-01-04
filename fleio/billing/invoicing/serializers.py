import decimal

from django.db import transaction
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from fleio.billing import utils
from fleio.billing.models import Invoice, TaxRule
from fleio.billing.models import InvoiceItemConfigurableOption
from fleio.billing.models import InvoiceItem
from fleio.billing.models import InvoiceItemTax
from fleio.billing.models.invoice import InvoiceStatus
from fleio.billing.operations import get_invoice_payment_options
from fleio.billing.serializers import JournalDetailSerializer
from fleio.billing.settings import BillingItemTypes

from fleio.core.clients.serializers import ClientMinSerializer
from fleio.core.models import Client


class InvoiceItemBriefSerializer(serializers.ModelSerializer):
    total = serializers.ReadOnlyField()

    class Meta:
        model = InvoiceItem
        fields = ('amount', 'description')


class InvoiceItemTaxBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItemTax
        fields = ('name', 'amount', 'tax_rule')


class InvoiceItemConfigurableOptionsSerializer(serializers.ModelSerializer):
    display = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = InvoiceItemConfigurableOption
        fields = ('id', 'display', 'option_value', 'quantity', 'price', 'setup_fee', 'unit_price', 'is_free')


class InvoiceItemSerializer(serializers.ModelSerializer):
    taxes = InvoiceItemTaxBriefSerializer(many=True, required=False)
    configurable_options = InvoiceItemConfigurableOptionsSerializer(many=True, read_only=True)

    class Meta:
        model = InvoiceItem
        fields = ('amount', 'description', 'service', 'item_type', 'taxed', 'taxes', 'configurable_options')


class InvoiceDetailSerializer(serializers.ModelSerializer):
    client = ClientMinSerializer()
    items = InvoiceItemSerializer(many=True)
    journal = JournalDetailSerializer(many=True)
    fleio_info = serializers.ReadOnlyField(source='get_company_info')
    balance = serializers.DecimalField(read_only=True, max_digits=14, decimal_places=2)
    taxes = serializers.JSONField(read_only=True)
    payment_options = serializers.SerializerMethodField()

    class Meta:
        model = Invoice
        fields = ('id', 'status', 'issue_date', 'due_date', 'subtotal', 'total', 'currency', 'first_name', 'last_name',
                  'company', 'address1', 'city', 'country', 'state', 'zip_code', 'phone', 'fax', 'email', 'items',
                  'fleio_info', 'journal', 'balance', 'client', 'taxes', 'payment_options', 'display_number',
                  'is_fiscal', 'fiscal_date', 'fiscal_due_date', 'number', 'name')

    @staticmethod
    def get_payment_options(obj):
        return get_invoice_payment_options(invoice=obj)


class InvoiceBriefSerializer(serializers.ModelSerializer):
    """Serializer used for read operations."""
    client = ClientMinSerializer()

    class Meta:
        model = Invoice
        fields = ('id', 'status', 'client', 'issue_date', 'due_date', 'total', 'currency', 'display_number',
                  'is_fiscal', 'fiscal_date', 'fiscal_due_date', 'number', 'name')


# TODO: to discuss where functionality from this serializer should reside
class InvoiceSerializer(serializers.ModelSerializer):
    """Invoice serializer to be used by staff API."""
    total = serializers.DecimalField(read_only=True, decimal_places=2, max_digits=10)
    items = InvoiceItemSerializer(many=True)

    class Meta:
        model = Invoice
        fields = ('id', 'status', 'client', 'issue_date', 'due_date', 'total', 'currency', 'items', 'display_number')

    def to_internal_value(self, data):
        if isinstance(data, dict) and 'currency' not in data and 'client' in data:
            try:
                client = Client.objects.get(id=data['client'])
                self.fields['currency'].default = client.currency
            except Client.DoesNotExist:
                pass
        return super(InvoiceSerializer, self).to_internal_value(data)

    def validate(self, attrs):
        # FIXME(tomo): Take taxes into account
        if 'items' not in attrs or len(attrs['items']) == 0:
            raise serializers.ValidationError(_('Invoice must have at least one item'))

        total = decimal.Decimal('0.00')
        for item in attrs['items']:
            total += item['amount']
            if total > Invoice.MAX_TOTAL:
                raise serializers.ValidationError(_('Invoice total is bigger than maximum allowed'))

        return attrs

    @staticmethod
    def create_invoice_items(invoice, items, tax_rules):
        for item in items:
            # discard existing taxes, we will recreate them
            item.pop('taxes', [])
            invoice_item = invoice.items.create(**item)

            # calculate taxes if needed
            InvoiceSerializer.calculate_taxes(invoice_item, item, tax_rules)

            if item.get('item_type') == BillingItemTypes.service and item.get('service', None):
                # NOTE(tomo): Add configurable options to invoice item here
                for conf_opt in item.get('service').configurable_options.all():
                    invoice_item.configurable_options.create(option=conf_opt.option,
                                                             option_value=conf_opt.option_value,
                                                             quantity=conf_opt.quantity,
                                                             has_price=conf_opt.has_price,
                                                             taxable=conf_opt.taxable,
                                                             price=conf_opt.price,
                                                             unit_price=conf_opt.unit_price,
                                                             setup_fee=conf_opt.setup_fee)
        invoice.update_totals()

    @staticmethod
    def calculate_taxes(invoice_item, item, tax_rules):
        item_is_taxed = item.get('taxed')
        if item_is_taxed and tax_rules:
            item_amount = item.get('amount')
            for tax_rule in tax_rules:
                tax_amount = (item_amount * tax_rule.rate) / 100
                tax_amount = utils.cdecimal(tax_amount, q='.01')
                invoice_item.taxes.create(**{
                    'name': tax_rule.name,
                    'amount': tax_amount,
                    'tax_rule': tax_rule
                })

    def create(self, validated_data):
        items = validated_data.pop('items')
        client_attributes = ('first_name', 'last_name', 'company', 'address1',
                             'address2', 'city', 'country', 'state', 'zip_code',
                             'phone', 'fax', 'email')
        client = validated_data['client']
        for client_attr in client_attributes:
            if client_attr not in validated_data:
                validated_data[client_attr] = getattr(client, client_attr)

        tax_rules = None if client.tax_exempt else TaxRule.for_country_and_state(
            country=client.country_name,
            state=client.state
        )

        with transaction.atomic():
            invoice = super(InvoiceSerializer, self).create(validated_data)
            self.create_invoice_items(invoice, items, tax_rules)
        return invoice

    def update(self, invoice, validated_data):
        tax_rules = None if invoice.client.tax_exempt else TaxRule.for_country_and_state(
            country=invoice.client.country_name,
            state=invoice.client.state
        )

        items = validated_data.pop('items')
        with transaction.atomic():
            invoice.items.all().delete()
            self.create_invoice_items(invoice, items, tax_rules)

            if validated_data.get('status') == InvoiceStatus.ST_PAID != invoice.status:
                # Mark the invoice as PAID by also formatting the invoice number.
                # We can't just update the status alone.
                invoice.set_paid()
        return super(InvoiceSerializer, self).update(invoice, validated_data)
