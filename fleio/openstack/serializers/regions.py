from rest_framework import serializers

from fleio.openstack.models import OpenstackRegion


class RegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = OpenstackRegion
        fields = ('id', 'description', 'enabled', 'enable_volumes', 'enable_snapshots', )


class RegionBriefSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)

    class Meta:
        model = OpenstackRegion
        fields = ('id',)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
