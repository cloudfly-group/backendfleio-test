from rest_framework import serializers
from fleio.openstack.models import VolumeSnapshot


class StaffVolumeSnapshotCreateSerializer(serializers.ModelSerializer):
    volume_id = serializers.CharField(allow_null=False, allow_blank=False, write_only=True, required=True)
    force = serializers.BooleanField(default=False)
    for_client = serializers.BooleanField(default=False)

    class Meta:
        model = VolumeSnapshot
        fields = ('name', 'description', 'volume_id', 'force', 'for_client',)
