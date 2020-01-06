from typing import Optional

from django.conf import settings

from fleio.celery import app

from fleio.core.models import AppUser
from fleio.core.utils import fleio_parse_url

from fleio.notifications import notifier

from plugins.tickets.common.notification_types import NotificationType
from plugins.tickets.exceptions import NoRecipientsException
from plugins.tickets.models import Ticket


def get_ticket_department_email(ticket: Ticket):
    return ticket.department.email if ticket and ticket.department and ticket.department.email else None


def get_ticket_url(ticket_id: str, is_staff: bool) -> Optional[str]:
    frontend_url = getattr(settings, 'FRONTEND_URL', None)
    staff_url_path = getattr(settings, 'STAFF_FRONTEND_URL_ENDPOINT', None)
    if frontend_url:
        if is_staff:
            if staff_url_path:
                staff_url = fleio_parse_url(frontend_url) + settings.STAFF_FRONTEND_URL_ENDPOINT
                if staff_url[-1:] != '/':
                    return "{}/tickets/{}".format(staff_url, ticket_id)
                else:
                    return "{}tickets/{}".format(staff_url, ticket_id)
        else:
            return "{}tickets/{}".format(fleio_parse_url(frontend_url), ticket_id)
    return None


@app.task(
    bind=True,
    max_retries=settings.TASK_RETRIES,
    name='Notify all staff members on ticket',
    resource_type='Ticket',
)
def notify_all_staff_members(self, ticket_id: str, notification_type: str, reply_text=None, update_created_by=None,
                             ticket_created_by=None):
    del self  # unused
    ticket = Ticket.objects.get(id=ticket_id)  # type: Ticket

    # get email details
    staff_users = AppUser.objects.filter(is_staff=True).all()
    staff_emails = [staff_user.email for staff_user in staff_users]
    ticket_department_email = get_ticket_department_email(ticket)

    # compose ticket url
    ticket_url = get_ticket_url(ticket_id=ticket_id, is_staff=True)

    notification_name = None
    variables = None
    if notification_type == NotificationType.opened:
        notification_name = 'ticket.staff.opened'
        variables = {
            'ticket_id': ticket.id,
            'ticket_title': ticket.title,
            'ticket_body': ticket.description,
            'ticket_url': ticket_url,
            'ticket_created_by': ticket_created_by,
        }
    elif notification_type == NotificationType.reply and update_created_by:
        notification_name = 'ticket.staff.reply'
        variables = {
            'ticket_id': ticket.id,
            'ticket_title': ticket.title,
            'ticket_update_owner': update_created_by,
            'ticket_update_body': reply_text,
            'ticket_url': ticket_url,
        }

    if not variables or not notification_name:
        return
    if len(staff_emails) > 0:
        for staff_email in staff_emails:
            notifier.send(
                client=None,
                name=notification_name,
                priority=notifier.Notification.PRIORITY_NORMAL,
                variables=variables,
                to_emails=[staff_email],
                sender_address=ticket_department_email,
            )


@app.task(
    bind=True,
    max_retries=settings.TASK_RETRIES,
    name='Notify ticket participants',
    resource_type='Ticket',
)
def notify_ticket_participants_on_enduser_reply(self, ticket_id: str, except_email: str,
                                                reply_text=None, update_created_by=None):
    """
    Sends notifications to participants(ticket related end users and to cc recipients)
    on enduser reply to ticket
    """
    del self  # unused
    ticket = Ticket.objects.get(id=ticket_id)

    ticket_department_email = get_ticket_department_email(ticket)
    to_emails = list()

    if ticket.created_by and ticket.created_by.is_staff is False:
        # send to ticket owner only if he is an enduser
        to_emails.append(ticket.created_by.email)
    elif ticket.created_by and ticket.created_by.is_staff is True and ticket.client:
        # send to ticket client if the ticket was opened by a staff user for the client
        if ticket.client.email:
            to_emails.append(ticket.client.email)
    elif ticket.email_message and ticket.email_message.sender_address:
        to_emails.append(ticket.email_message.sender_address)

    if ticket.cc_recipients:
        if ',' in ticket.cc_recipients:
            cc = ticket.cc_recipients.split(',')
            for recipient in cc:
                to_emails.append(recipient)
        else:
            to_emails.append(ticket.cc_recipients)

    ticket_url = get_ticket_url(ticket_id=ticket_id, is_staff=False)

    # send notification to each participant except reply owner
    if len(to_emails) > 0:
        for email in to_emails:
            if email != except_email:
                notifier.send(
                    client=None,
                    name='ticket.enduser.reply',
                    priority=notifier.Notification.PRIORITY_NORMAL,
                    variables={
                        'ticket_id': ticket.id,
                        'ticket_title': ticket.title,
                        'ticket_update_owner': update_created_by,
                        'ticket_update_body': reply_text,
                        'ticket_url': ticket_url,
                    },
                    to_emails=[email],
                    sender_address=ticket_department_email,
                )


@app.task(
    bind=True,
    max_retries=settings.TASK_RETRIES,
    name='Notify owner on ticket changes',
    resource_type='Ticket',
)
def notify_ticket_owner(self, ticket_id: str, notification_type: str, reply_text=None, update_created_by=None,
                        notify_cc_recipients: bool = False, ticket_created_by=None):
    """Notifications to end users only"""
    del self  # unused
    ticket = Ticket.objects.get(id=ticket_id)

    ticket_department_email = get_ticket_department_email(ticket)
    to_emails = None
    if ticket.created_by and ticket.created_by.is_staff is False:
        # if enduser created ticket send notification to him
        to_emails = [ticket.created_by.email]
    elif ticket.created_by and ticket.created_by.is_staff is True and ticket.client:
        # if a staff user created the ticket and chose a client send the notification to the client's related user
        # TODO: handle case when there will be multiple users related to a client
        if ticket.client.email:
            related_user = ticket.client.users.first()
            if related_user.email:
                to_emails = [related_user.email]
            else:
                raise NoRecipientsException('No ticket owner address found for ticket {}'.format(ticket_id))
    elif ticket.email_message and ticket.email_message.sender_address:
        # if ticket has no created_by (thus was generated from an email) send the notification to the email that
        # generated it
        to_emails = [ticket.email_message.sender_address]
    else:
        raise NoRecipientsException('No ticket owner address found for ticket {}'.format(ticket_id))

    if notify_cc_recipients is True and ticket.cc_recipients:
        # set cc recipients
        if ',' in ticket.cc_recipients:
            cc = ticket.cc_recipients.split(',')
        else:
            cc = [ticket.cc_recipients]
    else:
        cc = None

    auto_replied = False
    variables = None
    notification_name = None

    # compose ticket url
    ticket_url = get_ticket_url(ticket_id=ticket_id, is_staff=False)

    if notification_type == NotificationType.opened:
        notification_name = 'ticket.enduser.opened'
        if ticket.email_message:
            # ticket was generated from email, mark the notification email as auto-replied
            auto_replied = True
        variables = {
            'ticket_id': ticket.id,
            'ticket_title': ticket.title,
            'ticket_body': ticket.description,
            'ticket_url': ticket_url,
            'ticket_created_by': ticket_created_by,
        }
    elif notification_type == NotificationType.closed:
        notification_name = 'ticket.enduser.closed'
        variables = {
            'ticket_id': ticket.id,
            'ticket_title': ticket.title,
            'ticket_url': ticket_url,
        }
    elif notification_type == NotificationType.reply and update_created_by:
        notification_name = 'ticket.enduser.reply'
        variables = {
            'ticket_id': ticket.id,
            'ticket_title': ticket.title,
            'ticket_update_owner': update_created_by,
            'ticket_update_body': reply_text,
            'ticket_url': ticket_url,
        }

    if not variables or not notification_name:
        return
    notifier.send(
        client=None,
        name=notification_name,
        priority=notifier.Notification.PRIORITY_NORMAL,
        variables=variables,
        to_emails=to_emails,
        cc=cc,
        sender_address=ticket_department_email,
        auto_replied=auto_replied,
    )
