from rest_framework import serializers

from fleio.openstack.models import OpenstackInstanceFlavor
from fleio.openstack.models import FlavorGroup


class AdminFlavorGroupSerializer(serializers.ModelSerializer):
    flavor_count = serializers.SerializerMethodField()

    class Meta:
        model = FlavorGroup
        fields = '__all__'

    @staticmethod
    def get_flavor_count(flavor_group):
        return OpenstackInstanceFlavor.objects.filter(flavor_group=flavor_group).count()


class AdminFlavorGroupMinSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlavorGroup
        fields = (
            'name',
        )
