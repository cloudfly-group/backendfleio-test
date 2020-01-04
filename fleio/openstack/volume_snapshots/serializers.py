from rest_framework import serializers

from fleio.core.clients.serializers import ClientMinSerializer
from fleio.openstack import models


class VolumeSnapshotSyncSerializer(serializers.ModelSerializer):
    sync_version = serializers.IntegerField(default=0)
    project_id = serializers.CharField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = models.VolumeSnapshot
        fields = '__all__'


class VolumeSnapshotSerializer(serializers.ModelSerializer):
    related_volume_name = serializers.SerializerMethodField(read_only=True)
    client = ClientMinSerializer(source='project.service.client', read_only=True, default=None)

    class Meta:
        model = models.VolumeSnapshot
        exclude = ('project', 'sync_version',)

    @staticmethod
    def get_related_volume_name(model):
        try:
            related_volume = model.volume
        except models.Volume.DoesNotExist:
            return None
        if related_volume:
            return related_volume.name
        return None


class VolumeSnapshotCreateSerializer(serializers.ModelSerializer):
    volume_id = serializers.CharField(allow_null=False, allow_blank=False, write_only=True, required=True)
    force = serializers.BooleanField(default=False)

    class Meta:
        model = models.VolumeSnapshot
        fields = ('name', 'description', 'volume_id', 'force')


class VolumeSnapshotUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VolumeSnapshot
        fields = ('name', 'description')
