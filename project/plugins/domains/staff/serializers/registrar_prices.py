from rest_framework import serializers

from plugins.domains.models import RegistrarPrices


class RegistrarPricesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistrarPrices
        fields = '__all__'
