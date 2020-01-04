from fleio.core.plugins.plugin_ui_component import PluginUIComponent


class TldDetails(PluginUIComponent):
    required_services = ['tlds', 'registrarconnectors']
