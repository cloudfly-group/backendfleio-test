from __future__ import unicode_literals

from rest_framework import serializers

from fleio.billing.models import TaxRule


class StaffTaxRuleSerializer(serializers.ModelSerializer):
    rate = serializers.DecimalField(max_digits=5, decimal_places=2, coerce_to_string=False)

    class Meta:
        model = TaxRule
        fields = '__all__'


class StaffTaxRuleCreateUpdateSerializer(serializers.ModelSerializer):
    rate = serializers.DecimalField(max_digits=5, decimal_places=2, coerce_to_string=False)
    state = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = TaxRule
        fields = '__all__'
