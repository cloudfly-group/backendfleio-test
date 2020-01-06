from rest_framework import serializers

from django.utils.translation import ugettext_lazy as _

from fleio.core.models import Client
from fleio.osbilling.models import ServiceDynamicUsage, ServiceDynamicUsageHistory
from fleio.osbilling.utils import cdecimal, INTER_PRICE_DISPLAY_PREC, INTER_PRICE_ROUNDING


class ServiceDynamicUsageSerializer(serializers.ModelSerializer):
    usage = serializers.JSONField()
    service_display = serializers.SerializerMethodField()
    price = serializers.DecimalField(read_only=True, decimal_places=4, max_digits=12, coerce_to_string=False)
    updated_at = serializers.DateTimeField(read_only=True)
    billing_start = serializers.DateTimeField(source='first_anniversary_date', read_only=True)
    billing_end = serializers.DateTimeField(source='last_anniversary_date', read_only=True)
    previous_history = serializers.SerializerMethodField()

    class Meta:
        model = ServiceDynamicUsage
        exclude = ('service', 'plan', )

    @staticmethod
    def get_service_display(obj):
        try:
            if obj.service.openstack_project:
                if obj.service.display_name:
                    return '{} - {}'.format(obj.service.display_name, obj.service.openstack_project.project_id)
                else:
                    return _('Service {} - {}').format(obj.service.id, obj.service.openstack_project.project_id)
        except Exception as e:
            del e  # unused
            return obj.service.display_name or obj.service.id
        return obj.service.display_name or obj.service.id

    @staticmethod
    def get_previous_history(obj):
        prev = obj.get_previous_history()
        if prev:
            return prev.id
        else:
            return None

    def to_representation(self, instance):
        data = super().to_representation(instance=instance)
        usage = data.get('usage', None)
        if usage:
            usages_details = usage.get('usage_details', [])
            for usage_details in usages_details:
                resources_usage = usage_details.get('usage', [])
                for resource_usage in resources_usage:
                    usage_history = resource_usage.get('history', [])
                    for rule in usage_history:
                        if 'base_price' in rule:
                            rule['base_price'] = str(cdecimal(
                                rule['base_price'], q=INTER_PRICE_DISPLAY_PREC, rounding=INTER_PRICE_ROUNDING
                            ))
                        modifiers = rule.get('modifiers', [])
                        for modifier in modifiers:
                            modifier['price'] = str(cdecimal(
                                modifier['price'], q=INTER_PRICE_DISPLAY_PREC, rounding=INTER_PRICE_ROUNDING
                            ))

        return data


class BillingUsageSummary(serializers.BaseSerializer):
    def to_representation(self, instance):
        usage_summary = {
            'project': instance.get('project', ''),
            'currency': instance.get('currency', ''),
            'price': instance.get('price', 0.00)
        }
        return usage_summary


class ClientMinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id', 'name', 'external_billing_id')


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


class ServiceDynamicUsageHistoryListSerializer(ServiceDynamicUsageHistorySerializer):
    usage = BillingUsageSummary()
