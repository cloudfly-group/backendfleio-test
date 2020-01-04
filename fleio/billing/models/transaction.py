import decimal
from jsonfield import JSONField

from django.db import models
from django.utils.timezone import now as utcnow
from django.utils.translation import ugettext_lazy as _

from fleio.core.models import Currency

from .gateway import Gateway
from .invoice import Invoice


class TransactionStatus(object):
    WAITING = 'waiting'
    PREAUTH = 'preauth'
    CONFIRMED = 'confirmed'
    REJECTED = 'rejected'
    REFUNDED = 'refunded'
    PARTIAL_REFUNDED = 'refundpart'
    SUCCESS = 'success'
    FAILURE = 'failure'
    CANCELED = 'canceled'
    UNKNOWN = 'unknown'

    STATUS_CHOICES = ((WAITING, _('Waiting')),
                      (PREAUTH, _('Preauthorization')),
                      (CONFIRMED, _('Confirmed')),
                      (REJECTED, _('Rejected')),
                      (REFUNDED, _('Refunded')),
                      (PARTIAL_REFUNDED, _('Partially Refunded')),
                      (SUCCESS, _('Success')),
                      (FAILURE, _('Failure')),
                      (CANCELED, _('Canceled')),
                      (UNKNOWN, _('Unknown')))


class TransactionQuerySet(models.QuerySet):
    pass


class Transaction(models.Model):
    """Gateway transaction"""
    TRANSACTION_STATUS = TransactionStatus
    external_id = models.CharField(max_length=64, db_index=True, blank=True, null=True)
    invoice = models.ForeignKey(Invoice, related_name='transactions', unique=False, blank=True, null=True,
                                on_delete=models.SET_NULL)
    date_initiated = models.DateTimeField(db_index=True, default=utcnow)
    gateway = models.ForeignKey(Gateway, related_name='transactions', blank=True, null=True,
                                on_delete=models.SET_NULL)
    status = models.CharField(max_length=10, db_index=True, choices=TRANSACTION_STATUS.STATUS_CHOICES)
    currency = models.ForeignKey(Currency, blank=True, null=True, on_delete=models.SET_NULL)
    amount = models.DecimalField(max_digits=14, decimal_places=2, default=decimal.Decimal('0.00'))
    fee = models.DecimalField(max_digits=14, decimal_places=2, default=decimal.Decimal('0.00'),
                              help_text='Gateway fee')
    extra = JSONField(null=True, blank=True)
    refunded_transaction = models.ForeignKey("self", related_name="refund_transactions", blank=True, null=True,
                                             on_delete=models.PROTECT)

    objects = TransactionQuerySet.as_manager()

    def __str__(self):
        return '{0} / {1}'.format(self.id, self.external_id)

    def is_refundable(self):
        if self.refunded_transaction is not None:
            return False
        if self.status not in (TransactionStatus.CONFIRMED,
                               TransactionStatus.PARTIAL_REFUNDED,
                               TransactionStatus.PREAUTH,
                               TransactionStatus.SUCCESS):
            return False
        return True
