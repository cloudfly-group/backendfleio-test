import celery
import logging

from typing import Dict, List, Optional

from django.core import exceptions as django_exceptions
from django.conf import settings
from django.db import transaction
from django.utils.module_loading import import_string

from fleio.celery import app
from fleio.core.features import staff_active_features
from fleio.core.models import AppUser
from fleio.notifications.models import Notification, NotificationTemplate
from fleio.notifications.utils import reset_current_notification


LOG = logging.getLogger('cron')

DISPATCHERS = ['frontend', 'email']
DISPATCHERS_PATH = 'fleio.notifications.dispatcher.{}.Dispatcher'


class Notifier(object):
    def __init__(self, client, name, sender_address: str = None, to_emails: Optional[List] = None, priority=None,
                 user=None, cc: Optional[List] = None, variables=None, auto_replied: bool = False,
                 attachments_builder=None, attachments_builder_args=None, is_current: bool = False):
        """
        :param client:
        :param name:
        :param sender_address: who sends the notification (optional if client is used)
        :param to_emails: where should the notification go (optional if client is used)
        :param priority:
        :param user:
        :param variables: used to interpolate the template text
        :param auto_replied: boolean that marks the Auto-Submitted header of the email as auto-replied
        """
        self.client = client
        self.name = name
        self.priority = priority or Notification.PRIORITY_LOW
        self.user = user
        self.variables = variables
        self.is_current = is_current
        self.sender_address = sender_address
        self.to_emails = to_emails
        self.cc = cc
        self.auto_replied = auto_replied
        self.attachments_builder = attachments_builder
        self.attachments_builder_args = attachments_builder_args

    def is_disabled(self):
        notification_template = NotificationTemplate.objects.filter(name=self.name).first()
        if notification_template:
            return notification_template.disable_notification
        else:
            return True

    def send(self):
        if self.client:
            log_msg = 'Sending {} notification for client: {} with project_id: {}, priority: {}'
            project = self.client.first_project

            if project:
                project = project.project_id

            LOG.info(log_msg.format(self.name, self.client, project, self.priority))
        elif self.to_emails:
            LOG.info('Sending {} notification to {}'.format(self.name, self.to_emails))
        if self.is_current:
            # if it is a new current notification remove the flag from the last one if exists
            reset_current_notification(client=self.client, notification_name=self.name, priority=self.priority)
        notification = Notification.objects.create(
            client=self.client,
            user=self.user,
            name=self.name,
            variables=self.variables,
            priority=self.priority,
            is_current=self.is_current,
        )
        send_task_group = list()
        for dispatcher in DISPATCHERS:
            send_task_group.append(send_as_task.s(
                notification.id,
                dispatcher=dispatcher,
                to_emails=self.to_emails,
                cc=self.cc,
                sender_address=self.sender_address,
                auto_replied=self.auto_replied,
                attachments_builder=self.attachments_builder,
                attachments_builder_args=self.attachments_builder_args,
            ))
        transaction.on_commit(lambda: celery.group(send_task_group).apply_async())
        return send_task_group

    def already_notified(self, time_frame=None, is_current_verification: bool = False):
        if is_current_verification:
            return Notification.objects.already_has_a_current_notification(
                client=self.client,
                name=self.name,
                priority=self.priority,
            )
        return Notification.objects.already_sent_this_month_or_time_frame(
            client=self.client,
            name=self.name,
            priority=self.priority,
            time_frame=time_frame,
        )


def send(name, priority=Notification.PRIORITY_LOW,
         client=None,
         user=None,
         sender_address: str = None, to_emails: Optional[List] = None,
         cc: Optional[List] = None,
         variables=None,
         is_current: bool = False,
         check_if_already_notified: bool = False,
         time_frame=None,
         is_current_verification: bool = False,
         auto_replied: bool = False,
         attachments_builder=None,
         attachments_builder_args=None):
    """

    :param client: based on this we'll get from_field and to_emails params for the send_email method; if None is used,
    sender_address and to_emails need to be specified
    :param sender_address: who sends the notification (optional if client is used)
    :param to_emails: where should the notification go (optional if client is used)
    :param cc: cc recipients of email
    :param name:
    :param user: the user the notification is related to for language matching (optional if client is used)
    :param priority:
    :param variables:
    :param is_current: set the is_current field to True or False on the notification in order to later use the
    "is_current_verification" in order not to send a notification of some type more than once
    :param check_if_already_notified: whether to check or not if the notification was already sent so it won't
    send again
    :param time_frame: use this to specify from what date to check if a notification was already sent
    :param is_current_verification: if True, doesn't send notification if last notification of same type has
    "is_current" field set to True
    :param auto_replied: boolean that marks the Auto-Submitted header of the email as auto-replied
    :param attachments_builder: string that represents the path to a method that returns an attachment/list of
    attachments
    :param attachments_builder_args: arguments (dictionary) that will get passed to the method define in the
    attachments_builder parameter
    :return:
    """
    notification = Notifier(
        client=client,
        name=name,
        user=user,
        priority=priority,
        variables=variables,
        is_current=is_current,
        sender_address=sender_address,
        cc=cc,
        to_emails=to_emails,
        auto_replied=auto_replied,
        attachments_builder=attachments_builder,
        attachments_builder_args=attachments_builder_args,
    )

    if notification.is_disabled():
        LOG.info('Notification {} is disabled and will not be sent'.format(name))
        return

    if user or client:
        if not user:
            user = client.users.first()
        notifications_settings = getattr(user, 'notifications_settings', None)
        if notifications_settings and not notifications_settings.is_notification_enabled(name):
            LOG.info('Notification {} is disabled for user {} and will not be sent'.format(name, user))
            return

    already_notified = False
    if check_if_already_notified:
        already_notified = notification.already_notified(
            time_frame=time_frame, is_current_verification=is_current_verification
        )
    if not already_notified:
        notification.send()
    else:
        LOG.info('Not sending {} notification for client {} because he was already notified.'
                 .format(name, client))


def send_staff_notification(
        name: str,
        priority: str = Notification.PRIORITY_LOW,
        variables: Optional[Dict[str, str]] = None):
    if not staff_active_features.is_enabled('notifications.send'):
        LOG.info('Notification sending is disabled for staff, aborting')
        return

    if variables is None:
        variables = {}
    for staff_user in AppUser.objects.filter(is_staff=True):
        send(
            name=name,
            priority=priority,
            user=staff_user,
            variables=variables,
        )


def low(client, name, variables, check_if_already_notified: bool = False, time_frame=None):
    send(name, client=client, priority=Notification.PRIORITY_LOW, variables=variables,
         check_if_already_notified=check_if_already_notified, time_frame=time_frame)


def normal(client, name, variables, check_if_already_notified: bool = False, time_frame=None):
    send(name, client=client, priority=Notification.PRIORITY_NORMAL, variables=variables,
         check_if_already_notified=check_if_already_notified, time_frame=time_frame)


def high(client, name, variables, check_if_already_notified: bool = False, time_frame=None):
    send(name, client=client, priority=Notification.PRIORITY_HIGH, variables=variables,
         check_if_already_notified=check_if_already_notified, time_frame=time_frame)


def critical(client, name, variables, check_if_already_notified: bool = False, time_frame=None):
    send(name, client=client, priority=Notification.PRIORITY_CRITICAL, variables=variables,
         check_if_already_notified=check_if_already_notified, time_frame=time_frame)


@app.task(bind=True, max_retries=settings.TASK_RETRIES, autoretry_for=(Exception, ),
          name='Send notification', resource_type='Notification')
def send_as_task(self, notification_id, dispatcher, to_emails: Optional[List] = None, sender_address: str = None,
                 cc: Optional[List] = None, auto_replied: bool = False, attachments_builder=None,
                 attachments_builder_args=None):
    del self  # unused
    try:
        dispatcher_class = import_string(DISPATCHERS_PATH.format(dispatcher))
        params = dict()
        attachments = None
        if attachments_builder:
            try:
                attachments_builder = import_string(attachments_builder)
            except ImportError:
                pass
            else:
                attachments_builder_result = attachments_builder(**attachments_builder_args)
                if isinstance(attachments_builder_result, list):
                    attachments = attachments_builder_result
                else:
                    attachments = [attachments_builder_result]

        if dispatcher == 'email':
            params = dict(
                to_emails=to_emails,
                cc=cc,
                sender_address=sender_address,
                auto_replied=auto_replied,
                attachments=attachments if attachments else None,
            )
        dispatcher_class().send(notification_id, **params)
    except django_exceptions.ImproperlyConfigured as e:
        LOG.error(e)
    except ImportError as e:
        LOG.error(e)
