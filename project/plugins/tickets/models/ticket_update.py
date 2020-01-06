import bleach

from django.db import models
from django.utils import timezone

from fleio.core.models import AppUser

from plugins.tickets.models.email_message import EmailMessage
from plugins.tickets.models.ticket import Ticket
from plugins.tickets.models.ticket import TicketStatus


class TicketUpdate(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(AppUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='updates', null=True, blank=True)
    reply_text = models.CharField(max_length=10240, null=True, blank=True)
    new_status = models.CharField(max_length=100, null=True, blank=True)
    new_department = models.CharField(max_length=100, null=True, blank=True)
    new_priority = models.CharField(max_length=100, null=True, blank=True)
    new_internal_status = models.CharField(max_length=100, null=True, blank=True)
    new_assignee = models.ForeignKey(AppUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    description_changed = models.BooleanField(default=False, blank=True)
    title_changed = models.BooleanField(default=False, blank=True)
    new_client = models.CharField(max_length=100, null=True, blank=True)
    new_cc = models.CharField(max_length=1024, null=True, blank=True)
    last_edited = models.DateTimeField(default=None, null=True, blank=True)
    last_edited_by = models.ForeignKey(AppUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    email_message = models.OneToOneField(EmailMessage, on_delete=models.CASCADE, null=True, blank=True, default=None)

    def __str__(self):
        return 'Update for {}'.format(self.ticket)

    def save(self, *args, **kwargs):
        new_status = None
        if self.reply_text:
            self.reply_text = bleach.clean(self.reply_text, strip=True)
            if self.created_by and self.created_by.is_admin:
                new_status = TicketStatus.answered
            else:
                new_status = TicketStatus.customer_reply

        if self.ticket_id:
            related_ticket = Ticket.objects.filter(id=self.ticket_id).first()  # type: Ticket
            if related_ticket:
                related_ticket.last_reply_at = self.created_at
                if new_status:
                    related_ticket.status = new_status
                related_ticket.save()

        super().save(*args, **kwargs)
