from fleio.core.plugins.plugin_ui_component import PluginUIComponent


class RegisterDomainForm(PluginUIComponent):
    required_services = [
        'contacts',
        'orderdomain',
    ]
