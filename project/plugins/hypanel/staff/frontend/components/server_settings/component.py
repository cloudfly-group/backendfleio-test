import logging

from rest_framework import serializers

from fleio.conf.utils import fernet_encrypt
from fleio.conf.utils import fernet_decrypt

from fleio.core.plugins.plugin_ui_component import PluginUIComponent

LOG = logging.getLogger(__name__)


class HypanelPasswordSerializer(serializers.CharField):
    def to_internal_value(self, data):
        if data:
            try:
                data = fernet_encrypt(data)
            except Exception as e:
                LOG.exception(e)
                data = None
        return super(HypanelPasswordSerializer, self).to_internal_value(data)

    def to_representation(self, value):
        if value:
            try:
                value = fernet_decrypt(value)
            except Exception as e:
                LOG.exception(e)
                value = None
        return super(HypanelPasswordSerializer, self).to_representation(value)


class ServerSettingsSerializer(serializers.Serializer):
    url = serializers.CharField(max_length=255, allow_null=False)
    username = serializers.CharField(max_length=255, allow_null=False)
    password = HypanelPasswordSerializer(max_length=1024, allow_null=True)

    def create(self, validated_data):
        return validated_data

    def update(self, instance, validated_data):
        return validated_data


class ServerSettings(PluginUIComponent):
    server_settings_serializer = ServerSettingsSerializer
