from rest_framework import serializers

from plugins.cpanel.models import CpanelProductSettings


class CpanelProductSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CpanelProductSettings
        fields = '__all__'
