import copy
import logging
import os

from celery import Celery
# noinspection PyProtectedMember
from celery import Task

from django.conf import settings

from fleio.activitylog.utils.functions import current_activity_id
from fleio.activitylog.utils.functions import end_current_activity
from fleio.activitylog.utils.functions import set_current_activity_if_none

from fleio.base_settings import TASK_LOG_DIR

CURRENT_TASK_ID = None
LOG = logging.getLogger(__name__)
ENABLE_TASK_LOGGING = True


class FleioTask(Task):
    abstract = True

    def __init__(self):
        self.typing = False

    def run(self, *args, **kwargs):
        pass

    def delay(self, *args, **kwargs):
        global CURRENT_TASK_ID
        return super().delay(
            *args, **kwargs, parent_task_id=CURRENT_TASK_ID,
            activity_log_id=current_activity_id(),
        )

    def si(self, *args, **kwargs):
        global CURRENT_TASK_ID
        return super().si(
            *args, **kwargs, parent_task_id=CURRENT_TASK_ID,
            activity_log_id=current_activity_id(),
        )

    def s(self, *args, **kwargs):
        global CURRENT_TASK_ID
        return super().s(
            *args, **kwargs, parent_task_id=CURRENT_TASK_ID,
            activity_log_id=current_activity_id(),
        )

    def __call__(self, *args, **kwargs):
        if not self.request.id:
            # we do not have task id, this happens when task is invoked directly
            # we do not log anything here at the moment since this is just a normal function call
            return super().__call__(*args, **kwargs)

        global CURRENT_TASK_ID
        old_task_id = CURRENT_TASK_ID
        CURRENT_TASK_ID = self.request.id

        task_kwargs = copy.deepcopy(kwargs)

        if 'parent_task_id' in task_kwargs:
            self.parent_task_id = task_kwargs.pop('parent_task_id')
        else:
            LOG.error('Parent task id is not present in task parameters !!!')

        must_end_activity = False
        if 'activity_log_id' in task_kwargs:
            self.activity_log_id = task_kwargs.pop('activity_log_id')
            must_end_activity = set_current_activity_if_none(activity_id=self.activity_log_id)

        if ENABLE_TASK_LOGGING:
            # set custom log handler to capture task logs
            formatter = logging.Formatter('[%(asctime)s][%(levelname)s] %(message)s')
            task_handler = logging.FileHandler(os.path.join(settings.TASK_LOG_DIR, CURRENT_TASK_ID + '.log'))
            task_handler.setFormatter(formatter)
            task_handler.setLevel(logging.DEBUG)
            logging.root.addHandler(task_handler)

        try:
            # actual task execution
            task_result = super().__call__(*args, **task_kwargs)
        finally:
            if ENABLE_TASK_LOGGING:
                # remove log handler
                # noinspection PyUnboundLocalVariable
                logging.root.removeHandler(task_handler)
                task_handler.flush()
                task_handler.close()

            if must_end_activity:
                end_current_activity(activity_id=self.activity_log_id)

            CURRENT_TASK_ID = old_task_id

        return task_result


class FleioCelery(Celery):
    task_cls = FleioTask


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fleio.settings')

try:
    if not os.path.isdir(TASK_LOG_DIR):
        parent_dir = os.path.dirname(TASK_LOG_DIR)
        parent_stat = os.stat(parent_dir)

        os.mkdir(TASK_LOG_DIR, 0o755)
        stats = os.stat(TASK_LOG_DIR)
        if stats.st_uid != parent_stat.st_uid:
            os.chown(TASK_LOG_DIR, parent_stat.st_uid, parent_stat.st_gid)
except Exception as e:
    del e  # unused
    LOG.exception('Failed to create tasklog directory, disabling task logging')
    ENABLE_TASK_LOGGING = False


app = FleioCelery('fleio')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))  # noqa
