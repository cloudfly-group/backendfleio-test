from fleio.billing.models import Product
from fleio.core.plugins.plugin_ui_component import PluginUIComponent

from plugins.hypanel.models import HypanelProductSettings
from .serializer import HypanelProductSettingsSerializer


class ProductSettings(PluginUIComponent):
    model_manager = HypanelProductSettings.objects
    parent_obj_name = 'product'
    parent_obj_type = Product
    reverse_relation_name = 'hypanel_product_settings'
    serializer_class = HypanelProductSettingsSerializer
