from rest_framework import serializers

from plugins.cpanelserver.models import CpanelServerProductSettings


class CpanelServerProductSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CpanelServerProductSettings
        fields = '__all__'
