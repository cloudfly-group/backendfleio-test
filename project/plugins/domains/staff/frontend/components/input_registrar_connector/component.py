from fleio.core.plugins.plugin_ui_component import PluginUIComponent


class InputRegistrarConnector(PluginUIComponent):
    # noinspection SpellCheckingInspection
    required_services = ['registrarconnectors']
