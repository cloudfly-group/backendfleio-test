from django.db import models

from fleio.billing.models import Service
from fleio.core.models import AppUser
from fleio.core.models import Client
from fleio.osbilling.models import PricingPlan


class ResellerResourcesManager(models.Manager):
    def for_user(self, user: AppUser):
        return self.filter(service__client__users=user)

    def for_client(self, client: Client):
        return self.filter(service__client=client)


class ResellerResources(models.Model):
    service = models.OneToOneField(
        Service,
        related_name='reseller_resources',
        on_delete=models.PROTECT,
        db_index=True,
        null=True,
        blank=True,
    )
    plan = models.ForeignKey(
        PricingPlan,
        related_name='+',
        on_delete=models.PROTECT,
        db_index=True,
        null=True,
        blank=True,
    )

    enduser_panel_url = models.URLField(default=None, blank=True, null=True)

    objects = ResellerResourcesManager()

    def __str__(self):
        return 'Reseller resources for {}'.format(self.service.client)
