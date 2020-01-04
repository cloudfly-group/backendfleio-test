from django.conf import settings
from rest_framework import serializers

from fleio.billing.models import Gateway


class StaffGatewayBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gateway
        fields = ('name', 'display_name')


class StaffGatewaySerializer(serializers.ModelSerializer):
    module_settings = serializers.JSONField(read_only=True)
    instructions = serializers.CharField(max_length=1024, allow_null=True, allow_blank=True)

    class Meta:
        model = Gateway
        fields = ('id', 'name', 'display_name', 'enabled', 'recurring_payments_enabled',
                  'visible_to_user', 'instructions', 'fixed_fee', 'percent_fee', 'module_settings')

        read_only_fields = ('id', 'name', 'module_settings')


class StaffRetrieveGatewaySerializer(StaffGatewaySerializer):
    instructions = serializers.SerializerMethodField()

    @staticmethod
    def get_instructions(gateway):
        if gateway.instructions is None or gateway.instructions == '':
            return getattr(settings, 'RECURRENT_PAYMENTS_TERMS_AND_CO_DEFAULT')
        return gateway.instructions
