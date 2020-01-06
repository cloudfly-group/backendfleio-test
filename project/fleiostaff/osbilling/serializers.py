from django.db import transaction
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from common_admin.osbilling.pricing.serializers.pricing_plan import AdminPricingPlanSerializer
from fleio.core.features import staff_active_features
from fleio.core.models import Currency
from fleio.osbilling.models import ATTRIBUTE_UNITS
from fleio.osbilling.models import BillingResource
from fleio.osbilling.models import PricingPlan
from fleio.osbilling.models import PricingRule
from fleio.osbilling.models import PricingRuleCondition
from fleio.osbilling.models import PricingRuleModifier
from fleio.osbilling.models import TIME_UNITS
from fleiostaff.core.clients.serializers import StaffClientBriefSerializer


class ResourceSerializer(serializers.ModelSerializer):
    definition = serializers.JSONField()

    class Meta:
        model = BillingResource
        fields = '__all__'


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'


class PricingPlanDeleteSerializer(serializers.Serializer):
    plan_to_migrate = serializers.PrimaryKeyRelatedField(queryset=PricingPlan.objects.all())

    def __init__(self, plan, *args, **kwargs):
        self.plan = plan
        super(PricingPlanDeleteSerializer, self).__init__(*args, **kwargs)

    def validate_plan_to_migrate(self, data):
        if data.id == self.plan.id:
            raise serializers.ValidationError(_('Can\'t migrate to selected plan'))
        return data


class PriceRuleConditionSerializer(serializers.ModelSerializer):
    value = serializers.JSONField()

    class Meta:
        model = PricingRuleCondition
        exclude = ('price_rule',)

    def validate(self, attrs):
        # FIXME(tomo): Get pricerule_pk in some other way
        price_rule_id = self.context['view'].kwargs.get('pricerule_pk', None)
        if price_rule_id:
            for modifier in PricingRule.objects.get(id=price_rule_id).modifiers.all():
                if modifier.attribute == attrs['attribute']:
                    msg = _('Attribute {} already present in modifiers').format(attrs['attribute'])
                    raise serializers.ValidationError({'attribute': msg})
        return attrs


class PriceRuleModifierSerializer(serializers.ModelSerializer):
    value = serializers.JSONField()
    price = serializers.DecimalField(coerce_to_string=False, max_digits=12, decimal_places=4)

    class Meta:
        model = PricingRuleModifier
        exclude = ('price_rule',)

    def validate(self, attrs):
        attrs = super(PriceRuleModifierSerializer, self).validate(attrs)
        # FIXME(tomo): Get pricerule_pk in some other way
        price_rule_id = self.context['view'].kwargs.get('pricerule_pk', None)
        if price_rule_id:
            for condition in PricingRule.objects.get(id=price_rule_id).conditions.all():
                if condition.attribute == attrs['attribute']:
                    msg = _('Attribute {} already present in conditions').format(attrs['attribute'])
                    raise serializers.ValidationError({'attribute': msg})
        return attrs


class PricingDefinitionSerializer(serializers.Serializer):
    f = serializers.DecimalField(max_digits=16, decimal_places=6)
    p = serializers.DecimalField(max_digits=16, decimal_places=6)


class PricingSerializer(serializers.Serializer):
    prices = PricingDefinitionSerializer(required=True, many=True)
    attribute = serializers.CharField(max_length=255, required=False, allow_null=True, allow_blank=True)
    attribute_unit = serializers.ChoiceField(choices=ATTRIBUTE_UNITS, required=False, allow_null=True, allow_blank=True)
    time_unit = serializers.ChoiceField(choices=TIME_UNITS, required=False, allow_null=True, allow_blank=True)


class PriceRuleSerializer(serializers.ModelSerializer):
    conditions = PriceRuleConditionSerializer(many=True, required=False, allow_null=False)
    modifiers = PriceRuleModifierSerializer(many=True, required=False, allow_null=False)
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
        return super(PriceRuleSerializer, self).to_internal_value(data)

    @staticmethod
    def validate_pricing(value):
        sv = PricingSerializer(data=value)
        sv.is_valid(raise_exception=True)
        seen = set()
        for pricing_def in sv.validated_data.get('prices'):
            if pricing_def.get('f') in seen:
                raise serializers.ValidationError(_('Multiple From values'))
            else:
                seen.add(pricing_def.get('f'))
        return sv.validated_data

    def validate(self, attrs):
        attrs = super(PriceRuleSerializer, self).validate(attrs)
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
            return super(PriceRuleSerializer, self).update(instance, validated_data)

    def create(self, validated_data):
        conditions = validated_data.pop('conditions', list())
        modifiers = validated_data.pop('modifiers', list())
        with transaction.atomic():
            price_rule = super(PriceRuleSerializer, self).create(validated_data)
            for condition in conditions:
                PricingRuleCondition.objects.create(price_rule=price_rule, **condition)
            for modifier in modifiers:
                PricingRuleModifier.objects.create(price_rule=price_rule, **modifier)

        return price_rule


class PriceRuleMinSerializer(serializers.ModelSerializer):
    resource_type = serializers.ReadOnlyField(source='resource.type')
    resource_name = serializers.ReadOnlyField(source='resource.display_name')
    price = serializers.SerializerMethodField()
    pricing_attribute = serializers.SerializerMethodField()
    display_unit = serializers.SerializerMethodField()
    modifiers_count = serializers.SerializerMethodField()
    tiered_price = serializers.SerializerMethodField()

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

    class Meta:
        model = PricingRule
        fields = ('id', 'display_name', 'resource_type', 'priority', 'resource_name', 'price', 'pricing_attribute',
                  'display_unit', 'modifiers_count', 'tiered_price')


class PricingPlanSerializer(AdminPricingPlanSerializer):
    reseller_client = serializers.SerializerMethodField()

    @staticmethod
    def get_pricing_rules(plan: PricingPlan):
        pricing_rules = plan.pricing_rules
        if not staff_active_features.is_enabled('openstack.instances.traffic'):
            traffic_resource = BillingResource.objects.filter(name='instance_traffic').first()
            pricing_rules = pricing_rules.exclude(resource=traffic_resource).all()
        return PriceRuleMinSerializer(many=True, read_only=True).to_representation(pricing_rules)

    class Meta:
        model = PricingPlan
        fields = '__all__'

    @staticmethod
    def get_reseller_client(plan: PricingPlan):
        return StaffClientBriefSerializer().to_representation(
            instance=plan.reseller_resources.service.client
        ) if plan.reseller_resources else None


class PricingPlanUpdateSerializer(serializers.ModelSerializer):
    other_default = serializers.PrimaryKeyRelatedField(queryset=PricingPlan.objects.all(), required=False)

    class Meta:
        model = PricingPlan
        fields = ('name', 'currency', 'is_default', 'other_default')
