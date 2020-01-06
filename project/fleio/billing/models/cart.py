import decimal
from django.db import models
from django.db.models import F, Sum
from django.db.models.functions import Coalesce
from jsonfield import JSONField

from fleio.core.models import AppUser
from fleio.core.models import Client
from fleio.core.models import Currency


class FleioCart(models.Model):
    storage_id = models.CharField(max_length=255, db_index=True)
    user = models.OneToOneField(AppUser, related_name='fleio_cart', null=True, blank=True, on_delete=models.CASCADE)
    client = models.OneToOneField(Client, related_name='fleio_cart', null=True, blank=True, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    metadata = JSONField(default={})
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total(self):
        # NOTE(tomo): Avoids None results from taxes not being present
        zero = decimal.Decimal('0.00')
        total = self.items.aggregate(total=Sum(F('fixed_price') + F('setup_fee')) +
                                     Coalesce(Sum(F('taxes__amount')), 0))['total']
        total = total or zero
        config_options_total = self.items.aggregate(total=Coalesce(Sum(F('configurable_options__price') +
                                                    F('configurable_options__setup_fee')), 0))['total']
        config_options_total = config_options_total or zero
        return total + config_options_total

    @property
    def subtotal(self):
        zero = decimal.Decimal('0.00')
        subtotal = self.items.aggregate(subtotal=Sum(F('fixed_price')))['subtotal']
        subtotal = subtotal or zero
        options_subtotal = self.items.aggregate(subtotal=Coalesce(Sum(F('configurable_options__price')), 0))['subtotal']
        options_subtotal = options_subtotal or zero
        return subtotal + options_subtotal

    @property
    def setup_fees(self):
        zero = decimal.Decimal('0.00')
        setup_fee = self.items.aggregate(setup_fees=Sum(F('setup_fee')))['setup_fees']
        setup_fee = setup_fee or zero
        option_setup_fee = self.items.aggregate(sf=Coalesce(Sum(F('configurable_options__setup_fee')), 0))['sf']
        option_setup_fee = option_setup_fee or zero
        return setup_fee + option_setup_fee

    @property
    def taxes(self):
        taxed_items = self.items.filter(taxes__isnull=False)
        return taxed_items.values('taxes__name').order_by('taxes__name').annotate(amount=Sum('taxes__amount'))
