from rest_framework import serializers

from fleio.openstack.models import Project


class StaffProjectSerializers(serializers.ModelSerializer):
    services_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = (
            'project_id',
            'service',
            'services_count',
        )
