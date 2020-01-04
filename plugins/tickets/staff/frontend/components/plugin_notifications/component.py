from fleio.core.models import AppUser
from django.db.models import Q
from fleio.core.plugins.plugin_ui_component import PluginUIComponent

from plugins.tickets.models import Ticket
from plugins.tickets.models.ticket import TicketStatus


class PluginNotifications(PluginUIComponent):
    required_services = ['tickets']

    @staticmethod
    def get_notification_count(user: AppUser) -> int:
        filter_param = Q(assigned_to=user) | Q(assigned_to=None)
        return Ticket.objects.filter(filter_param).exclude(internal_status=TicketStatus.done).count()
