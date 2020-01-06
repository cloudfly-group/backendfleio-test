from rest_framework import serializers

from fleio.billing.models import CancellationRequest
from fleio.billing.models import ClientCredit
from fleio.billing.models import Invoice
from fleio.billing.models import Journal
from fleio.billing.models import Order
from fleio.billing.models import Transaction
from fleio.billing.models.journal_sources import JournalSources


class AddTransactionSerializer(serializers.ModelSerializer):
    extra = serializers.JSONField(allow_null=True)

    class Meta:
        model = Transaction
        fields = '__all__'


class AddCreditSerializer(serializers.Serializer):
    credit = serializers.DecimalField(
        max_digits=14, decimal_places=2,
        min_value=0.01, max_value=Invoice.MAX_TOTAL,
    )
    client = serializers.IntegerField()

    def update(self, instance, validated_data):
        super().update(instance, validated_data)

    def create(self, validated_data):
        super().create(validated_data)


class CancellationRequestBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = CancellationRequest
        fields = ('id', 'reason', 'cancellation_type')


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Order
        fields = ('client_notes', 'user')
        read_only_fields = ('id', 'order_date', 'total')

    def to_internal_value(self, data):
        data = super(OrderSerializer, self).to_internal_value(data)
        data['client'] = data['user'].clients.first()
        return data


class ClientCreditMinSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientCredit
        fields = ('client', 'currency', 'amount')
        read_only_fields = fields


class TransactionSerializer(serializers.ModelSerializer):
    gateway = serializers.CharField(source='gateway.name', read_only=True)  # Send only gw name to normal user
    gateway_display_name = serializers.CharField(source='gateway.display_name', read_only=True)

    class Meta:
        model = Transaction
        fields = ('id', 'gateway', 'gateway_display_name', 'external_id', 'date_initiated', 'status', 'amount',
                  'invoice', 'currency')


class JournalDetailSerializer(serializers.ModelSerializer):
    transaction = TransactionSerializer(read_only=True)
    source_name = serializers.SerializerMethodField()
    destination_name = serializers.SerializerMethodField()

    class Meta:
        model = Journal
        fields = ('transaction', 'date_added', 'destination', 'destination_amount', 'destination_currency',
                  'source', 'source_amount', 'source_currency', 'exchange_rate', 'is_refund', 'partial',
                  'source_name', 'destination_name')

    @staticmethod
    def get_source_name(journal):
        return JournalSources.sources_map[journal.source]

    @staticmethod
    def get_destination_name(journal):
        return JournalSources.sources_map[journal.destination]
