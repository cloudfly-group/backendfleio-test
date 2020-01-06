from rest_framework import serializers

from fleio.billing.models import TaxRule


class EndUserTaxRuleSerializer(serializers.ModelSerializer):
    rate = serializers.DecimalField(max_digits=5, decimal_places=2, coerce_to_string=False)

    class Meta:
        model = TaxRule
        fields = '__all__'
