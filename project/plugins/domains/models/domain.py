from collections import OrderedDict

from django.db import models
from django.db import transaction
from django.utils.translation import ugettext_lazy as _

from fleio.billing.models import Service
from fleio.core.utils import RandomId

from .contact import Contact
from .nameserver import Nameserver
from .registrar import Registrar
from .tld import TLD


class DomainStatus:
    # general statuses
    undefined = 'undefined'
    unmanaged = 'unmanaged'

    # managed domains statuses
    pending = 'pending'
    pending_transfer = 'pending_transfer'
    active = 'active'
    grace = 'grace'
    redemption = 'redemption'
    expired = 'expired'
    transferred_away = 'transferred_away'
    cancelled = 'cancelled'
    deleted = 'deleted'
    fraud = 'fraud'

    domain_status_map = OrderedDict([
        (undefined, _('Undefined')),
        (unmanaged, _('Unmanaged')),
        (pending, _('Registration pending')),
        (pending_transfer, _('Transfer pending')),
        (active, _('Active')),
        (grace, _('Grace')),
        (redemption, _('Redemption')),
        (expired, _('Expired')),
        (transferred_away, _('Transferred away')),
        (cancelled, _('Cancelled')),
        (deleted, _('Deleted')),
        (fraud, _('Fraud')),
    ])


class Domain(models.Model):
    id = models.BigIntegerField(unique=True, default=RandomId('plugins.Domain'), primary_key=True)
    name = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    tld = models.ForeignKey(TLD, on_delete=models.PROTECT, related_name='domains')
    service = models.OneToOneField(Service, on_delete=models.PROTECT, related_name='domain', null=True, blank=True)
    assigned_to_service = models.OneToOneField(
        Service,
        on_delete=models.SET_NULL,
        related_name='assigned_domain',
        null=True,
        blank=True,
    )
    managed = models.BooleanField(default=False, blank=True)
    nameservers = models.ManyToManyField(Nameserver, related_name='domains', blank=True)
    last_registrar = models.ForeignKey(
        Registrar,
        on_delete=models.PROTECT,
        related_name='domains',
        null=True,
        blank=True
    )
    status = models.CharField(max_length=100, default=DomainStatus.undefined)
    registration_date = models.DateField(default=None, null=True, blank=True)
    expiry_date = models.DateField(default=None, null=True, blank=True)
    registration_period = models.IntegerField(default=1, null=False, blank=False)
    registrar_locked = models.BooleanField(default=False)
    epp_code = models.CharField(max_length=255, null=True, blank=True)
    contact = models.ForeignKey(Contact, on_delete=models.PROTECT, related_name='domains', null=True, blank=True)

    def __str__(self):
        return _('Domain {}').format(self.name)

    def delete(self, using=None, keep_parents=False):
        # TODO: maybe use service delete task here?
        with transaction.atomic():
            super().delete(using=using, keep_parents=keep_parents)
            if self.service:
                self.service.delete()
