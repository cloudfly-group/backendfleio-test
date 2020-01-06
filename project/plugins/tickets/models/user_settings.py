from django.db import models

from fleio import settings


class UserSettings(models.Model):
    notify_on_ticket_open = models.BooleanField(default=False, blank=True)
    notify_on_ticket_close = models.BooleanField(default=False, blank=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
