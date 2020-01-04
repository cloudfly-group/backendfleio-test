from django.db import models
from django.conf import settings
from django.utils import timezone


class Department(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=32, blank=False, unique=True)
    email = models.EmailField(max_length=127, unique=True)
    ticket_id_format = models.CharField(
        max_length=64, blank=False, null=False, default=getattr(settings, 'TICKET_ID_DEFAULT_FORMAT')
    )
    notification_on_ticket_open_to_staff = models.BooleanField()
    notification_on_staff_user_reply_to_staff = models.BooleanField()
    notification_on_user_reply_to_staff = models.BooleanField(default=False, blank=True)
    notification_to_user_on_ticket_opened = models.BooleanField(default=False, blank=True)
    notification_to_user_on_ticket_closed = models.BooleanField(default=False, blank=True)
    notification_on_staff_user_reply_to_user = models.BooleanField(default=False, blank=True)
    notify_cc_recipients_on_ticket_open = models.BooleanField(default=False, blank=True)
    notify_cc_recipients_on_ticket_close = models.BooleanField(default=False, blank=True)
    notify_cc_recipients_on_ticket_reply = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.name


class DepartmentNotificationsMap:
    DEFAULT_VALUE = False
    NOTIFICATIONS = {
        'notification_on_ticket_open_to_staff': DEFAULT_VALUE,
        'notification_on_staff_user_reply_to_staff': DEFAULT_VALUE,
        'notification_on_user_reply_to_staff': DEFAULT_VALUE,
        'notification_to_user_on_ticket_opened': DEFAULT_VALUE,
        'notification_to_user_on_ticket_closed': DEFAULT_VALUE,
        'notification_on_staff_user_reply_to_user': DEFAULT_VALUE,
        'notify_cc_recipients_on_ticket_open': DEFAULT_VALUE,
        'notify_cc_recipients_on_ticket_close': DEFAULT_VALUE,
        'notify_cc_recipients_on_ticket_reply': DEFAULT_VALUE,
    }
