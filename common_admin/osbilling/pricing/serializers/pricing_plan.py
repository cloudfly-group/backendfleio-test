from rest_framework import serializers

from fleio.core.serializers import CurrencySerializer
from fleio.osbilling.models import PricingPlan
from fleio.osbilling.models import ServiceDynamicUsage


class AdminPricingPlanMinSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricingPlan
        fields = ('id', 'name')


class AdminPricingPlanCreateOptionsSerializer(serializers.Serializer):
    currencies = CurrencySerializer(many=True, read_only=True)
    non_default_plans = AdminPricingPlanMinSerializer(many=True, read_only=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class AdminPricingPlanSerializer(serializers.ModelSerializer):
    pricing_rules = serializers.SerializerMethodField()
    services_count = serializers.SerializerMethodField()

    @staticmethod
    def get_services_count(data):
        return ServiceDynamicUsage.objects.filter(plan=data).distinct().count()
