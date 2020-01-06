from rest_framework import serializers

from fleio.openstack.models import OpenstackProductSettings


class OpenStackProductSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpenstackProductSettings
        fields = '__all__'
