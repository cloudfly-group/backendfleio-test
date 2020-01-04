from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _

from fleio.billing.models import ConfigurableOption, ConfigurableOptionChoice, ConfigurableOptionCycle
from fleio.billing.models.configurable_option import ConfigurableOptionWidget
from fleio.core.models import get_default_currency
from fleio.billing import utils


class ConfigCycleSerializer(serializers.ModelSerializer):
    display_name = serializers.CharField(read_only=True)

    class Meta:
        model = ConfigurableOptionCycle
        fields = '__all__'

    def validate(self, attrs):
        # NOTE(tomo): Validate cycle is unique
        value = attrs.get('value')
        option = attrs.get('option')
        cycle = attrs.get('cycle')
        cycle_multiplier = attrs.get('cycle_multiplier')
        currency = attrs.get('currency')
        if not currency:
            raise serializers.ValidationError(detail=_('Currency is required'))
        extra_attrs = {}
        if value:
            extra_attrs['value'] = value
        elif option:
            extra_attrs['option'] = option
        else:
            extra_attrs['value__isnull'] = True
            extra_attrs['option__isnull'] = True
        exist_query = ConfigurableOptionCycle.objects
        if self.instance:
            # We edit the same instance, exclude it from query
            exist_query = exist_query.exclude(pk=self.instance.pk)
        if exist_query.filter(cycle=cycle,
                              cycle_multiplier=cycle_multiplier,
                              currency=currency,
                              **extra_attrs).exists():
            raise serializers.ValidationError(detail='Similar cycle already exists')
        # End cycle unique validation
        relative_pricing = attrs.get('is_relative_price', False)
        if relative_pricing:
            # Check if relative pricing is sent, modify pricing if we have a similar cycle in default currency
            # or just raise
            default_currency = get_default_currency()
            if attrs['currency'] != default_currency:
                def_cycle = ConfigurableOptionCycle.objects.filter(
                    option=option,
                    cycle=cycle,
                    cycle_multiplier=cycle_multiplier,
                    currency=default_currency
                ).first()
                if def_cycle is None:
                    raise serializers.ValidationError(detail=_('Unable to auto calculate prices'))
                converted_price = utils.convert_currency(price=def_cycle.price,
                                                         from_currency=def_cycle.currency,
                                                         to_currency=attrs['currency'])
                attrs['price'] = utils.cdecimal(converted_price, q='.01')
                converted_setup_fee = utils.convert_currency(price=def_cycle.setup_fee,
                                                             from_currency=def_cycle.currency,
                                                             to_currency=attrs['currency'])
                attrs['setup_fee'] = utils.cdecimal(converted_setup_fee, q='.01')
        return attrs


class ConfigurableOptionChoiceSerializer(serializers.ModelSerializer):
    cycles = ConfigCycleSerializer(many=True, read_only=True)

    class Meta:
        model = ConfigurableOptionChoice
        fields = '__all__'


class ConfigurableOptionsSerializer(serializers.ModelSerializer):
    cycles = ConfigCycleSerializer(many=True, read_only=True)
    choices = ConfigurableOptionChoiceSerializer(many=True, read_only=True)
    settings = serializers.JSONField()

    class Meta:
        model = ConfigurableOption
        fields = '__all__'

    @staticmethod
    def validate_name(value: str):
        if not value or not value.isidentifier():
            raise serializers.ValidationError(detail='Name may only contain letters, numbers and _')
        return value

    def update(self, instance, validated_data):
        option = super(ConfigurableOptionsSerializer, self).update(instance=instance, validated_data=validated_data)
        if option.widget in ConfigurableOptionWidget.WITHOUT_CHOICES:
            option.choices.all().delete()  # NOTE(tomo): no choices are needed for yes no or quantity options
        else:
            option.cycles.filter(value__isnull=True).delete()
        return option
