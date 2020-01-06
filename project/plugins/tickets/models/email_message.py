import bleach

from django.db import models


class EmailMessage(models.Model):
    message_id = models.CharField(max_length=256, default=None, null=True, blank=True)
    sender_address = models.CharField(max_length=256)
    to = models.CharField(max_length=256)
    cc = models.CharField(max_length=1024, null=True, blank=True)
    subject = models.CharField(max_length=1024, default=None, null=True, blank=True)
    body = models.CharField(max_length=10240)

    def save(self, *args, **kwargs):
        if self.subject:
            self.subject = bleach.clean(self.subject, strip=True)
        if self.body:
            self.body = bleach.clean(self.body, strip=True)
        super().save(*args, **kwargs)
