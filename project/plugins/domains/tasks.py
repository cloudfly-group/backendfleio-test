from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from fleio.billing.models import Service
from fleio.celery import app


@app.task(
    bind=True,
    max_retries=settings.TASK_RETRIES,
    name='Delete domain task',
    resource_type='Service'
)
def delete_domain_task(self, service_id, **kwargs):
    del self, kwargs  # unused
    service = Service.objects.filter(id=service_id).first()
    if service:
        try:
            service.domain.delete()
        except ObjectDoesNotExist:
            pass
