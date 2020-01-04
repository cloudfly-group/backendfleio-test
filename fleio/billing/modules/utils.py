import logging

from fleio.celery import app

LOG = logging.getLogger(__name__)


@app.task(bind=True, max_retries=1, name='Delete service resources placeholder task',
          resource_type='Service')
def delete_service_resources_placeholder(self):
    LOG.debug('Delete service resources placeholder task called.'
              ' This means service has no resources to delete')
    pass
