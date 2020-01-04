from rest_framework import serializers

from fleio.openstack.models import OpenstackRole


class OpenstackRoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = OpenstackRole
        fields = ('id', 'name', )
