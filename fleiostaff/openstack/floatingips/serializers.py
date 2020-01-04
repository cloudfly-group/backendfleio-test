from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from fleio.core.clients.serializers import ClientMinSerializer
from fleio.core.models import Client
from fleio.openstack.models import FloatingIp
from fleio.openstack.models import Network
from fleio.openstack.models import Port
from fleio.openstack.models import Router
from fleio.openstack.networking.serializers import FloatingIpSerializer


class FloatingNetworkMinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Network
        fields = ('id', 'name', 'region')


class PortMinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Port
        fields = ('id', 'name')


class RouterMinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Router
        fields = ('id', 'name')


class StaffFloatingIpSerializer(FloatingIpSerializer):
    client = ClientMinSerializer(source='project.service.client', read_only=True, default=None)
    floating_network = FloatingNetworkMinSerializer(read_only=True)
    port = PortMinSerializer(read_only=True)
    router = RouterMinSerializer(read_only=True)


class StaffFloatingIpCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FloatingIp
        exclude = ('router', 'port')
        read_only_fields = (
            'id', 'status', 'project', 'floating_ip_address', 'fixed_ip_address')

    client = serializers.IntegerField(required=False)
    description = serializers.CharField(required=True)

    def validate_client(self, client):
        if not client:
            raise serializers.ValidationError('Client is required.')
        return client

    def to_internal_value(self, data):
        """
        Perform any data modification here.
        to_internal_value is called before .validate() and after each field is validated.
        """
        value = super(StaffFloatingIpCreateSerializer, self).to_internal_value(data)

        request = self.context.get('request', None)
        assert request, 'Serializer can only be used with http requests.'

        client_id = data['client']
        client = Client.objects.filter(id=client_id).first()
        if not client:
            raise ValidationError({'detail': _('Unable to find a client for the current user.')})
        project = client.first_project
        if not project:
            raise ValidationError({'detail': _('Cannot create floating ip without a project.')})
        value['project'] = project

        return value
