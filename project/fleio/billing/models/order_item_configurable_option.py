import decimal
from django.db import models

from .order_item import OrderItem
from .configurable_option import ConfigurableOption


class OrderItemConfigurableOption(models.Model):
    order_item = models.ForeignKey(OrderItem,
                                   related_name='configurable_options',
                                   on_delete=models.CASCADE)
    option = models.ForeignKey(ConfigurableOption, related_name='order_items_configurable_options',
                               null=True, blank=True,
                               on_delete=models.SET_NULL)
    option_value = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    has_price = models.BooleanField(default=False)
    taxable = models.BooleanField(default=False)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default='0.00')
    price = models.DecimalField(max_digits=12, decimal_places=2, default='0.00')
    setup_fee = models.DecimalField(max_digits=12, decimal_places=2, default='0.00')

    @property
    def display(self):
        if self.option.has_choices:
            choice = self.option.choices.filter(choice=self.option_value).first()
            if choice and choice.label:
                return '{}: {}'.format(self.option.description, choice.label)
            else:
                return '{}: {}'.format(self.option.description, choice.choice)
        elif self.option and self.option.widget == 'num_in':
            return '{}: {}'.format(self.option.description, self.quantity)
        elif self.option and self.option.widget == 'yesno':
            return '{}'.format(self.option.description)
        elif self.option:
            return '{}: {}'.format(self.option.description, self.option_value)

    @property
    def is_free(self):
        if self.price == decimal.Decimal('0.00') and self.setup_fee == decimal.Decimal('0.00'):
            return True
        return False

    def __str__(self):
        return '{} ({})'.format(getattr(self.option, 'description', ''), self.quantity)
