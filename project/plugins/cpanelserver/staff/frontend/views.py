from django.apps import apps

from fleio.core.drf import StaffOnly
from fleio.core.plugins.frontent_view_base import FrontendViewBase
from fleio.core.plugins.plugin_definition import PluginConfigTypes


class FrontendView(FrontendViewBase):
    permission_classes = (StaffOnly,)
    plugin_label = apps.get_containing_app_config(__name__).label
    config_type = PluginConfigTypes.staff
