from typing import Dict
from typing import Optional

from rest_framework.serializers import Serializer

from fleio.core.plugins.plugin_ui_component import PluginUIComponent
from plugins.domains.enduser.serializers import RegisterDomainSerializer
from plugins.domains.enduser.serializers import TransferDomainSerializer


class OrderProduct(PluginUIComponent):
    required_services = ['contacts', 'orderproduct']

    def create_serializer(self, plugin_data: Dict, **kwargs) -> Optional[Serializer]:
        operation = plugin_data.get('operation', 'register')

        if operation == 'register':
            return RegisterDomainSerializer(data=plugin_data, **kwargs)

        if operation == 'transfer':
            return TransferDomainSerializer(data=plugin_data, **kwargs)

        return None
