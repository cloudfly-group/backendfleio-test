from django.conf import settings
from django.db import models


class TicketsUserSettings(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='tickets_user_settings',
    )

    notify_on_ticket_opened = models.BooleanField(default=False, blank=False, null=False)
    notify_on_ticket_closed = models.BooleanField(default=False, blank=False, null=False)
