from fleio.core.plugins.plugin_ui_component import PluginUIComponent


class RegisterDomain(PluginUIComponent):
    required_services = [
        'contacts',
        'orderdomain',
    ]
