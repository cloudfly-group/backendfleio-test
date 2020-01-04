from rest_framework import serializers

from fleio.core.models import Plugin


class EnduserPluginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plugin
        fields = '__all__'
