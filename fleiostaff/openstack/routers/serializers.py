from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from fleio.core.models import Client
from fleio.openstack.models import Port, Router, Subnet


class RouterInterfaceSerializer(serializers.ModelSerializer):
    fixed_ips = serializers.JSONField()

    class Meta:
        model = Port
        fields = ('id', 'network_name', 'fixed_ips', 'admin_state_up', )


class StaffRouterSerializer(serializers.ModelSerializer):
    routes = serializers.JSONField(required=False)
    availability_zones = serializers.JSONField(required=False)
    availability_hints = serializers.JSONField(required=False)
    external_fixed_ips = serializers.JSONField(required=False)
    network_name = serializers.ReadOnlyField()

    class Meta:
        model = Router
        exclude = ('sync_version',)
        read_only_fields = ('permissions',)


class StaffRouterDetailSerializer(StaffRouterSerializer):
    interfaces = serializers.SerializerMethodField()

    def get_interfaces(self, router):
        return RouterInterfaceSerializer(
            instance=Port.objects.filter(
                device_id=router.id,
                device_owner=getattr(settings, 'ROUTER_PORT_DEVICE_OWNER', 'network:router_interface'),
            ),
            many=True,
        ).data


class StaffRouterCreateSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)

    class Meta:
        model = Router
        fields = ('id', 'name', 'description', 'external_network_id', 'admin_state_up', 'client', 'region')

    client = serializers.IntegerField(required=False)

    def to_internal_value(self, data):
        """
        Perform any data modification here.
        to_internal_value is called before .validate() and after each field is validated.
        """
        value = super(StaffRouterCreateSerializer, self).to_internal_value(data)

        request = self.context.get('request', None)
        assert request, 'Serializer can only be used with http requests.'

        if 'client' in data:
            client_id = data['client']
            client = Client.objects.filter(id=client_id).first()
            if not client:
                raise ValidationError({'detail': _('Client not found.')})
            project = client.first_project
            if not project:
                raise ValidationError({'detail': _('Client has no project.')})
            value['project'] = project

        return value


class StaffRouterUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Router
        fields = ('name', 'description', 'external_network_id', 'admin_state_up',)
        read_only_fields = ('id', 'region',)


class SubnetInterfaceSerializer(serializers.ModelSerializer):
    network_name = serializers.CharField(source='network.name')

    class Meta:
        model = Subnet
        fields = ('id', 'name', 'network_name', 'cidr')
