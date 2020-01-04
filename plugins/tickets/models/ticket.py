import bleach

from typing import Optional, Tuple

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from fleio.core.exceptions import APIBadRequest
from fleio.core.models import AppUser
from fleio.core.models import Client
from fleio.billing.models.service import Service

from fleio.utils.model import dict_to_choices

from plugins.tickets.exceptions import TicketException
from plugins.tickets.models.email_message import EmailMessage
from plugins.tickets.models.utils.ticket_id import generate_ticket_id, validate_ticket_id
from plugins.tickets.models.department import Department


class TicketStatus(object):
    open = 'open'
    customer_reply = 'customer reply'
    answered = 'answered'
    in_progress = 'in progress'
    on_hold = 'on hold'
    done = 'done'

    status_map = {
        open: _('Open'),
        customer_reply: _('Customer Reply'),
        answered: _('Answered'),
        in_progress: _('In Progress'),
        on_hold: _('On Hold'),
        done: _('Done')
    }

    internal_status_map = {
        open: _('Open'),
        in_progress: _('In Progress'),
        on_hold: _('On Hold'),
        done: _('Done')
    }

    @classmethod
    def get_choices(cls):
        return dict_to_choices(cls.status_map)

    @classmethod
    def get_internal_choices(cls):
        return dict_to_choices(cls.internal_status_map)


class TicketPriority(object):
    high = 'high'
    medium = 'medium'
    low = 'low'

    priority_map = {
        high: _('High'),
        medium: _('Medium'),
        low: _('Low')
    }

    @classmethod
    def get_choices(cls):
        return dict_to_choices(cls.priority_map)


class TicketManager(models.Manager):
    def add_ticket(self,
                   title: str,
                   description: str,
                   client: Client = None,
                   department: Department = None,
                   priority: str = TicketPriority.medium,
                   status: str = TicketStatus.open,
                   internal_status: Optional[str] = None,
                   assigned_to: AppUser = None,
                   created_by: AppUser = None,
                   cc_recipients: str = None,
                   email_message: object = None):
        return self.create(
            title=title,
            description=description,
            client=client,
            department=department,
            priority=priority,
            status=status,
            internal_status=internal_status,
            assigned_to=assigned_to,
            created_by=created_by,
            cc_recipients=cc_recipients,
            email_message=email_message
        )


class Ticket(models.Model):
    id = models.CharField(max_length=64, unique=True, default=1, primary_key=True)
    created_at = models.DateTimeField(default=timezone.now)
    last_reply_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(AppUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    assigned_to = models.ForeignKey(AppUser, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=1024)
    description = models.CharField(max_length=10240)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, null=True)
    priority = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    internal_status = models.CharField(max_length=100, null=True, blank=True, default=None)
    cc_recipients = models.CharField(max_length=1024, null=True, blank=True)
    email_message = models.OneToOneField(EmailMessage, on_delete=models.CASCADE, null=True, blank=True, default=None)
    linked_tickets = models.ManyToManyField("self", blank=True, through='TicketLink', symmetrical=False)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, blank=True, null=True)

    objects = TicketManager()

    @staticmethod
    def find_available_id_by_department_format(department_id) -> Tuple[bool, str]:
        """
        try maximum 10 times to find IDs for ticket based on the department format, returning the first available one
        :param department_id: the id of the department where the format is defined in the "ticket_id_format" attribute
        :return: tuple containing bool representing success or failure and string representing message error or
        the available ticket ID
        """
        number_of_retries = 0
        while True:
            if number_of_retries > 9:
                return False, _('Max retries exceeded for finding an available ticket id using the format defined in '
                                'the department')
            try:
                department = Department.objects.get(id=department_id)
            except Department.DoesNotExist:
                return False, _('No department found when trying to create ticket')
            ticket_id = generate_ticket_id(department.ticket_id_format)
            try:
                Ticket.objects.get(id=ticket_id)
                number_of_retries += 1
            except Ticket.DoesNotExist:
                return True, ticket_id

    def save(self, *args, **kwargs):
        try:
            Ticket.objects.get(id=self.id)
            if self.description:
                self.description = bleach.clean(self.description, strip=True)
            return super().save(*args, **kwargs)
        except Ticket.DoesNotExist:
            # generate ticket id based on the format from department
            department_id = self.department_id
            try:
                available_id = self.find_available_id_by_department_format(
                    department_id=department_id
                )  # type: Tuple[bool, str]
                if available_id[0] is True:
                    self.id = available_id[1]
                else:
                    # if ticket id generation based on department format fails, retry using the default format
                    default_format = getattr(settings, 'TICKET_ID_DEFAULT_FORMAT', '%n%n%n%n%n%n')
                    result, message = validate_ticket_id(id_format=default_format)  # type: Tuple[bool, str]
                    if result is True:
                        while True:
                            ticket_id = generate_ticket_id(default_format)  # type: str
                            try:
                                Ticket.objects.get(id=ticket_id)
                            except Ticket.DoesNotExist:
                                self.id = ticket_id
                                break
                    else:
                        raise APIBadRequest(
                            _('Ticket ID format defined in settings file is invalid. {}').format(message)
                        )
            except TicketException as e:
                raise e

        if self.description:
            self.description = bleach.clean(self.description, strip=True)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Tickets'

    def __str__(self):
        return '{} - {}'.format(self.title, self.status)


class TicketLink(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='first_ticket')
    linked_ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='second_ticket')

    class Meta:
        unique_together = ('ticket', 'linked_ticket')
        verbose_name_plural = 'Ticket links'

    def __str__(self):
        return 'Link of ticket {} to {}'.format(self.linked_ticket, self.ticket)
