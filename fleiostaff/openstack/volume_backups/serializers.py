from rest_framework import serializers

from fleio.core.clients.serializers import ClientMinSerializer
from fleio.openstack.models import VolumeBackup
from fleio.openstack.models import Volume


class StaffVolumeBackupSerializer(serializers.ModelSerializer):
    related_volume_name = serializers.SerializerMethodField(read_only=True)
    client = ClientMinSerializer(source='project.service.client', read_only=True, default=None)

    class Meta:
        model = VolumeBackup
        fields = '__all__'

    @staticmethod
    def get_related_volume_name(model):
        try:
            related_volume = model.volume
        except Volume.DoesNotExist:
            return None
        if related_volume:
            return related_volume.name
        return None


class StaffVolumeBackupCreateSerializer(serializers.ModelSerializer):
    volume_id = serializers.CharField(allow_null=False, allow_blank=False, write_only=True, required=True)
    for_client = serializers.BooleanField(default=False)
    incremental = serializers.BooleanField(default=False)
    force = serializers.BooleanField(default=False)

    class Meta:
        model = VolumeBackup
        fields = ('name', 'description', 'volume_id', 'for_client', 'incremental', 'force')
