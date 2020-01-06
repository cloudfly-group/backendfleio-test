from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from fleio.osbilling.models import PricingRule
from fleio.osbilling.models import PricingRuleModifier


class ResellerPriceRuleModifierSerializer(serializers.ModelSerializer):
    value = serializers.JSONField()
    price = serializers.DecimalField(coerce_to_string=False, max_digits=12, decimal_places=4)

    class Meta:
        model = PricingRuleModifier
        exclude = ('price_rule', )

    def validate(self, attrs):
        attrs = super().validate(attrs)
        # FIXME(tomo): Get pricerule_pk in some other way
        price_rule_id = self.context['view'].kwargs.get('pricerule_pk', None)
        if price_rule_id:
            for condition in PricingRule.objects.get(id=price_rule_id).conditions.all():
                if condition.attribute == attrs['attribute']:
                    msg = _('Attribute {} already present in conditions').format(attrs['attribute'])
                    raise serializers.ValidationError({'attribute': msg})
        return attrs
