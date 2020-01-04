from fleio.core.models import AppUser
from django.db.models import Q
from fleio.core.plugins.plugin_ui_component import PluginUIComponent

from plugins.tickets.models import Ticket
from plugins.tickets.models.ticket import TicketStatus


class PluginNotifications(PluginUIComponent):
    required_services = ['tickets']

    @staticmethod
    def get_notification_count(user: AppUser) -> int:
        user_clients = user.clients.all()
        params = Q(client__in=user_clients) | Q(created_by=user)
        qs = Ticket.objects.filter(params)
        qs = qs.exclude(status=TicketStatus.done)
        return qs.count()
