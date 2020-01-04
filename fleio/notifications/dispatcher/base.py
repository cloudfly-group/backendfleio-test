import logging

from django.template import Context, Template
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from ..models import NotificationTemplate

LOG = logging.getLogger(__name__)


class DispatcherException(Exception):
    pass


class DispatcherBase(object):
    """Base dispatcher class.
    A dispatcher handles the notifications delivery and tracking where applicable.
    Dispatchers may be enabled in the application settings module.
    """

    def __init__(self):
        self.dispatcher_name = 'base'
        self.dispatcher_description = _('Base dispatcher that doesn\'t do anything')

    def send(self, notification_id, *args, **kwargs):
        raise NotImplementedError()

    def get_title_and_message(self, notification):
        template = self.get_notification_template(notification)
        if template is not None:
            title, body = template.title, template.content
        else:
            LOG.warning('Unable to find a notification template for: %s' % notification.name)
            title, body = notification.name, notification.name

        return self.parse_template(title_template=title,
                                   message_template=body,
                                   context={'notification': notification,
                                            'client': notification.client,
                                            'user': notification.user,
                                            'variables': notification.variables}
                                   )

    def get_notification_template(self, notification):
        """Returns the NotificationTemplate for the notification.name and the current dispatcher if it exists."""

        # send the notification email using the language of the client's user
        # TODO(manu): treat the case when a client has multiple users with multiple languages
        user = None
        if notification.client:
            user = notification.client.users.all().first()
        elif notification.user:
            user = notification.user

        # get the template we want (by user language / default language / any template)
        language_code = user.language if (user and user.language) else None
        templates = self.get_templates_based_on_language_code(
            notification_name=notification.name,
            language_code=language_code
        )

        if templates.exists():
            for template in templates:
                if template.dispatcher == self.dispatcher_name:
                    return template
            return templates.first()
        else:
            return None

    def get_templates_based_on_language_code(self, notification_name: str, language_code=None, templates=None):
        """Search for the notification template in a certain language"""
        if language_code is not None:
            templates = NotificationTemplate.objects.filter(
                dispatcher__in=['all', self.dispatcher_name],
                name=notification_name,
                language=language_code
            )
        # if no template using the given language_code exists or language code is not provided,
        # search one using the default language code
        if not templates or not templates.exists():
            templates = NotificationTemplate.objects.filter(
                dispatcher__in=['all', self.dispatcher_name],
                name=notification_name,
                language=getattr(settings, 'DEFAULT_NOTIFICATION_TEMPLATE_LANGUAGE_CODE')
            )
        # if still none found, get any other template
        if not templates or not templates.exists():
            templates = NotificationTemplate.objects.filter(
                dispatcher__in=['all', self.dispatcher_name],
                name=notification_name,
            )
        return templates

    @staticmethod
    def parse_template(title_template, message_template, context):
        subject = Template(title_template).render(Context(context))
        text_body = Template(message_template).render(Context(context))
        text_body = DispatcherBase.un_escape(text_body)
        subject = DispatcherBase.un_escape(subject)
        return subject, text_body

    @staticmethod
    def un_escape(s):
        s = s.replace('&lt;', '<')
        s = s.replace('&gt;', '>')
        s = s.replace('&amp;', '&')
        s = s.replace('&quot;', '"')
        s = s.replace('&#39;', '\'')
        return s
