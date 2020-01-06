from fleio.openstack.models import Hypervisor
from rest_framework import serializers


class HypervisorsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Hypervisor
