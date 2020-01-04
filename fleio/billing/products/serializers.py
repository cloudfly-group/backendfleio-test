from rest_framework import serializers

from fleio.billing.models import Product
from fleio.billing.models import ProductCycle
from fleio.billing.models import ProductGroup
from fleio.billing.settings import PricingModel


class ProductGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductGroup
        fields = ('name', 'description')


class ProductCycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCycle
        fields = ('id', 'currency', 'cycle', 'cycle_multiplier', 'fixed_price', 'setup_fee', 'display_name')


class ProductCycleBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCycle
        fields = ('id', 'currency', 'cycle', 'cycle_multiplier', 'fixed_price', 'setup_fee', 'display_name')


class ProductSerializer(serializers.ModelSerializer):
    cycles = ProductCycleSerializer(many=True, read_only=True)
    is_free = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'code', 'name', 'description', 'cycles', 'is_free', 'requires_domain')
        read_only_fields = fields

    @staticmethod
    def get_is_free(obj):
        return obj.price_model == PricingModel.free


class ProductBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'description')
