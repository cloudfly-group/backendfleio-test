import celery

from django.test import TestCase
from django.utils.module_loading import import_string

from fleio.core.tests.factories import ClientFactory
from fleio.notifications import notifier
from fleio.notifications.models import Category, DispatcherLog, Notification, NotificationTemplate
from fleio.notifications.notifier import DISPATCHERS_PATH


class TestNotification(TestCase):
    @classmethod
    def setUp(self):
        self.fleio_client = ClientFactory.create()
        self.dispatcher_name = 'frontend'
        notifier.DISPATCHERS = [self.dispatcher_name]
        self.notification_name = 'some.notification'
        self.notifier = notifier.Notifier(client=self.fleio_client,
                                          name=self.notification_name,
                                          priority=Notification.PRIORITY_HIGH)
        send_task_group = self.notifier.send()
        celery.group(send_task_group).apply_async()

    def test_notification_created_in_db(self):
        db_notification = Notification.objects.get(client=self.fleio_client,
                                                   name=self.notification_name,
                                                   priority=Notification.PRIORITY_HIGH)
        self.assertEqual(db_notification.name, self.notification_name)

    def test_notifier_already_notifier(self):
        self.assertEqual(self.notifier.already_notified(), True)

    def test_dispatcher_logged(self):
        db_notification = Notification.objects.get(client=self.fleio_client,
                                                   name=self.notification_name,
                                                   priority=Notification.PRIORITY_HIGH)
        dispatcher_log = DispatcherLog.objects.get(name=self.dispatcher_name, notification=db_notification)
        self.assertEqual(dispatcher_log.status, DispatcherLog.PENDING)


class TestTemplateParsing(TestCase):
    def setUp(self):
        self.client = ClientFactory.create()
        self.dispatcher_name = 'frontend'
        notifier.DISPATCHERS = [self.dispatcher_name]
        self.notification_name = 'some.notification'
        self.notifier = notifier.Notifier(client=self.client,
                                          name=self.notification_name,
                                          priority=Notification.PRIORITY_HIGH)
        self.notifier.send()

    def test_template_parsing(self):
        db_notification = Notification.objects.get(client=self.client,
                                                   name=self.notification_name,
                                                   priority=Notification.PRIORITY_HIGH)
        NotificationTemplate.objects.create(name=self.notification_name,
                                            content="{{client.first_name}}",
                                            title="{{notification.name}}",
                                            category=Category.objects.first())
        disp = import_string(DISPATCHERS_PATH.format(self.dispatcher_name))
        title, message = disp().get_title_and_message(db_notification)
        self.assertEqual(title, self.notification_name)
        self.assertEqual(message, self.client.first_name)
