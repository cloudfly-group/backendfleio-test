from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from fleio.core.models import Client
from fleio.openstack.models import Network, Project
from fleio.openstack.networking.serializers import NetworkSerializerExtra, SubnetMinSerializer
from fleiostaff.openstack.subnets.serializers import StaffSubnetCreateSerializer


class StaffNetworkSerializerExtra(NetworkSerializerExtra):
    client_id = serializers.SerializerMethodField()
    client_full_name = serializers.SerializerMethodField()
    subnets = serializers.SerializerMethodField()

    class Meta:
        model = Network
        exclude = ('sync_version',)

    @staticmethod
    def get_subnets(network):
        return SubnetMinSerializer(instance=network.subnet_set.all(), many=True).data

    @staticmethod
    def get_client_id(network):
        project = Project.objects.filter(project_id=network.project).first()
        if project and project.service:
            return project.service.client.id
        else:
            return None

    @staticmethod
    def get_client_full_name(network):
        project = Project.objects.filter(project_id=network.project).first()
        if project and project.service:
            client = project.service.client
            return '{0} {1}'.format(client.first_name, client.last_name)
        else:
            return _('n/a')

    def get_allowed_actions(self, network):
        return []


class StaffNetworkCreateSerializer(serializers.ModelSerializer):
    subnet = StaffSubnetCreateSerializer(required=False)
    id = serializers.CharField(read_only=True)
    provider_network_type = serializers.CharField(required=False)
    provider_physical_network = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    provider_segmentation_id = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = Network
        fields = '__all__'
        read_only_fields = ('project', 'created_at', 'updated_at', 'status', 'extra')

    client = serializers.IntegerField(required=False)

    def to_internal_value(self, data):
        """
        Perform any data modification here.
        to_internal_value is called before .validate() and after each field is validated.
        """
        value = super(StaffNetworkCreateSerializer, self).to_internal_value(data)

        request = self.context.get('request', None)
        assert request, 'Serializer can only be used with http requests.'

        if 'provider_segmentation_id' in value and value['provider_segmentation_id']:
            try:
                int(value['provider_segmentation_id'])
            except (TypeError, ValueError):
                raise ValidationError({'detail': _('provider_segmentation_id must be a number')})
        if 'client' in data:
            client_id = data['client']
            client = Client.objects.filter(id=client_id).first()
            if not client:
                raise ValidationError({'detail': _('No client found.')})
            project = client.first_project
            if not project:
                raise ValidationError({'detail': _('Client has no project.')})
            value['project'] = project

        return value


class StaffNetworkUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Network
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'status', 'extra', 'region',)


class StaffNetworkAutoCreateSerializer(serializers.Serializer):
    region = serializers.CharField(required=False)
    client = serializers.IntegerField(required=False)

    def validate_client(self, client):
        if not client:
            raise serializers.ValidationError(_('Client is required.'))
        return client

    def to_internal_value(self, data):
        """
        Perform any data modification here.
        to_internal_value is called before .validate() and after each field is validated.
        """
        value = super(StaffNetworkAutoCreateSerializer, self).to_internal_value(data)

        request = self.context.get('request', None)
        assert request, 'Serializer can only be used with http requests.'

        client = data['client']
        if not client:
            raise ValidationError({'detail': _('Unable to find a client for the current user.')})
        project = client.first_project
        if not project:
            raise ValidationError({'detail': _('Cannot create a network without a project.')})
        value['project'] = project

        return value
