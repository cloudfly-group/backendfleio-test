from fleio.core.plugins.plugin_ui_component import PluginUIComponent


class TicketsCreate(PluginUIComponent):
    required_services = ['tickets', 'ticketattachments', ]
