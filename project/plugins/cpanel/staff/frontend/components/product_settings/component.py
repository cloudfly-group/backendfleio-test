from fleio.billing.models import Product

from fleio.core.plugins.plugin_ui_component import PluginUIComponent

from plugins.cpanel.models import CpanelProductSettings
from .serializer import CpanelProductSettingsSerializer


class ProductSettings(PluginUIComponent):
    model_manager = CpanelProductSettings.objects
    parent_obj_name = 'product'
    parent_obj_type = Product
    reverse_relation_name = 'cpanel_product_settings'
    serializer_class = CpanelProductSettingsSerializer
