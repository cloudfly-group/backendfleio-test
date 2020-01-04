import decimal

from django.db import models
from django.utils.translation import ugettext_lazy as _
from jsonfield import JSONField

from fleio.billing import utils
from fleio.billing.settings import CyclePeriods
from fleio.core.models import Currency
from fleio.core.models import get_default_currency


class ConfigurableOptionWidget:
    dropdown = 'drop'
    yesno = 'yesno'
    radio = 'radio'
    number_input = 'num_in'
    text_input = 'text_in'

    CHOICES = [
        (dropdown, _('Dropdown')),
        (radio, _('Radio')),
        (yesno, _('Yes/No')),
        (number_input, _('Quantity input')),
        (text_input, _('Text input'))
    ]

    WITH_CHOICES = (dropdown, radio)
    WITHOUT_CHOICES = (yesno, number_input, text_input)


class ConfigurableOptionStatus:
    public = 'public'
    private = 'private'
    retired = 'retired'

    CHOICES = [
        (public, _('Public')),
        (private, _('Private')),
        (retired, _('Retired'))
    ]


class ConfigurableOptionQueryset(models.QuerySet):
    def public(self):
        """Public options, available to everyone"""
        return self.filter(status=ConfigurableOptionStatus.public)

    def private(self):
        """Private options, only available to staff and modules"""
        return self.filter(status=ConfigurableOptionStatus.private)

    def public_or_retired(self):
        return self.filter(status__in=(ConfigurableOptionStatus.public, ConfigurableOptionStatus.retired))

    def with_cycles(self, cycle=None, cycle_multiplier=None, currency=None, required=None):
        """Returns all configurable options that are public, with cycles"""
        if cycle and cycle_multiplier:
            options_with_choices = models.Q(widget__in=ConfigurableOptionWidget.WITH_CHOICES,
                                            choices__cycles__cycle=cycle,
                                            choices__cycles__cycle_multiplier=cycle_multiplier,
                                            choices__cycles__currency__code=currency)
            options_wo_choices = models.Q(widget__in=ConfigurableOptionWidget.WITHOUT_CHOICES,
                                          cycles__cycle=cycle,
                                          cycles__cycle_multiplier=cycle_multiplier,
                                          cycles__currency__code=currency)
        else:
            options_with_choices = models.Q(widget__in=ConfigurableOptionWidget.WITH_CHOICES,
                                            choices__cycles__isnull=False,
                                            choices__cycles__currency__code=currency)
            options_wo_choices = models.Q(widget__in=ConfigurableOptionWidget.WITHOUT_CHOICES,
                                          cycles__isnull=False,
                                          cycles__currency__code=currency)

        options_filter = models.Q(options_with_choices) | models.Q(options_wo_choices)

        if required is True or required is False:
            return self.filter(options_filter).filter(required=required).distinct()
        else:
            return self.filter(options_filter).distinct()


class ConfigurableOption(models.Model):
    WIDGET_CHOICES = ConfigurableOptionWidget

    name = models.CharField(max_length=64, db_index=True)
    description = models.CharField(max_length=128, help_text='Text to display on order and invoices')
    help_text = models.CharField(max_length=255, null=True, blank=True)
    widget = models.CharField(choices=ConfigurableOptionWidget.CHOICES, max_length=12, db_index=True)
    status = models.CharField(choices=ConfigurableOptionStatus.CHOICES, max_length=8, db_index=True)
    settings = JSONField(default={})
    required = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = ConfigurableOptionQueryset.as_manager()
    visible = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def get_price_by_cycle_quantity_and_choice(self, cycle_name, cycle_multiplier, quantity, currency,
                                               choice_value=None, option_value=None):
        zero = decimal.Decimal('0.00')
        if self.widget == ConfigurableOptionWidget.yesno and option_value != 'yes':
            return zero, zero, zero
        if self.widget in ConfigurableOptionWidget.WITHOUT_CHOICES:
            cycle = self.cycles.filter(cycle=cycle_name,
                                       cycle_multiplier=cycle_multiplier,
                                       currency=currency).first()
            if cycle:
                price = cycle.price * quantity
                if cycle.setup_fee_entire_quantity:
                    setup_fee = cycle.setup_fee
                else:
                    setup_fee = quantity * cycle.setup_fee
                return (utils.cdecimal(cycle.price, q='0.01'),
                        utils.cdecimal(price, q='0.01'),
                        utils.cdecimal(setup_fee, q='0.01'))
        elif self.widget in ConfigurableOptionWidget.WITH_CHOICES:
            value = self.choices.filter(choice=choice_value).first()
            if value:
                cycle = value.cycles.filter(cycle=cycle_name,
                                            cycle_multiplier=cycle_multiplier,
                                            currency=currency).first()
                if cycle is None:
                    return zero, zero, zero
                else:
                    price = cycle.price * quantity
                    if cycle.setup_fee_entire_quantity:
                        setup_fee = cycle.setup_fee
                    else:
                        setup_fee = quantity * cycle.setup_fee
                    return (utils.cdecimal(cycle.price, q='0.01'),
                            utils.cdecimal(price, q='0.01'),
                            utils.cdecimal(setup_fee, q='0.01'))
        return zero, zero, zero

    def has_cycle(self, cycle, cycle_multiplier, choice_value=None, currency=None):
        if self.widget in ConfigurableOptionWidget.WITH_CHOICES:
            return self.choices.filter(choice=choice_value,
                                       cycles__cycle=cycle,
                                       cycles__cycle_multiplier=cycle_multiplier,
                                       cycles__currency__code=currency).exists()
        else:
            return self.cycles.filter(cycle=cycle,
                                      cycle_multiplier=cycle_multiplier,
                                      currency__code=currency).exists()

    def product_cycles_match(self, product):
        return utils.config_option_cycles_match_product(configurable_option=self,
                                                        product=product)

    @property
    def has_choices(self):
        return self.widget in self.WIDGET_CHOICES.WITH_CHOICES

    @property
    def has_quantity(self):
        return self.widget == 'num_in'

    def __str__(self):
        return self.name


class ConfigurableOptionChoice(models.Model):
    option = models.ForeignKey(ConfigurableOption, related_name='choices', on_delete=models.CASCADE)
    choice = models.CharField(max_length=64, default='', help_text='Only valid for Drop or Radio widget')
    label = models.CharField(max_length=128, default='', help_text='Only valid for Drop or Radio widget')

    class Meta:
        unique_together = ('option', 'choice')

    def __str__(self):
        return '{} {}'.format(self.label, self.choice)


class ConfigurableOptionCycle(models.Model):
    value = models.ForeignKey(ConfigurableOptionChoice, related_name='cycles', on_delete=models.CASCADE,
                              null=True, blank=True)
    option = models.ForeignKey(ConfigurableOption, related_name='cycles', null=True, blank=True,
                               on_delete=models.CASCADE)
    cycle = models.CharField(max_length=8, choices=CyclePeriods.choices, db_index=True)
    cycle_multiplier = models.IntegerField(default=1, db_index=True)
    price = models.DecimalField(max_digits=14, decimal_places=2, default=decimal.Decimal('0.00'))
    currency = models.ForeignKey(Currency, null=True, blank=True, default=get_default_currency,
                                 on_delete=models.SET_DEFAULT)
    setup_fee = models.DecimalField(max_digits=14, decimal_places=2, default=decimal.Decimal('0.00'))
    setup_fee_entire_quantity = models.BooleanField(default=True, help_text=_('Apply to quantity options'))
    is_relative_price = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    @property
    def display_name(self):
        return CyclePeriods.display_name(cycle=self.cycle, multiplier=self.cycle_multiplier)

    def __str__(self):
        return '{}'.format(self.display_name)
