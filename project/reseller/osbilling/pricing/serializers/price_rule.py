from django.db import transaction
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from fleio.osbilling.models import PricingRule
from fleio.osbilling.models import PricingRuleCondition
from fleio.osbilling.models import PricingRuleModifier
from reseller.osbilling.pricing.serializers.price_rule_condition import ResellerPriceRuleConditionSerializer
from reseller.osbilling.pricing.serializers.price_rule_modifier import ResellerPriceRuleModifierSerializer
from reseller.osbilling.pricing.serializers.pricing import ResellerPricingSerializer


class ResellerPriceRuleSerializer(serializers.ModelSerializer):
    conditions = ResellerPriceRuleConditionSerializer(many=True, required=False, allow_null=False)
    modifiers = ResellerPriceRuleModifierSerializer(many=True, required=False, allow_null=False)
    pricing = serializers.JSONField()

    class Meta:
        model = PricingRule
        fields = '__all__'

    def to_internal_value(self, data):
        if type(data) is dict and data.get('modifiers', None):
            # NOTE(tomo): Set any percent modifier time_unit from the main price rule.
            modifiers = data.get('modifiers', [])
            for modifier in modifiers:
                if type(modifier) is dict and modifier.get('price_is_percent', False):
                    price_rule_time_unit = data.get('pricing', {}).get('time_unit')
                    modifier['time_unit'] = data.get('time_unit', price_rule_time_unit)
        return super().to_internal_value(data)

    @staticmethod
    def validate_pricing(value):
        sv = ResellerPricingSerializer(data=value)
        sv.is_valid(raise_exception=True)
        seen = set()
        for pricing_def in sv.validated_data.get('prices'):
            if pricing_def.get('f') in seen:
                raise serializers.ValidationError(_('Multiple From values'))
            else:
                seen.add(pricing_def.get('f'))
        return sv.validated_data

    def validate(self, attrs):
        attrs = super().validate(attrs)
        conditions = attrs.get('conditions', None)
        modifiers = attrs.get('modifiers', None)
        if conditions and modifiers:
            attr_cond_set = set([c['attribute'] for c in conditions])
            attr_mod_set = set([m['attribute'] for m in modifiers])
            duplicates = attr_cond_set.intersection(attr_mod_set)
            if duplicates:
                dup_set = [d for d in duplicates]
                msg = _('Same attribute not allowed in modifiers and conditions: {}').format(*dup_set)
                raise serializers.ValidationError(msg)
        return attrs

    def update(self, instance, validated_data):
        conditions = validated_data.pop('conditions', list())
        modifiers = validated_data.pop('modifiers', list())
        with transaction.atomic():
            instance.conditions.all().delete()
            instance.modifiers.all().delete()
            for condition in conditions:
                PricingRuleCondition.objects.create(price_rule=instance, **condition)
            for modifier in modifiers:
                PricingRuleModifier.objects.create(price_rule=instance, **modifier)
            return super().update(instance, validated_data)

    def create(self, validated_data):
        conditions = validated_data.pop('conditions', list())
        modifiers = validated_data.pop('modifiers', list())
        with transaction.atomic():
            price_rule = super().create(validated_data)
            for condition in conditions:
                PricingRuleCondition.objects.create(price_rule=price_rule, **condition)
            for modifier in modifiers:
                PricingRuleModifier.objects.create(price_rule=price_rule, **modifier)

        return price_rule


class ResellerPriceRuleMinSerializer(serializers.ModelSerializer):
    resource_type = serializers.ReadOnlyField(source='resource.type')
    resource_name = serializers.ReadOnlyField(source='resource.display_name')
    price = serializers.SerializerMethodField()
    pricing_attribute = serializers.SerializerMethodField()
    display_unit = serializers.SerializerMethodField()
    modifiers_count = serializers.SerializerMethodField()
    tiered_price = serializers.SerializerMethodField()

    class Meta:
        model = PricingRule
        fields = ('id', 'display_name', 'resource_type', 'priority', 'resource_name', 'price', 'pricing_attribute',
                  'display_unit', 'modifiers_count', 'tiered_price')

    @staticmethod
    def get_modifiers_count(rule):
        return PricingRuleModifier.objects.filter(price_rule=rule).count()

    @staticmethod
    def get_display_unit(rule):
        return rule.get_display_unit()

    @staticmethod
    def get_pricing_attribute(rule):
        return rule.attribute

    @staticmethod
    def get_price(rule):
        return rule.price

    @staticmethod
    def get_tiered_price(rule):
        return rule.get_pricing_def()
