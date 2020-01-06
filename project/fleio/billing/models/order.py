from jsonfield import JSONField

from django.db import models
from django.utils.encoding import smart_text
from django.utils.timezone import now as utcnow
from django.utils.translation import ugettext_lazy as _

from fleio.billing.settings import OrderStatus
from fleio.core.models import Client
from fleio.core.models import Currency
from fleio.core.models import get_default_currency
from fleio.core.utils import RandomId
from fleio.settings import AUTH_USER_MODEL


class Order(models.Model):
    id = models.BigIntegerField(_('Random id'), default=RandomId('billing.Order'), primary_key=True)
    order_date = models.DateTimeField(db_index=True, default=utcnow)
    user = models.ForeignKey(AUTH_USER_MODEL, related_name='orders',
                             db_index=True, on_delete=models.CASCADE,
                             help_text=_('User who placed the order. Can be a staff user.'))
    client = models.ForeignKey(Client, related_name='orders', db_index=True, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, default=get_default_currency, on_delete=models.CASCADE)
    status = models.CharField(max_length=32, choices=OrderStatus.choices, default=OrderStatus.pending, db_index=True)
    invoice = models.OneToOneField('billing.Invoice', related_name='order', null=True, blank=True,
                                   on_delete=models.SET_NULL)
    client_notes = models.TextField(max_length=4096, null=True, blank=True)
    staff_notes = models.TextField(max_length=4096, null=True, blank=True)
    fraud_check_result = JSONField(null=True, blank=True, default=None)
    metadata = JSONField(default=dict(), help_text='Various request attributes like IP Address a.s.o.')

    class Meta:
        get_latest_by = "order_date"
        ordering = ['-order_date']

    @property
    def total(self):
        return self.items.total_price()

    def __str__(self):
        return smart_text(self.id)
