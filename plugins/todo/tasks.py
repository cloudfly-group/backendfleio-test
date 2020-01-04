from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from fleio.billing.models import Service

from fleio.celery import app
from fleio.emailing import send_email

from plugins.todo import models
from plugins.todo.models import TODOProductSettings


@app.task(
    bind=True,
    max_retries=settings.TASK_RETRIES,
    name='Add TODO for delete service',
    resource_type='Service'
)
def add_todo_for_delete_service(self, service_id, **kwargs):
    del self, kwargs  # unused

    service = Service.objects.get(pk=service_id)
    try:
        todo_settings = service.product.todo_settings  # type: TODOProductSettings
    except AttributeError:
        todo_settings = None

    if todo_settings and todo_settings.add_todo_on_destroy:
        models.TODO.objects.add_todo(
            title=_('Service deleted'),
            description=_('Service {} was deleted').format(service),
            assigned_to=todo_settings.todo_user
        )


@app.task(
    bind=True, max_retries=settings.TASK_RETRIES,
    name='Send TODO email',
    resource_type='User'
)
def send_todo_email(self, todo_id: int, email_type: str):
    del self  # unused

    todo = models.TODO.objects.get(id=todo_id)  # type: models.TODO
    if not todo.assigned_to:
        # we cannot send mail if there is no assignee
        return

    user = todo.assigned_to
    if email_type == 'created':
        email_subject = str(_('A new TODO has been created and assigned to you'))
        email_body = str(_('The TODO "{}" has been created and assigned to you')).format(todo)
    else:
        email_subject = str(_('A TODO assigned to you has been changed'))
        email_body = str(_('The TODO {} assigned to you has been changed')).format(todo)

    to_email = user.email
    from_email = None

    send_email(
        from_field=from_email,
        to_emails=to_email,
        subject_template=email_subject,
        body_template=email_body,
        params={}
    )
