import logging

from rest_framework import serializers

from fleio.core.clients.serializers import ClientMinSerializer
from fleio.openstack import models
from fleio.openstack.models import Volume, VolumeBackup

LOG = logging.getLogger(__name__)


class VolumeBackupSyncSerializer(serializers.ModelSerializer):
    sync_version = serializers.IntegerField(default=0)
    project_id = serializers.CharField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = models.VolumeBackup
        fields = '__all__'


class VolumeBackupSerializer(serializers.ModelSerializer):
    related_volume_name = serializers.SerializerMethodField(read_only=True)
    client = ClientMinSerializer(source='project.service.client', read_only=True, default=None)

    class Meta:
        model = VolumeBackup
        exclude = ('project', 'sync_version',)

    @staticmethod
    def get_related_volume_name(model):
        try:
            related_volume = model.volume
        except Volume.DoesNotExist:
            return None
        if related_volume:
            return related_volume.name
        return None


class VolumeBackupCreateSerializer(serializers.ModelSerializer):
    volume_id = serializers.CharField(allow_null=False, allow_blank=False, write_only=True, required=True)
    incremental = serializers.BooleanField(default=False)
    force = serializers.BooleanField(default=False)

    class Meta:
        model = VolumeBackup
        fields = ('name', 'description', 'volume_id', 'incremental', 'force')


class VolumeBackupRestoreSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    name = serializers.CharField(allow_blank=True, allow_null=True, required=False, max_length=255)
    volume_id = serializers.CharField(allow_null=True, allow_blank=True, required=False, max_length=36)

    class Meta:
        fields = '__all__'


class VolumeBackupUpdateSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    name = serializers.CharField(allow_blank=True, allow_null=True, required=False, max_length=255)
    description = serializers.CharField(allow_null=True, allow_blank=True, required=False, max_length=255)

    class Meta:
        fields = '__all__'
