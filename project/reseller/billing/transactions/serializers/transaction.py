from rest_framework import serializers

from fleio.billing.gateways.utils import get_transaction_actions
from fleio.billing.models import Transaction

from fleiostaff.billing.gateways.serializers import StaffGatewayBriefSerializer
from fleiostaff.billing.gateways.serializers import StaffGatewaySerializer


class ResellerTransactionBriefSerializer(serializers.ModelSerializer):
    available_actions = serializers.SerializerMethodField()
    gateway = StaffGatewayBriefSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = ('id', 'status', 'external_id', 'gateway', 'available_actions')

    @staticmethod
    def get_available_actions(transaction):
        actions = get_transaction_actions(transaction)
        return actions


class ResellerTransactionSerializer(serializers.ModelSerializer):
    extra = serializers.JSONField()
    gateway = StaffGatewaySerializer()
    actions = serializers.SerializerMethodField()
    is_refundable = serializers.BooleanField(read_only=True)

    class Meta:
        model = Transaction
        fields = '__all__'

    @staticmethod
    def get_actions(transaction):
        return get_transaction_actions(transaction)
