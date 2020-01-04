from __future__ import unicode_literals

import smtplib
import socket

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text
from typing import List, Optional  # noqa

from fleio.core.utils import get_default_configuration_field_value
from fleio.emailing import send_email
from fleio.notifications.models import Notification
from .base import DispatcherBase


class Dispatcher(DispatcherBase):
    def __init__(self):
        super(Dispatcher, self).__init__()
        self.dispatcher_name = 'email'

    def send(self, notification_id, *args, **kwargs):
        to_emails = kwargs.get('to_emails', None)  # type: Optional[List]
        sender_address = kwargs.get('sender_address', None)  # type: Optional[str]
        cc = kwargs.get('cc', None)  # type: Optional[List]
        attachments = kwargs.get('attachments', None)
        auto_replied = kwargs.get('auto_replied', False)  # type: bool
        notification = Notification.objects.get(id=notification_id)
        title, message = self.get_title_and_message(notification)
        dlog = notification.dispatchers_log.create(name=self.dispatcher_name)

        # get sender email address
        # NOTE: if sender_email is None Django uses it's DEFAULT_FROM_EMAIL setting
        if notification.client:
            sender_email = notification.client.billing_settings.sender_email
        elif sender_address:
            sender_email = sender_address
        else:
            sender_email = get_default_configuration_field_value(field_name='sender_email')
        if not sender_email:
            sender_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None)
        # get sender name
        if notification.client:
            sender_name = notification.client.billing_settings.sender_name
        else:
            # get sender name from default configuration
            sender_name = get_default_configuration_field_value(field_name='sender_name')

        # Format from field as either Name <addr@dom> or just addr@dom
        if sender_name and sender_email:
            from_field = '{} <{}>'.format(sender_name, sender_email)
        else:
            from_field = sender_email

        to_field = list()
        if to_emails:
            to_field = to_emails
        try:
            client_email = notification.client.email if notification.client else None
            if client_email:
                to_field.append(client_email)
        except ObjectDoesNotExist:
            if len(to_field) < 1:
                dlog.set_status(dlog.ERROR, _('{} does not have an e-mail address').format(notification.client.name))
                return
            else:
                pass
        try:
            send_email(
                from_field=from_field,
                to_emails=to_field,
                subject_template=title,
                body_template=message,
                params=dict(),
                cc=cc,
                is_html=True,
                auto_replied=auto_replied,
                attachments=attachments,
            )
        except smtplib.SMTPRecipientsRefused as e:
            dlog.set_status(dlog.ERROR, e.recipients)
        except smtplib.SMTPResponseException as e:
            dlog.set_status(dlog.ERROR, _('Code: {code} Message: {error}').format(code=e.smtp_code, error=e.smtp_error))
        except smtplib.SMTPException as e:
            dlog.set_status(dlog.ERROR, _('Unable to send email: {error}').format(error=force_text(e)))
        except socket.error as e:
            dlog.set_status(dlog.ERROR, _('Unable to send email: {error}').format(error=force_text(e)))
        else:
            dlog.set_status(dlog.SENT, _('Sent...'))
