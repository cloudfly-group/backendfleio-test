from django.conf import settings

from fleio.billing.models import Service
from fleio.core.models import AppUser

from plugins.todo import signals
from plugins.todo.models import TODO
from plugins.todo.models import TODOStatus
from plugins.todo.tasks import send_todo_email

VIEW_SIGNAL_MAP = {
    'created': signals.todo_created,
    'deleted': signals.todo_deleted,
    'updated': signals.todo_updated,
}


def create_todo_for_service(
        service: Service,
        title: str,
        description: str,
        status: str = TODOStatus.open,
        assigned_to: AppUser = None,
        created_by: AppUser = None
):
    todo = TODO.objects.create(
        title=title,
        description=description,
        status=status,
        assigned_to=assigned_to,
        created_by=created_by
    )

    if getattr(settings, 'TODO_SIGNAL_FOR_SERVICE', True):
        signals.todo_created.send(
            sender=service,
            todo=todo,
        )

    if getattr(settings, 'TODO_EMAIL_FOR_SERVICE', False):
        send_todo_email.delay(todo_id=todo.id, email_type='created')

    return todo


def create_todo_for_external_caller(
        title: str,
        description: str,
        status: str = TODOStatus.open,
        assigned_to: AppUser = None,
        created_by: AppUser = None
):
    todo = TODO.objects.add_todo(
        title=title,
        description=description,
        status=status,
        assigned_to=assigned_to,
        created_by=created_by,
    )

    if getattr(settings, 'TODO_SIGNAL_FOR_EXTERNAL_CALLER', True):
        signals.todo_created.send(
            sender='external',
            todo=todo,
        )

    if getattr(settings, 'TODO_EMAIL_FOR_EXTERNAL_CALLER', False):
        send_todo_email.delay(todo_id=todo.id, email_type='created')

    return todo


def send_view_notification(user: AppUser, todo: TODO, signal_type: str):
    if getattr(settings, 'TODO_SIGNAL_FOR_VIEW', True):
        if signal_type in VIEW_SIGNAL_MAP:
            VIEW_SIGNAL_MAP[signal_type].send(sender=user, todo=todo)

    if getattr(settings, 'TODO_EMAIL_FOR_VIEW', False):
        send_todo_email.delay(todo_id=todo.id, email_type=signal_type)
