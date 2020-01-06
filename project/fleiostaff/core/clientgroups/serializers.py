from rest_framework import serializers

from fleio.core.models import Client
from fleio.core.models import ClientGroup


class ClientGroupSerializer(serializers.ModelSerializer):
    client_count = serializers.SerializerMethodField()

    class Meta:
        model = ClientGroup
        fields = '__all__'

    @staticmethod
    def get_client_count(client_group):
        return Client.objects.filter(groups=client_group).count()


class ClientGroupsMinSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientGroup
        fields = ('id', 'name')
        read_only_fields = ('id',)


class ClientGroupDetailsSerializer(serializers.ModelSerializer):
    client_count = serializers.SerializerMethodField()

    class Meta:
        model = ClientGroup
        fields = '__all__'

    @staticmethod
    def get_client_count(client_group):
        return Client.objects.filter(groups=client_group).count()
