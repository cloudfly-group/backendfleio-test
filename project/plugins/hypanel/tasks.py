from django.conf import settings

from fleio.celery import app

from plugins.hypanel.utils import send_hypanel_request


@app.task(
    bind=True,
    max_retries=settings.TASK_RETRIES,
    name='Delete hypanel task',
    resource_type='Service'
)
def delete_hypanel_task(self, service_id, **kwargs):
    del self  # unused
    send_hypanel_request(
        hypanel_server_settings=kwargs.get('hypanel_server_settings'),
        method='terminate_machine',
        params={
            'billing_client_id': kwargs.get('billing_client_id'),
            'billing_service_id': service_id
        }
    )
