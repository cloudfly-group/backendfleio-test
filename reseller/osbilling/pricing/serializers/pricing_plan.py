from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from common_admin.osbilling.pricing.serializers.pricing_plan import AdminPricingPlanSerializer
from fleio.core.features import reseller_active_features
from fleio.osbilling.models import BillingResource
from fleio.osbilling.models import PricingPlan
from reseller.osbilling.pricing.serializers.price_rule import ResellerPriceRuleMinSerializer
from reseller.utils.serialization import CurrentResellerResourcesDefault


class ResellerPricingPlanSerializer(AdminPricingPlanSerializer):
    reseller_resources = serializers.HiddenField(default=CurrentResellerResourcesDefault())

    @staticmethod
    def get_pricing_rules(plan: PricingPlan):
        pricing_rules = plan.pricing_rules
        if not reseller_active_features.is_enabled('openstack.instances.traffic'):
            traffic_resource = BillingResource.objects.filter(name='instance_traffic').first()
            pricing_rules = pricing_rules.exclude(resource=traffic_resource).all()
        return ResellerPriceRuleMinSerializer(many=True, read_only=True).to_representation(pricing_rules)

    class Meta:
        model = PricingPlan
        fields = '__all__'


class ResellerPricingPlanDeleteSerializer(serializers.Serializer):
    plan_to_migrate = serializers.PrimaryKeyRelatedField(queryset=PricingPlan.objects.all())

    def __init__(self, plan, *args, **kwargs):
        self.plan = plan
        super().__init__(*args, **kwargs)

    def validate_plan_to_migrate(self, data):
        if data.id == self.plan.id:
            raise serializers.ValidationError(_('Can\'t migrate to selected plan'))
        if data.reseller_resources != self.plan.reseller_resources:
            raise serializers.ValidationError(_('Can\'t migrate to another reseller plan'))

        return data

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class ResellerPricingPlanUpdateSerializer(serializers.ModelSerializer):
    reseller_resources = serializers.HiddenField(default=CurrentResellerResourcesDefault())
    other_default = serializers.PrimaryKeyRelatedField(
        queryset=PricingPlan.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = PricingPlan
        fields = ('name', 'currency', 'is_default', 'other_default', 'reseller_resources')

    def validate_other_default(self, other_default):
        if other_default and other_default.reseller != self.context.get('request').user:
            raise serializers.ValidationError(_('Invalid reseller for other default plan.'))

        return other_default
