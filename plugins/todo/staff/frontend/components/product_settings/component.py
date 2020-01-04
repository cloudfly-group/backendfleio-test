from fleio.billing.models import Product

from fleio.core.plugins.plugin_ui_component import PluginUIComponent

from plugins.todo.models import TODOProductSettings
from plugins.todo.staff.frontend.components.product_settings.serializer import TODOProductSettingsSerializer


class ProductSettings(PluginUIComponent):
    model_manager = TODOProductSettings.objects
    parent_obj_name = 'product'
    parent_obj_type = Product
    reverse_relation_name = 'todo_product_settings'
    serializer_class = TODOProductSettingsSerializer
