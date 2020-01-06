import bleach

from django.db import models
from django.utils import timezone

from fleio.core.models import AppUser

from plugins.tickets.models.ticket import Ticket


class TicketNote(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(AppUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='notes', null=True, blank=True)
    note_text = models.CharField(max_length=10240, null=True, blank=True)
    last_edited = models.DateTimeField(default=None, null=True, blank=True)
    last_edited_by = models.ForeignKey(AppUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')

    def __str__(self):
        return 'Note for {}'.format(self.ticket)

    def save(self, *args, **kwargs):
        if self.note_text:
            self.note_text = bleach.clean(self.note_text, strip=True)
        super().save(*args, **kwargs)
