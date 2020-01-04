from rest_framework import serializers

from fleio.osbilling.models import ServiceDynamicUsageHistory
from fleio.osbilling.serializers import ClientMinSerializer


class ServiceDynamicUsageHistorySerializer(serializers.ModelSerializer):
    usage = serializers.JSONField()
    price = serializers.DecimalField(read_only=True, decimal_places=4, max_digits=16, coerce_to_string=False)
    updated_at = serializers.DateTimeField(read_only=True)
    previous_history = serializers.SerializerMethodField()
    next_history = serializers.SerializerMethodField()
    client = ClientMinSerializer(source='service_dynamic_usage.service.client')

    class Meta:
        model = ServiceDynamicUsageHistory
        fields = '__all__'

    @staticmethod
    def get_previous_history(obj):
        sd = obj.start_date
        prev = obj.service_dynamic_usage.billing_cycle_history.filter(start_date__lt=sd).order_by('-start_date').first()
        return prev.id if prev is not None else None

    @staticmethod
    def get_next_history(obj):
        sd = obj.start_date
        next_h = obj.service_dynamic_usage.billing_cycle_history.filter(
            start_date__gt=sd
        ).order_by('start_date').first()
        return next_h.id if next_h is not None else None
