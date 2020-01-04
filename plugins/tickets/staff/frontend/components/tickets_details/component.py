from fleio.core.plugins.plugin_ui_component import PluginUIComponent


class TicketsDetails(PluginUIComponent):
    required_services = ['tickets', 'ticketnotes', 'ticketupdates', 'ticketattachments', 'ticketlinking']
