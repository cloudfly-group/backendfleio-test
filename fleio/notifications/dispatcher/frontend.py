from __future__ import unicode_literals

from fleio.notifications.models import Notification
from .base import DispatcherBase


class Dispatcher(DispatcherBase):
    def __init__(self):
        super(Dispatcher, self).__init__()
        self.dispatcher_name = 'frontend'

    def send(self, notification_id, *args, **kwargs):
        notification = Notification.objects.get(id=notification_id)
        notification.dispatchers_log.create(name=self.dispatcher_name)


frontend_dispatcher = Dispatcher()
