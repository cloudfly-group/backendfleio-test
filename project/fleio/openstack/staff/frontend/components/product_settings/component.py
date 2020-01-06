from fleio.billing.models import Product
from fleio.core.plugins.plugin_ui_component import PluginUIComponent

from fleio.openstack.models import OpenstackProductSettings
from .serializer import OpenStackProductSettingsSerializer


class ProductSettings(PluginUIComponent):
    model_manager = OpenstackProductSettings.objects
    parent_obj_name = 'product'
    parent_obj_type = Product
    reverse_relation_name = 'openstack_product_settings'
    serializer_class = OpenStackProductSettingsSerializer
