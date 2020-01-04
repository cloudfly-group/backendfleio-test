import logging

import celery
from django.conf import settings

from fleio.billing.models import Service
from fleio.celery import app
from fleio.core.tasks import terminate_client
from fleio.reseller.models import ResellerResources

LOG = logging.getLogger(__name__)


@app.task(bind=True, max_retries=settings.TASK_RETRIES, name='Delete reseller resources from db',
          resource_type='ResellerResources')
def delete_reseller_resources_from_db(self, reseller_resources_id: int):
    del self  # unused
    reseller_resources = ResellerResources.objects.filter(id=reseller_resources_id).first()
    if reseller_resources:
        reseller_resources.flavor_groups.all().delete()
        reseller_resources.configurations.all().delete()
        reseller_resources.pricing_plans.all().delete()
        reseller_resources.user_groups.all().delete()
        reseller_resources.users.all().delete()
        reseller_resources.client_groups.all().delete()

        for image in reseller_resources.images.all():
            image.reseller_resources = None
            image.save()

        for flavor in reseller_resources.flavors.all():
            flavor.reseller_resources = None
            flavor.save()

        reseller_resources.delete()


@app.task(bind=True, max_retries=settings.TASK_RETRIES, name='Delete reseller service resources',
          resource_type='Project')
def delete_reseller_service_resources(self, service_id: int):
    del self  # unused

    service = Service.objects.filter(id=service_id).first()
    if service:
        if service.reseller_resources:
            resources = service.reseller_resources

            delete_tasks = []
            for client in resources.clients.all():
                delete_tasks.append(
                    terminate_client.si(
                        client_id=client.id,
                        delete_all_resources=True,
                    )
                )

            delete_tasks.append(delete_reseller_resources_from_db.si(reseller_resources_id=resources.id))
            celery.chain(delete_tasks).apply_async()
        else:
            LOG.error('Service {}({}) has no reseller resources'.format(service, service.id))

    else:
        LOG.error('Cannot find service {}'.format(service_id))
