from django.db import transaction
from rest_framework import serializers

from fleio.billing.invoicing.tasks import invoice_add_payment
from fleio.billing.invoicing.serializers import InvoiceSerializer
from fleio.billing.models import Gateway
from fleio.billing.models import InvoiceItemConfigurableOption
from fleio.billing.models import Invoice
from fleio.billing.models import InvoiceItem
from fleio.billing.models import InvoiceItemTax
from fleio.billing.models.invoice import InvoiceStatus
from fleio.billing.models.transaction import TransactionStatus
from fleio.billing.serializers import AddTransactionSerializer


from fleiostaff.billing.journal.serializers import StaffJournalDetailsSerializer
from fleiostaff.billing.transactions.serializers import StaffTransactionSerializer

from fleio.core.clients.serializers import ClientMinSerializer
from fleio.core.models import Currency


class StaffInvoiceItemTaxBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItemTax
        fields = ('name', 'amount')


class StaffInvoiceItemConfigurableOptionsSerializer(serializers.ModelSerializer):
    display = serializers.CharField(max_length=255, read_only=True)
    is_free = serializers.BooleanField(read_only=True)

    class Meta:
        model = InvoiceItemConfigurableOption
        fields = ('id', 'display', 'option_value', 'quantity', 'price', 'setup_fee', 'unit_price', 'is_free')


class StaffInvoiceItemSerializer(serializers.ModelSerializer):
    taxes = StaffInvoiceItemTaxBriefSerializer(many=True, required=False)
    configurable_options = StaffInvoiceItemConfigurableOptionsSerializer(many=True, read_only=True)

    class Meta:
        model = InvoiceItem
        fields = ('amount', 'description', 'service', 'item_type', 'taxed', 'taxes', 'configurable_options')


class StaffInvoiceDetailSerializer(serializers.ModelSerializer):
    client = ClientMinSerializer()
    items = StaffInvoiceItemSerializer(many=True)
    journal = StaffJournalDetailsSerializer(many=True)
    fleio_info = serializers.ReadOnlyField(source='get_company_info')
    balance = serializers.DecimalField(read_only=True, max_digits=14, decimal_places=2)
    taxes = serializers.JSONField(read_only=True)
    transactions = StaffTransactionSerializer(many=True)
    statuses = serializers.SerializerMethodField()
    is_add_credit = serializers.SerializerMethodField()

    class Meta:
        model = Invoice
        fields = ('id', 'status', 'issue_date', 'due_date', 'subtotal', 'total', 'currency', 'first_name', 'last_name',
                  'company', 'address1', 'city', 'country', 'state', 'zip_code', 'phone', 'fax', 'email', 'items',
                  'fleio_info', 'journal', 'balance', 'client', 'taxes', 'transactions', 'statuses', 'display_number',
                  'is_add_credit', 'is_fiscal', 'fiscal_date', 'fiscal_due_date', 'name')
        read_only_fields = ('statuses', 'is_add_credit')

    @staticmethod
    def get_statuses(model):
        del model  # unused
        return InvoiceStatus.STATUSES_LIST

    @staticmethod
    def get_is_add_credit(model):
        return model.is_credit_invoice()


class StaffInvoiceBriefSerializer(serializers.ModelSerializer):
    """Serializer used for read operations."""
    client = ClientMinSerializer()

    class Meta:
        model = Invoice
        fields = ('id', 'status', 'client', 'issue_date', 'due_date', 'total', 'currency', 'display_number')


# NOTE: duplicate class here if changes are needed
class StaffInvoiceSerializer(InvoiceSerializer):
    pass


class StaffAddInvoicePaymentSerializer(serializers.Serializer):
    external_id = serializers.CharField(max_length=64, allow_null=True, allow_blank=True, required=False, default='')
    extra_info = serializers.CharField(max_length=256, allow_null=True, allow_blank=True, required=False, default='')
    invoice = serializers.PrimaryKeyRelatedField(queryset=Invoice.objects.all())
    date_initiated = serializers.DateTimeField()
    gateway = serializers.PrimaryKeyRelatedField(queryset=Gateway.objects.all())
    currency = serializers.SlugRelatedField(queryset=Currency.objects.all(), slug_field='code', allow_empty=True,
                                            allow_null=True, required=False)
    amount = serializers.DecimalField(max_digits=14, decimal_places=2, default=0)
    fee = serializers.DecimalField(max_digits=14, decimal_places=2, default=0)

    def to_internal_value(self, data):
        data = super(StaffAddInvoicePaymentSerializer, self).to_internal_value(data)
        if data.get('currency', None) is None:
            data['currency'] = data['invoice'].currency
        return data

    def create(self, validated_data):
        invoice = validated_data['invoice']
        user_id = self.context.get('request').user.pk if self.context.get('request') else None
        serializer_data = {'invoice': invoice.pk,
                           'external_id': validated_data['external_id'],
                           'amount': validated_data['amount'],
                           'currency': validated_data['currency'].code,
                           'gateway': validated_data['gateway'].id,
                           'fee': 0,
                           'date_initiated': validated_data['date_initiated'],
                           'extra': validated_data.get('extra_info', ''),
                           'status': TransactionStatus.SUCCESS}
        tr_ser = AddTransactionSerializer(data=serializer_data)
        tr_ser.is_valid(raise_exception=True)
        with transaction.atomic():
            new_transaction = tr_ser.save()
        transaction.on_commit(lambda: invoice_add_payment(
            invoice_id=invoice.id,
            amount=validated_data['amount'],
            currency_code=validated_data['currency'].code,
            transaction_id=new_transaction.pk,
            gateway_fee=validated_data['fee'],
            user_id=user_id
        ))
        return invoice
