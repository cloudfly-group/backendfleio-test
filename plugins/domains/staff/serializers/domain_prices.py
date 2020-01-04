from collections import OrderedDict

from rest_framework import serializers

from fleio.core.models import Currency
from fleio.core.serializers import CurrencySerializer

from plugins.domains.models import TLD
from plugins.domains.models.tld import PriceCycles
from plugins.domains.models.tld import PriceType

from .price_cycles import PriceCyclesSerializer


class DomainPricesSerializer(serializers.Serializer):
    default_currency = CurrencySerializer(read_only=True)
    price_types = serializers.DictField()
    price_cycles_list = PriceCyclesSerializer(many=True)
    price_cycles_by_currency = serializers.SerializerMethodField()
    price_cycles_by_type = serializers.SerializerMethodField()
    default_price_cycles = serializers.SerializerMethodField()

    @staticmethod
    def get_default_price_cycles(instance):
        default_price_cycles = {}
        for (index, price_cycles) in enumerate(instance.price_cycles_list):
            if price_cycles.currency.is_default:
                default_price_cycles[price_cycles.price_type] = index
        return default_price_cycles

    @staticmethod
    def get_price_cycles_by_currency(instance):
        price_cycles_by_currency = OrderedDict()
        for currency in Currency.objects.order_by('-is_default').all():
            price_cycles_by_currency[currency.code] = OrderedDict()
            price_cycles_by_currency[currency.code][PriceType.register] = None
            price_cycles_by_currency[currency.code][PriceType.transfer] = None
            price_cycles_by_currency[currency.code][PriceType.renew] = None

        for index, price_cycles in enumerate(instance.price_cycles_list):
            price_cycles_by_currency[price_cycles.currency.code][price_cycles.price_type] = index

        return price_cycles_by_currency

    @staticmethod
    def get_price_cycles_by_type(instance):
        price_cycles_by_type = OrderedDict()
        price_cycles_by_type[PriceType.register] = OrderedDict()
        price_cycles_by_type[PriceType.transfer] = OrderedDict()
        price_cycles_by_type[PriceType.renew] = OrderedDict()
        for currency in Currency.objects.order_by('-is_default').all():
            price_cycles_by_type[PriceType.register][currency.code] = None
            price_cycles_by_type[PriceType.transfer][currency.code] = None
            price_cycles_by_type[PriceType.renew][currency.code] = None

        for index, price_cycles in enumerate(instance.price_cycles_list):
            price_cycles_by_type[price_cycles.price_type][price_cycles.currency.code] = index

        return price_cycles_by_type

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    def save_prices(self, tld: TLD):
        price_cycles_list = self.validated_data['price_cycles_list']
        price_cycles_object_list = [PriceCycles(**price_cycles) for price_cycles in price_cycles_list]
        tld.save_prices(price_cycles_object_list)
