import logging

from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from fleio.core.models import Client
from .models import PricingPlan

LOG = logging.getLogger(__name__)


@receiver(post_save, sender=Client)
def client_post_save_callback(sender, **kwargs):
    LOG.debug('Client post save callback invoked by {}'.format(sender))
    client = kwargs.get('instance')
    if kwargs.get('created', False):
        del client


@receiver(pre_delete, sender=PricingPlan)
def change_default_plan(sender, **kwargs):
    LOG.debug('Pricing plan delete callback invoked by {}'.format(sender))
    instance = kwargs.get('instance', None)  # type: PricingPlan
    if instance and instance.is_default:
        existing_plan = PricingPlan.objects.filter(reseller_resources=instance.reseller_resources).first()
        if existing_plan:
            existing_plan.is_default = True
            existing_plan.save()
