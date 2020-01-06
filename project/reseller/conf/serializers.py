from rest_framework import serializers
from fleio.billing.models import Product
from fleio.billing.models import ProductCycle


class ProductCycleSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCycle
        fields = ('id', 'display_name')


class ProductWithCyclesSettingsSerializer(serializers.ModelSerializer):
    cycles = ProductCycleSettingsSerializer(many=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'cycles')
