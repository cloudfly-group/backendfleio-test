from django.conf import settings
from django.db import models
from django.template import Context, Template
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now as utcnow
from jsonfield import JSONField

from fleio.core.models import AppUser
from fleio.core.models import Client


class NotificationManager(models.Manager):
    def already_sent(self, client, name, priority=None):
        if priority is None:
            priority = Notification.PRIORITY_NORMAL
        if self.filter(client=client, name=name, priority=priority).exists():
            return True
        return False

    def already_sent_this_month_or_time_frame(self, client, name, priority=None, time_frame=None) -> bool:
        priority = priority or Notification.PRIORITY_NORMAL
        if not time_frame:
            date = utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)  # first of month
        else:
            date = time_frame  # the given time_frame
        if self.filter(client=client, name=name, priority=priority, generated__gte=date).exists():
            return True
        return False

    def already_has_a_current_notification(self, client, name, priority) -> bool:
        client_last_notification = self.filter(
            client=client, name=name, priority=priority
        ).order_by('generated').last()  # gets the last sent notification of this type for the client
        if client_last_notification:
            return client_last_notification.is_current
        return False


class Notification(models.Model):
    STATUS_ACTIVE = 'active'
    STATUS_ERROR = 'error'
    STATUS_EXPIRED = 'expired'
    NOTIFICATION_STATUS = ((STATUS_ACTIVE, _('Active')),
                           (STATUS_ERROR, _('Error')),
                           (STATUS_EXPIRED, _('Expired')))
    PRIORITY_LOW = 'low'
    PRIORITY_NORMAL = 'normal'
    PRIORITY_HIGH = 'high'
    PRIORITY_CRITICAL = 'critical'
    NOTIFICATION_PRIORITIES = (
        (PRIORITY_LOW, _('Low')),
        (PRIORITY_NORMAL, _('Normal')),
        (PRIORITY_HIGH, _('High')),
        (PRIORITY_CRITICAL, _('Critical')),
    )

    generated = models.DateTimeField(auto_now_add=True, db_index=True)
    name = models.CharField(max_length=64, db_index=True)
    priority = models.CharField(choices=NOTIFICATION_PRIORITIES, default=PRIORITY_NORMAL, max_length=10, db_index=True)
    client = models.ForeignKey(Client, related_name='notifications', on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    status = models.CharField(choices=NOTIFICATION_STATUS, default=STATUS_ACTIVE, max_length=10, db_index=True)
    is_current = models.BooleanField(default=False)  # used for notifications that should not be sent more than once
    # variables to use in template rendering
    variables = JSONField(null=True, blank=True)

    objects = NotificationManager()

    class Meta:
        verbose_name_plural = 'Notifications'
        app_label = 'notifications'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=16, db_index=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class NotificationTemplateQueryset(models.QuerySet):
    def choices(self):
        return self.all().values_list('name', 'title')

    def unique_choices(self):
        qs = self.all()
        qs = qs.filter(language=getattr(settings, 'DEFAULT_NOTIFICATION_TEMPLATE_LANGUAGE_CODE'))
        qs = qs.values_list('name', 'title',)
        return qs


class NotificationTemplate(models.Model):
    # FIXME(tomo): dispatcher as string ?
    # FIXME(tomo): Write a validator that will check all installed dispatchers
    name = models.CharField(max_length=64, db_index=True)
    content = models.TextField(default='')
    title = models.CharField(max_length=255, default='')
    category = models.ForeignKey(Category, related_name='templates', on_delete=models.CASCADE)
    template_engine = models.CharField(default='django', max_length=32)
    dispatcher = models.CharField(max_length=64, default='all', db_index=True)
    language = models.CharField(max_length=5, choices=settings.LANGUAGES, blank=False, null=False, default='en')
    disable_notification = models.BooleanField(default=False, blank=False, null=False)

    objects = NotificationTemplateQueryset.as_manager()

    class Meta:
        verbose_name_plural = 'Notification templates'
        app_label = 'notifications'
        unique_together = (('name', 'dispatcher', 'language'), )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def set_dispatcher(self, dispatcher_name):
        self.dispatcher = dispatcher_name
        self.save()


class DispatcherLog(models.Model):
    PENDING = 'pending'
    SENT = 'sent'
    SEEN = 'seen'
    ERROR = 'error'
    DISPATCH_STATUS = ((PENDING, _('Pending')),
                       (SENT, _('Sent')),
                       (SEEN, _('Seen')),
                       (ERROR, _('Error')))

    generated = models.DateTimeField(auto_now_add=True, db_index=True)
    name = models.CharField(max_length=64, db_index=True)
    notification = models.ForeignKey(Notification, related_name='dispatchers_log', on_delete=models.CASCADE)
    status = models.CharField(choices=DISPATCH_STATUS, default=PENDING, max_length=10, db_index=True)
    status_detail = models.TextField(default='')

    class Meta:
        verbose_name_plural = 'Dispatchers logs'
        app_label = 'notifications'

    def set_status(self, status, status_detail):
        self.status = status
        self.status_detail = status_detail
        self.save(update_fields=['status', 'status_detail'])

    def __str__(self):
        return self.name

    @staticmethod
    def get_title(context=None):
        from fleio.notifications.dispatcher.frontend import frontend_dispatcher
        template = frontend_dispatcher.get_notification_template(notification=context['notification'])
        if template is not None:
            return Template(template.title).render(Context(context))
        return None

    @staticmethod
    def get_body(context=None):
        from fleio.notifications.dispatcher.frontend import frontend_dispatcher
        template = frontend_dispatcher.get_notification_template(notification=context['notification'])
        if template is not None:
            return Template(template.content).render(Context(context))
        return None


class UserNotificationsSettings(models.Model):
    user = models.OneToOneField(
        AppUser, related_name='notifications_settings', on_delete=models.CASCADE, null=False, blank=False,
    )
    implicitly_enabled = models.BooleanField(default=True, null=False, blank=False)

    def is_notification_enabled(self, name):
        notification_settings = self.notifications.filter(name=name).first()
        return notification_settings.enabled if notification_settings else self.implicitly_enabled

    def set_notification_enabled_flag(self, name, enabled=True):
        notification_settings = self.notifications.filter(name=name).first()
        if notification_settings:
            if not notification_settings.enabled == enabled:
                notification_settings.enabled = enabled
                notification_settings.save()
        else:
            NotificationSettings.objects.create(
                user_notification_settings=self,
                name=name,
                enabled=enabled,
            )


class NotificationSettings(models.Model):
    user_notification_settings = models.ForeignKey(
        UserNotificationsSettings, related_name='notifications', on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=64, db_index=True)
    enabled = models.BooleanField(default=True, null=False, blank=False)
