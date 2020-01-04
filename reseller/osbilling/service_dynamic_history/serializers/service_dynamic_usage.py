from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from fleio.core.serializers import CurrencySerializer
from fleio.osbilling.models import ServiceDynamicUsage
from fleio.osbilling.utils import INTER_PRICE_DISPLAY_PREC
from fleio.osbilling.utils import INTER_PRICE_ROUNDING
from fleio.osbilling.utils import cdecimal


class ServiceDynamicUsageSerializer(serializers.ModelSerializer):
    usage = serializers.JSONField()
    service_display = serializers.SerializerMethodField()
    price = serializers.DecimalField(read_only=True, decimal_places=4, max_digits=12, coerce_to_string=False)
    updated_at = serializers.DateTimeField(read_only=True)
    billing_start = serializers.DateTimeField(source='first_anniversary_date', read_only=True)
    billing_end = serializers.DateTimeField(source='last_anniversary_date', read_only=True)
    previous_history = serializers.SerializerMethodField()
    client_currency = serializers.SerializerMethodField()
    client_display = serializers.SerializerMethodField()

    class Meta:
        model = ServiceDynamicUsage
        exclude = ('plan', )

    @staticmethod
    def get_client_currency(obj):
        return CurrencySerializer().to_representation(instance=obj.active_service.client.currency)

    @staticmethod
    def get_service_display(obj):
        if obj.active_service.openstack_project:
            if obj.active_service.display_name:
                return '{} - {}'.format(
                    obj.active_service.display_name,
                    obj.active_service.openstack_project.project_id,
                )
            else:
                return _('Service {} - {}').format(
                    obj.active_service.id,
                    obj.active_service.openstack_project.project_id
                )
        return obj.active_service.display_name or obj.active_service.id

    @staticmethod
    def get_client_display(obj):
        return '{}({})'.format(
            obj.active_service.client.name,
            obj.active_service.client.id,
        )

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
