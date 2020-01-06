import logging
import threading
from typing import Optional

from ipware.ip import get_ip
from rest_framework.request import Request

from django.utils.translation import ugettext_lazy as _

from fleio.activitylog.formatting import logclass_text
from fleio.activitylog.models import Log
from fleio.activitylog.models import LogCategory
from fleio.activitylog.models import LogClass
from fleio.activitylog.operations import fetch_log_category
from fleio.core.features import active_features
from fleio.core.models import AppUser

LOG = logging.getLogger(__name__)

logclass_text['unknown activity'] = _('Unknown activity')


class ActivityHelper:
    def __init__(self):
        self.thread_local = threading.local()

    def has_current_activity(self):
        return getattr(self.thread_local, 'current_activity', None) is not None

    def set_current_activity(self, activity_id):
        self.thread_local.current_activity = Log.objects.filter(id=activity_id).first()

    def get_current_activity_log(self) -> Optional[Log]:
        current_activity = getattr(self.thread_local, 'current_activity', None)
        if not current_activity:
            LOG.warning(
                'Get current activity log called, but no activity is currently started, starting unknown activity.',
            )
            self.start_generic_activity(
                category_name='activity log',
                activity_class='unknown activity',
            )
            current_activity = getattr(self.thread_local, 'current_activity', None)

        return current_activity

    def get_current_activity_log_id(self) -> Optional[int]:
        current_activity = self.get_current_activity_log()
        return current_activity.id if current_activity else None

    def start_view_activity(
            self, activity_category: LogCategory, activity_class: str, request: Request, object_id=None
    ):
        # do not record visitors IP in demo mode
        ip = None if active_features.is_enabled('demo') else get_ip(request)
        user = request.user
        if not isinstance(user, AppUser):
            user = None

        parameters = {}

        if user:
            parameters['username'] = user.username
            parameters['user_id'] = user.id

        impersonator = getattr(request, 'impersonator', None)
        if impersonator:
            parameters['impersonator'] = impersonator.username
            parameters['impersonator_id'] = impersonator.id

        if object_id is not None:
            parameters['object_id'] = object_id

        info_log_class, _ = LogClass.objects.get_or_create(
            category=activity_category, name=activity_class, type='info',
        )

        self.thread_local.current_activity = Log.objects.create(
            user=user, ip=ip, log_class=info_log_class, parameters=parameters,
        )

    def start_generic_activity(self, category_name: str, activity_class: str, **parameters):
        activity_category = fetch_log_category(category_name)
        info_log_class, _ = LogClass.objects.get_or_create(
            category=activity_category, name=activity_class, type='info',
        )

        self.thread_local.current_activity = Log.objects.create(
            log_class=info_log_class, parameters=parameters,
        )

    def add_current_activity_params(self, **extra_parameters):
        if self.thread_local.current_activity:
            self.thread_local.current_activity.parameters.update(extra_parameters)
            self.thread_local.current_activity.save()

    @staticmethod
    def add_activity_params(activity_id, **extra_parameters):
        activity = Log.objects.filter(id=activity_id).first()
        if activity:
            activity.parameters.update(extra_parameters)
            activity.save()

    def end_activity(self, failed: bool = False):
        if failed:
            current_log = self.get_current_activity_log()  # type: Log
            error_log_class, _ = LogClass.objects.get_or_create(
                category=current_log.log_class.category, name=current_log.log_class.name, type='error',
            )
            current_log.log_class = error_log_class
            current_log.save()

        del self.thread_local.current_activity


activity_helper = ActivityHelper()
