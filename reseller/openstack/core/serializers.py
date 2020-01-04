from rest_framework import serializers

from fleio.openstack.models import Project


class ResellerProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('created_at', 'deleted', 'description', 'extras', 'fleio_disabled_reason',
                  'id', 'is_domain', 'name', 'project_domain_id', 'project_id', 'service', 'updated_at')


class ResellerOpenstackProjectSerializer(serializers.Serializer):
    description = serializers.CharField()
    domain_id = serializers.CharField()
    enabled = serializers.BooleanField()
    id = serializers.CharField()
    is_domain = serializers.BooleanField()
    name = serializers.CharField()


class ResellerOpenstackProjectBriefSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    name = serializers.ReadOnlyField()
    project_id = serializers.ReadOnlyField()


# TODO: move this in staff billing
class ResellerCreateServiceSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    product_cycle_id = serializers.IntegerField()
    create_new_project = serializers.BooleanField()
    service_external_id = serializers.CharField(max_length=36, required=False)
    project_id = serializers.CharField(max_length=36, required=False)


# TODO: move this in staff billing
class ResellerDeleteServiceSerializer(serializers.Serializer):
    service_id = serializers.IntegerField()
