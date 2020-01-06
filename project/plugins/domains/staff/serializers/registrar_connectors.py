from rest_framework import serializers

from plugins.domains.models import RegistrarConnector


class RegistrarConnectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistrarConnector
        fields = '__all__'


class RegistrarConnectorWithPricesSerializer(serializers.ModelSerializer):
    prices = serializers.SerializerMethodField()

    class Meta:
        model = RegistrarConnector
        fields = '__all__'

    def get_prices(self, obj):
        request = self.context.get('request')
        price_queryset = obj.registrar_prices.all()
        if request:
            tld_name = request.query_params.get('tld_name')
            currency = request.query_params.get('currency')
            if tld_name:
                price_queryset = price_queryset.filter(tld_name=tld_name)
            if currency:
                price_queryset = price_queryset.filter(currency=currency)
        return price_queryset.values('tld_name', 'register_price',
                                     'transfer_price', 'renew_price',
                                     'promo_price', 'currency',
                                     'years', 'updated_at')
