from fleio.billing.models import Product
from fleio.core.plugins.plugin_ui_component import PluginUIComponent

from plugins.cpanelserver.models import CpanelServerProductSettings
from .serializer import CpanelServerProductSettingsSerializer


class ProductSettings(PluginUIComponent):
    model_manager = CpanelServerProductSettings.objects
    parent_obj_name = 'product'
    parent_obj_type = Product
    reverse_relation_name = 'cpanelserver_product_settings'
    serializer_class = CpanelServerProductSettingsSerializer
