from fleio.core.models import AppUser
from django.db.models import Q
from fleio.core.plugins.plugin_ui_component import PluginUIComponent

from plugins.todo.models import TODO


class PluginNotifications(PluginUIComponent):
    required_services = ['todo']

    @staticmethod
    def get_notification_count(user: AppUser) -> int:
        params = Q(assigned_to=user) | Q(assigned_to=None)
        return TODO.objects.filter(params).exclude(status='done').count()
