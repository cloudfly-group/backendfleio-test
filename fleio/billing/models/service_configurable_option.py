import decimal
from django.db import models
from django.db.models.functions import Coalesce

from .configurable_option import ConfigurableOption, ConfigurableOptionStatus
from .service import Service


class ServiceConfigurableOptionQueryset(models.QuerySet):
    def visible_to_client(self):
        return self.filter(option__status__in=(ConfigurableOptionStatus.public, ConfigurableOptionStatus.retired))

    def total_price(self):
        return self.aggregate(total=Coalesce(models.Sum('price'), 0))['total']


class ServiceConfigurableOption(models.Model):
    service = models.ForeignKey(Service,
                                related_name='configurable_options',
                                null=True,
                                blank=True,
                                on_delete=models.CASCADE)
    option = models.ForeignKey(ConfigurableOption, related_name='services', on_delete=models.CASCADE)
    option_value = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    has_price = models.BooleanField(default=False)
    taxable = models.BooleanField(default=False)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default='0.00')
    price = models.DecimalField(max_digits=12, decimal_places=2, default='0.00')
    setup_fee = models.DecimalField(max_digits=12, decimal_places=2, default='0.00')

    objects = ServiceConfigurableOptionQueryset.as_manager()

    @property
    def is_free(self):
        if self.price == decimal.Decimal('0.00') and self.setup_fee == decimal.Decimal('0.00'):
            return True
        return False

    @property
    def display(self):
        if self.option.widget in ('drop', 'radio'):
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

    def __str__(self):
        return '{} ({})'.format(getattr(self.option, 'description', '-'), self.option_value)
