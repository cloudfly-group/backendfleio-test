from fleio.openstack.models.hypervisors import Hypervisor

from rest_framework import serializers


class HypervisorSyncSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hypervisor
        fields = '__all__'
