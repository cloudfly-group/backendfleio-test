from fleio.core.models import AppUser
from plugins.tickets.common.notification_types import NotificationType
from plugins.tickets.common.tasks import notify_ticket_owner
from plugins.tickets.common.tasks import notify_all_staff_members
from plugins.tickets.common.tasks import notify_ticket_participants_on_enduser_reply

from plugins.tickets.models import Ticket, TicketUpdate
from plugins.tickets.models.ticket import TicketStatus


class TicketNotificationDispatcher:

    @staticmethod
    def get_ticket_creator(ticket: Ticket):
        ticket_created_by = None
        if ticket.created_by:
            ticket_created_by = ticket.created_by.get_full_name() or ticket.created_by.username
        elif ticket.email_message.sender_address:
            ticket_created_by = ticket.email_message.sender_address
        return ticket_created_by

    def ticket_created(self, ticket: Ticket):
        ticket_created_by = self.get_ticket_creator(ticket=ticket)
        if ticket.department.notification_on_ticket_open_to_staff:
            notify_all_staff_members.delay(
                ticket_id=ticket.id,
                notification_type=NotificationType.opened,
                ticket_created_by=ticket_created_by,
            )

        if ticket.department.notification_to_user_on_ticket_opened:
            notify_ticket_owner.delay(
                ticket_id=ticket.id,
                notification_type=NotificationType.opened,
                notify_cc_recipients=ticket.department.notify_cc_recipients_on_ticket_open,
                ticket_created_by=ticket_created_by,
            )

    def ticket_opened(self, ticket: Ticket):
        ticket_created_by = self.get_ticket_creator(ticket=ticket)
        if ticket.department.notification_on_ticket_open_to_staff:
            notify_all_staff_members.delay(
                ticket_id=ticket.id,
                notification_type=NotificationType.opened,
                ticket_created_by=ticket_created_by,
            )

        if ticket.department.notification_to_user_on_ticket_opened:
            notify_ticket_owner.delay(
                ticket_id=ticket.id,
                notification_type=NotificationType.opened,
                notify_cc_recipients=ticket.department.notify_cc_recipients_on_ticket_open,
                ticket_created_by=ticket_created_by,
            )

    @staticmethod
    def ticket_reopened(ticket: Ticket):
        if ticket.department.notification_on_ticket_open_to_staff:
            notify_all_staff_members.delay(
                ticket_id=ticket.id,
                notification_type=NotificationType.opened,
            )

        if ticket.department.notification_to_user_on_ticket_opened:
            notify_ticket_owner.delay(
                ticket_id=ticket.id,
                notification_type=NotificationType.opened,
                notify_cc_recipients=ticket.department.notify_cc_recipients_on_ticket_open,
            )

    @staticmethod
    def ticket_closed(ticket: Ticket):
        if ticket.department.notification_to_user_on_ticket_closed:
            notify_ticket_owner.delay(
                ticket_id=ticket.id,
                notification_type=NotificationType.closed,
                notify_cc_recipients=ticket.department.notify_cc_recipients_on_ticket_close,
            )

    def ticket_updated(self, ticket: Ticket):
        last_update = ticket.updates.last()

        email_sender = None
        if last_update.email_message and last_update.email_message.sender_address:
            email_sender = last_update.email_message.sender_address

        if last_update.reply_text:
            if last_update.created_by:
                self.send_notifications_on_reply_from_fleio_user(
                    ticket=ticket, update=last_update, fleio_user=last_update.created_by
                )
            elif email_sender:
                # if it was updated from email, check if the sender has a related fleio account and send notifications
                # based on it (it may be a staff member), otherwise consider notifications are received from an enduser
                fleio_user = AppUser.objects.filter(email=email_sender).first()
                if fleio_user:
                    self.send_notifications_on_reply_from_fleio_user(
                        ticket=ticket, update=last_update, fleio_user=fleio_user
                    )
                else:
                    if ticket.department.notification_on_user_reply_to_staff:
                        notify_all_staff_members.delay(
                            ticket_id=ticket.id,
                            notification_type=NotificationType.reply,
                            reply_text=last_update.reply_text,
                            update_created_by=email_sender,
                        )
                    # implicitly send notifications to participants(ticket related end users except the update owner)
                    notify_ticket_participants_on_enduser_reply.delay(
                        ticket_id=ticket.id,
                        except_email=email_sender,
                        reply_text=last_update.reply_text,
                        update_created_by=email_sender
                    )
            # send notifications to ticket participants (ticket owner and cc recipients except reply owner)

        ticket_reopened = last_update.new_internal_status and last_update.new_internal_status == TicketStatus.open
        ticket_reopened = ticket_reopened or (last_update.new_status and last_update.new_status == TicketStatus.open)

        if ticket_reopened:
            self.ticket_reopened(ticket=ticket)

        ticket_closed = last_update.new_internal_status and last_update.new_internal_status == TicketStatus.done
        ticket_closed = ticket_closed or (last_update.new_status and last_update.new_status == TicketStatus.done)
        if ticket_closed:
            self.ticket_closed(ticket=ticket)

    @staticmethod
    def send_notifications_on_reply_from_fleio_user(ticket: Ticket, update: TicketUpdate, fleio_user: AppUser):
        update_created_by = fleio_user.get_full_name() or fleio_user.username
        if ticket.department.notification_on_staff_user_reply_to_staff and fleio_user.is_staff:
            notify_all_staff_members.delay(
                ticket_id=ticket.id,
                notification_type=NotificationType.reply,
                reply_text=update.reply_text,
                update_created_by=update_created_by,
            )
        if ticket.department.notification_on_user_reply_to_staff and fleio_user.is_staff is False:
            notify_all_staff_members.delay(
                ticket_id=ticket.id,
                notification_type=NotificationType.reply,
                reply_text=update.reply_text,
                update_created_by=update_created_by,
            )
        if ticket.department.notification_on_staff_user_reply_to_user and fleio_user.is_staff:
            notify_ticket_owner.delay(
                ticket_id=ticket.id,
                notification_type=NotificationType.reply,
                reply_text=update.reply_text,
                update_created_by=update_created_by,
                notify_cc_recipients=ticket.department.notify_cc_recipients_on_ticket_reply,
            )
        if fleio_user.is_staff is False:
            # implicitly send notifications to participants(ticket related end users except the update owner)
            notify_ticket_participants_on_enduser_reply.delay(
                ticket_id=ticket.id,
                except_email=update.created_by.email,
                reply_text=update.reply_text,
                update_created_by=update_created_by
            )


ticket_notifications_dispatcher = TicketNotificationDispatcher()
