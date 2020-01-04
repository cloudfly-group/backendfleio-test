from django.apps import apps

from fleio.core.plugins.frontent_view_base import FrontendViewBase
from fleio.core.plugins.plugin_definition import PluginConfigTypes


class UserFrontendView(FrontendViewBase):
    plugin_label = apps.get_containing_app_config(__name__).label
    config_type = PluginConfigTypes.enduser
