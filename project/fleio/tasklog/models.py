import os

from celery.result import AsyncResult
from celery.signals import before_task_publish, task_failure, task_prerun, task_retry, task_success

from django.conf import settings
from django.db import models
from django.db.utils import OperationalError
from django.db import connections
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from jsonfield import JSONField

from fleio.activitylog.models import Log


class TaskState(object):
    PENDING = 0
    STARTED = 1
    RETRY = 2
    FAILURE = 3
    SUCCESS = 4

    states_map = {
        PENDING: 'pending',
        STARTED: 'started',
        RETRY: 'retry',
        FAILURE: 'failure',
        SUCCESS: 'success',
    }


class Task(models.Model):
    """Stores called Celery tasks"""
    id = models.CharField(max_length=36, primary_key=True)
    name = models.CharField(max_length=1024)
    args = JSONField(null=True, blank=True, default=list())
    kwargs = JSONField(null=True, blank=True, default=list())
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    resource_id = models.CharField(max_length=1024, blank=True, null=True,
                                   help_text='The Fleio resource this task is associated with.')
    resource_type = models.CharField(max_length=32, db_index=True, blank=True, null=True,
                                     help_text='The Fleio resource type, like service, order, user, project')
    state = models.PositiveSmallIntegerField(default=TaskState.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    activity_log = models.ForeignKey(Log, null=True, blank=True, on_delete=models.SET_NULL, related_name='tasks')
    parent_task = models.ForeignKey(
        'tasklog.Task', null=True, blank=True, on_delete=models.SET_NULL, related_name='children',
    )

    @property
    def result(self):
        return AsyncResult(self.id).result

    def __str__(self):
        return '{} / {}'.format(self.id, self.state)

    def get_log(self):
        log_file_name = os.path.join(settings.TASK_LOG_DIR, self.id + '.log')
        if os.path.isfile(log_file_name):
            with open(log_file_name, 'r', encoding='utf-8') as log_file:
                log = str(log_file.read()).strip()
                if log:
                    return log

        return _('Task has no associated log file.')


@python_2_unicode_compatible
class TaskRun(models.Model):
    """
    Stores one entry for each task run.
    One task can be retried multiple times if first run fails.
    """
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    retry = models.PositiveSmallIntegerField(default=0)
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    # traceback field is set if tasks fails
    traceback = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ('task', 'retry',)

    def __str__(self):
        return 'Task {}, retry {}'.format(self.task_id, self.retry)


def update_or_create_task(
        task_id, name, args, kwargs, state=TaskState.PENDING, resource_type=None, parent_task_id=None,
        activity_log_id=None,
):
    user_id = kwargs.get('user_id')
    resource_id = args[0] if resource_type and args else None

    defaults = {
        'id': task_id,
        'user_id': user_id,
        'name': name,
        'args': args,
        'kwargs': kwargs,
        'state': state,
    }
    if resource_type:
        defaults['resource_type'] = resource_type
    if resource_id:
        defaults['resource_id'] = resource_id

    try:
        if parent_task_id:
            defaults['parent_task'] = Task.objects.filter(id=parent_task_id).first()
        defaults['activity_log'] = Log.objects.filter(id=activity_log_id).first()
        task, created = Task.objects.update_or_create(id=task_id, defaults=defaults)
    except OperationalError:
        # close stale db connections and reconnect in case of error
        for conn in connections.all():
            conn.close_if_unusable_or_obsolete()

        if parent_task_id:
            defaults['parent_task'] = Task.objects.filter(id=parent_task_id).first()
        defaults['activity_log'] = Log.objects.filter(id=activity_log_id).first()
        task, created = Task.objects.update_or_create(id=task_id, defaults=defaults)
    return task


def update_or_create_task_run(task, retry, started_at=None, ended_at=None, traceback=None):
    defaults = {
        'task': task,
        'retry': retry,
        'started_at': started_at,
        'ended_at': ended_at,
        'traceback': traceback,
    }

    try:
        TaskRun.objects.update_or_create(task=task, retry=retry, defaults=defaults)
    except OperationalError:
        # close stale db connections and reconnect in case of error
        for conn in connections.all():
            conn.close_if_unusable_or_obsolete()
        TaskRun.objects.update_or_create(task=task, retry=retry, defaults=defaults)


@before_task_publish.connect
def before_task_published_handler(sender=None, headers=None, body=None, **kwargs):
    del sender, kwargs  # unused
    info = headers if 'task' in headers else body
    args = body[0]
    kwargs = body[1]
    task_id = info['id']
    name = headers['task']

    values = {
        'user_id': kwargs.get('user_id'),
        'name': name,
        'args': args,
        'kwargs': kwargs,
        'state': TaskState.PENDING,
    }

    Task.objects.get_or_create(id=task_id, defaults=values)


@task_prerun.connect
def task_prerun_handler(task_id=None, task=None, args=None, **kwargs):
    optional_args = kwargs['kwargs'].copy()
    parent_task_id = optional_args.get('parent_task_id', None)
    activity_log_id = optional_args.get('activity_log_id', None)
    resource_type = getattr(task, 'resource_type', None)
    name = getattr(task, 'name', None)
    db_task = update_or_create_task(
        task_id=task_id,
        name=name,
        resource_type=resource_type,
        state=TaskState.STARTED,
        args=args,
        kwargs=optional_args,
        parent_task_id=parent_task_id,
        activity_log_id=activity_log_id,
    )
    update_or_create_task_run(db_task, retry=task.request.retries, started_at=timezone.now())


@task_success.connect
def task_success_handler(result, **kwargs):
    del result  # unused
    task = kwargs['sender']
    task_id = task.request.id
    Task.objects.filter(id=task_id).update(state=TaskState.SUCCESS)
    TaskRun.objects.filter(task_id=task_id, retry=task.request.retries).update(ended_at=timezone.now())


@task_failure.connect
def task_failure_handler(task_id, exception, args, traceback, einfo, **kwargs):
    del exception, args, traceback  # unused
    task = kwargs['sender']
    Task.objects.filter(id=task_id).update(state=TaskState.FAILURE)
    TaskRun.objects.filter(task_id=task_id, retry=task.request.retries).update(ended_at=timezone.now(), traceback=einfo)


@task_retry.connect
def task_retry_handler(request, reason, einfo, **kwargs):
    del request, reason  # unused
    task = kwargs['sender']
    task_id = task.request.id
    Task.objects.filter(id=task_id).update(state=TaskState.RETRY)
    TaskRun.objects.filter(task_id=task_id, retry=task.request.retries).update(ended_at=timezone.now(), traceback=einfo)
