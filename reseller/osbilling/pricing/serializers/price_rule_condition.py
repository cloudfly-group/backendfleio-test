from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from fleio.osbilling.models import PricingRule
from fleio.osbilling.models import PricingRuleCondition


class ResellerPriceRuleConditionSerializer(serializers.ModelSerializer):
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
