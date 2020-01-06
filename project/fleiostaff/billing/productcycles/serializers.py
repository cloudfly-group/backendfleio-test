from django.utils.translation import ugettext_lazy as _
from fleio.billing import utils
from fleio.billing.models import ProductCycle
from rest_framework import serializers

from fleio.billing.settings import CyclePeriods
from fleio.core.models import get_default_currency


class StaffProductCycleSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCycle
        fields = '__all__'

    def validate(self, attrs):
        attrs = super(StaffProductCycleSerializer, self).validate(attrs)
        cycle = attrs.get('cycle')
        cycle_multiplier = attrs.get('cycle_multiplier')
        auto_calculate_price = attrs.get('is_relative_price', False)
        cycle_currency_code = attrs.get('currency')
        cycle_product = attrs.get('product')
        if cycle_product:
            # do not allow one-time cycles to go with recurring cycles
            other_cycles = ProductCycle.objects.filter(product=cycle_product)
            if cycle == CyclePeriods.onetime:
                for other_cycle in other_cycles:  # type: ProductCycle
                    if other_cycle.cycle != CyclePeriods.onetime:
                        raise serializers.ValidationError(
                            detail=_('Cannot add one time cycle if the product has a recurring cycle.')
                        )
            else:  # treat the case when the new cycle is a recurring one
                for other_cycle in other_cycles:  # type: ProductCycle
                    if other_cycle.cycle == CyclePeriods.onetime:
                        raise serializers.ValidationError(
                            detail=_('Cannot add recurring cycle if the product has a one time cycle.')
                        )
        if auto_calculate_price and cycle_product:
            # auto calculate prices
            default_currency = get_default_currency()
            if default_currency.code != cycle_currency_code:
                def_cycle = ProductCycle.objects.filter(product=cycle_product,
                                                        cycle=cycle,
                                                        cycle_multiplier=cycle_multiplier,
                                                        currency=default_currency).first()
                if def_cycle is None:
                    c_msg = _('A cycle with {} currency is required to auto calculate price').format(default_currency)
                    raise serializers.ValidationError(detail=c_msg)

                converted_price = utils.convert_currency(price=def_cycle.fixed_price,
                                                         from_currency=def_cycle.currency,
                                                         to_currency=cycle_currency_code)
                attrs['fixed_price'] = utils.cdecimal(converted_price, q='.01')
                converted_setup_fee = utils.convert_currency(price=def_cycle.setup_fee,
                                                             from_currency=def_cycle.currency,
                                                             to_currency=cycle_currency_code)
                attrs['setup_fee'] = utils.cdecimal(converted_setup_fee, q='.01')
        return attrs
