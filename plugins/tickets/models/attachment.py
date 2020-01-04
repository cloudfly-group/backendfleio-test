from django.db import models

from fleio.core.utils import RandomId

from plugins.tickets.models.email_message import EmailMessage
from plugins.tickets.models.ticket import Ticket
from plugins.tickets.models.ticket_update import TicketUpdate
from plugins.tickets.models.ticket_note import TicketNote

from plugins.tickets.common.attachments_storage import AttachmentsStorage


class Attachment(models.Model):
    id = models.BigIntegerField(unique=True, default=RandomId('tickets.Attachment'), primary_key=True)
    file_name = models.CharField(max_length=256, default=None, null=True, blank=True)
    disk_file = models.CharField(max_length=256, default=None, null=True, blank=True)
    content_type = models.CharField(max_length=128, default=None, null=True, blank=True)
    email_message = models.ForeignKey(
        EmailMessage,
        on_delete=models.CASCADE,
        related_name='attachments',
        null=True,
        blank=True,
    )
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name='attachments',
        null=True,
        blank=True,
    )
    ticket_update = models.ForeignKey(
        TicketUpdate,
        on_delete=models.CASCADE,
        related_name='attachments',
        null=True,
        blank=True,
    )
    ticket_note = models.ForeignKey(
        TicketNote,
        on_delete=models.CASCADE,
        related_name='attachments',
        null=True,
        blank=True,
    )

    objects = models.Manager

    def delete(self, using=None, keep_parents=False):
        attachment_storage = AttachmentsStorage.get_attachments_storage()
        attachment_storage.remove_attachment_from_disk(disk_file=self.disk_file)
        return super(Attachment, self).delete(using, keep_parents)
