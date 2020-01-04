from rest_framework import serializers

from fleio.osbilling.models import BillingResource


class ResellerResourceSerializer(serializers.ModelSerializer):
    definition = serializers.JSONField()

    class Meta:
        model = BillingResource
        fields = '__all__'
