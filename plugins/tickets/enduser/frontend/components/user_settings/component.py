from fleio.core.models import AppUser
from fleio.core.plugins.plugin_ui_component import PluginUIComponent

from .serializer import TicketsUserSettingsSerializer


class UserSettings(PluginUIComponent):
    disabled = True  # this is not needed for now
    parent_obj_name = 'user'
    parent_obj_type = AppUser
    reverse_relation_name = 'tickets_user_settings'
    serializer_class = TicketsUserSettingsSerializer
