from django.db import models
from django.utils.timezone import now as utcnow
from django.utils.translation import ugettext_lazy as _

from fleio.settings import AUTH_USER_MODEL
from fleio.core.utils import RandomId


class CancellationTypes(object):
    IMMEDIATE = 'immediate'
    END_OF_CYCLE = 'cycleend'

    choices = ((IMMEDIATE, _('Immediate')),
               (END_OF_CYCLE, _('At the end of billing period')))


class CancellationRequest(models.Model):
    id = models.BigIntegerField(_('Random id'), default=RandomId('billing.CancellationRequest'), primary_key=True)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    reason = models.TextField(max_length=2048)
    cancellation_type = models.CharField(choices=CancellationTypes.choices, max_length=10, db_index=True)
    created_at = models.DateTimeField(default=utcnow, db_index=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    objects = models.Manager()

    class Meta:
        app_label = 'billing'

    def __str__(self):
        return self.cancellation_type
