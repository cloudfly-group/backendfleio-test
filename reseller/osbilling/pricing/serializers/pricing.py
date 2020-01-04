from rest_framework import serializers

from fleio.osbilling.models import ATTRIBUTE_UNITS
from fleio.osbilling.models import TIME_UNITS


class ResellerPricingDefinitionSerializer(serializers.Serializer):
    f = serializers.DecimalField(max_digits=16, decimal_places=6)
    p = serializers.DecimalField(max_digits=16, decimal_places=6)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class ResellerPricingSerializer(serializers.Serializer):
    prices = ResellerPricingDefinitionSerializer(required=True, many=True)
    attribute = serializers.CharField(max_length=255, required=False, allow_null=True, allow_blank=True)
    attribute_unit = serializers.ChoiceField(choices=ATTRIBUTE_UNITS, required=False, allow_null=True, allow_blank=True)
    time_unit = serializers.ChoiceField(choices=TIME_UNITS, required=False, allow_null=True, allow_blank=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
