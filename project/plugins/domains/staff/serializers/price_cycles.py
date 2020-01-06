from rest_framework import serializers

from fleio.core.serializers import CurrencySerializer

from plugins.domains.models.tld import PriceType


class PriceCyclesSerializer(serializers.Serializer):
    currency = CurrencySerializer(read_only=True)
    price_type = serializers.CharField()
    price_type_display = serializers.SerializerMethodField()
    prices_per_years = serializers.ListField()
    currency_code = serializers.CharField()
    relative_prices = serializers.BooleanField()

    @staticmethod
    def get_price_type_display(instance):
        return PriceType.price_type_map[instance.price_type]

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
