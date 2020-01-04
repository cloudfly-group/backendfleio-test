from rest_framework import serializers

from plugins.hypanel.models import HypanelProductSettings


class HypanelProductSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HypanelProductSettings
        fields = '__all__'
