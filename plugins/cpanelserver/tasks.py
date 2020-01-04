import logging
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from fleio.billing.models import Service
from fleio.celery import app as app_task
from .utils import get_whmclient_from_service

LOG = logging.getLogger(__name__)


@app_task.task(
    bind=True,
    max_retries=settings.TASK_RETRIES,
    name='Delete cPanel account',
    resource_type='Service'
)
def delete_cpanel_account(self, service_id, **kwargs):
    del self, kwargs  # unused
    service = Service.objects.get(pk=service_id)
    try:
        account = service.hosting_account
    except ObjectDoesNotExist:
        LOG.error('cPanel service does not have a hosting account associated')
    else:
        with transaction.atomic():
            whmapi = get_whmclient_from_service(service=service)
            response = whmapi.request('removeacct', user=account.username)
            service.hosting_account.delete()
        return response
