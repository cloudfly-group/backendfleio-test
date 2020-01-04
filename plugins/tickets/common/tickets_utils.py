import logging
import re
from typing import Optional

from django.db import transaction

from fleio.core.models import AppUser

from plugins.tickets.common.ticket_notification_dispatcher import ticket_notifications_dispatcher

from plugins.tickets.models import Attachment, EmailMessage
from plugins.tickets.models import Ticket
from plugins.tickets.models.ticket import TicketStatus
from plugins.tickets.models.ticket_update import TicketUpdate
from plugins.tickets.models.department import Department
from plugins.tickets.models.utils.ticket_id import generate_ticket_id_regex

LOG = logging.getLogger(__name__)


class TicketUtils:
    @staticmethod
    def find_user(email: str) -> Optional[AppUser]:
        return AppUser.objects.filter(email=email).first()

    @staticmethod
    def find_department(emails: list) -> Optional[Department]:
        for email in emails:
            try:
                department = Department.objects.get(email=email)
                return department
            except Department.DoesNotExist:
                pass
        return None

    @staticmethod
    def check_permissions_to_update_ticket(sender_address: str, ticket: Ticket) -> bool:
        """
        Verifies if the sender email address is related in any way to the ticket that will be updated
        """
        if ticket.created_by and sender_address == ticket.created_by.email:
            return True
        elif ticket.email_message and sender_address == ticket.email_message.sender_address:
            return True
        # allow any staff user to update the ticket
        user = AppUser.objects.filter(email=sender_address).first()
        if user and user.is_staff is True:
            return True
        if ticket.cc_recipients and sender_address in ticket.cc_recipients:
            return True
        if ticket.client and sender_address == ticket.client.email:
            return True
        if ticket.department and sender_address == ticket.department.email:
            return True
        return False

    @staticmethod
    def create_or_update_ticket_from_received_email(received_email: EmailMessage):
        # check if this is related to any of fleio ticket departments
        try:
            search_department_emails = received_email.to.split(',')
        except AttributeError:
            LOG.warning('Could not parse emails from TO field')
            return None
        ticket_department = TicketUtils.find_department(emails=search_department_emails)  # type: Optional[Department]
        if not ticket_department:
            LOG.warning('Cannot create ticket as no department related email address was found in primary recipients')
            return None
        received_ticket_id = TicketUtils.extract_ticket_id(
            text=received_email.subject, id_format=ticket_department.ticket_id_format
        )
        if received_ticket_id is None:
            ticket = TicketUtils.create_ticket_from_received_email(
                received_email=received_email, ticket_department=ticket_department
            )
            if ticket is not None:
                ticket_notifications_dispatcher.ticket_created(ticket=ticket)
        else:
            ticket = Ticket.objects.filter(id=received_ticket_id).first()
            if not ticket:
                LOG.warning('Ticket {} not found in database'.format(received_ticket_id))
                return

            # check if the sender email address is related to the ticket
            allowed_to_update = TicketUtils.check_permissions_to_update_ticket(received_email.sender_address, ticket)

            if allowed_to_update is True:
                ticket, reopened = TicketUtils.update_ticket_from_received_mail(ticket, received_email)
                if reopened:
                    ticket_notifications_dispatcher.ticket_reopened(ticket=ticket)
                else:
                    ticket_notifications_dispatcher.ticket_updated(ticket=ticket)
            else:
                LOG.warning('Could not update ticket as the sender email address is not related in any way to it.')

    @staticmethod
    def create_ticket_from_received_email(received_email: EmailMessage, ticket_department: Department):
        ticket_user = TicketUtils.find_user(email=received_email.sender_address)  # type: AppUser

        with transaction.atomic():
            ticket = Ticket.objects.add_ticket(
                created_by=ticket_user,
                title=received_email.subject,
                description=received_email.body,
                client=ticket_user.clients.first() if ticket_user is not None else None,
                department=ticket_department if ticket_department is not None else None,
                cc_recipients=received_email.cc,
                email_message=received_email
            )
            received_email.attachments.update(ticket=ticket)

            return ticket

    @staticmethod
    def update_ticket_from_received_mail(ticket: Ticket, received_email: EmailMessage):
        ticket_user = TicketUtils.find_user(email=received_email.sender_address)  # type: AppUser
        new_cc_info = TicketUtils.add_new_addresses_to_cc(ticket.cc_recipients, received_email.cc)
        body = received_email.body
        with transaction.atomic():
            if not body:
                body = '<p><em>Reply with empty body generated from email.</em></p>'
            ticket_update = TicketUpdate.objects.create(
                ticket=ticket,
                created_by=ticket_user,
                reply_text=body,
                new_cc=new_cc_info['differences'],
                new_status=TicketStatus.open if ticket.status == TicketStatus.done else None,
                new_internal_status=TicketStatus.open if ticket.internal_status == TicketStatus.done else None,
                email_message=received_email
            )
            # update ticket cc recipients if there are changes
            if new_cc_info['new_cc_recipients'] is not None:
                ticket.cc_recipients = new_cc_info['new_cc_recipients']
                ticket.save()

            # reopen ticket if it was marked as done
            reopened = False
            if ticket.internal_status == TicketStatus.done or ticket.status == TicketStatus.done:
                if ticket.status == TicketStatus.done:
                    ticket.status = TicketStatus.open
                if ticket.internal_status == TicketStatus.done:
                    ticket.internal_status = TicketStatus.open
                reopened = True
                ticket.save()
            received_email.attachments.update(ticket=ticket, ticket_update=ticket_update)

            return ticket, reopened

    @staticmethod
    def extract_ticket_id(text: str, id_format: str) -> Optional[str]:
        # extracts ticket id from subject using a dynamically generated regex based on the id format defined on the
        # ticket department
        if text:
            dynamic_regex = generate_ticket_id_regex(id_format=id_format)
            match = re.findall(dynamic_regex, text)
            return match[0][2:-1] if len(match) > 0 else None
        else:
            return None

    @staticmethod
    def add_new_addresses_to_cc(previous: str, new: str) -> dict:
        if not previous:
            return {
                'differences': new,
                'new_cc_recipients': new
            }
        if not new:
            return {
                'differences': None,
                'new_cc_recipients': None
            }
        previous = previous.split(',')
        new = new.split(',')
        differences = list(set(new) - set(previous))
        if differences:
            updated_cc = previous + differences
            differences = ','.join(differences)
            updated_cc = ','.join(updated_cc)
        else:
            differences = None
            updated_cc = None
        return {
            'differences': differences,
            'new_cc_recipients': updated_cc
        }

    @staticmethod
    def remove_not_associated_attachments(attachment_ids: list):
        for attachment_id in attachment_ids:
            attachment = Attachment.objects.filter(id=attachment_id).first()
            if attachment:
                if (not attachment.ticket and not attachment.ticket_note and
                        not attachment.ticket_update and not attachment.email_message):
                    attachment.delete()
