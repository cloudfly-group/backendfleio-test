import logging
import ipaddress

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from fleio.core.drf import FieldsModelSerializer
from fleio.openstack import models
from fleio.openstack.models import Instance, NetworkRbac, Port, Project, Router
from fleiostaff.openstack.subnets.serializers import StaffSubnetCreateSerializer

LOG = logging.getLogger(__name__)


class ProjectMinSerializer(serializers.ModelSerializer):
    display_name = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('project_id', 'project_domain_id', 'name', 'description', 'display_name')

    @staticmethod
    def get_display_name(obj):
        return obj.name or obj.project_id


class SubnetSerializer(FieldsModelSerializer):
    class Meta:
        model = models.Subnet
        exclude = ('sync_version',)


class SubnetMinSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Subnet
        fields = ('id', 'name', 'cidr', 'ip_version', 'gateway_ip', 'project_id', 'enable_dhcp', 'extra',
                  'allocation_pools',)


class NetworkSerializer(FieldsModelSerializer):
    class Meta:
        model = models.Network
        exclude = ('extra', 'sync_version')


class NetworkTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.NetworkTag
        fields = ('tag_name',)
        read_only_fields = ('tag_name',)


class NetworkOptionsSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Network
        fields = ('id', 'name', 'tags',)

    @staticmethod
    def get_tags(model):
        qs = model.network_tags.all()
        return NetworkTagsSerializer(instance=qs, read_only=True, many=True).data


class PortSyncSerializer(serializers.ModelSerializer):
    extra = serializers.JSONField(default=dict())
    fixed_ips = serializers.JSONField(default=None)
    network_id = serializers.CharField(write_only=True, allow_blank=True, allow_null=True)
    project_id = serializers.CharField(write_only=True, allow_blank=True, allow_null=True)
    security_groups = serializers.JSONField(default=None)

    class Meta:
        model = models.Port
        fields = '__all__'
        extra_kwargs = {'id': {'validators': list()}}


class SubnetSyncSerializer(serializers.ModelSerializer):
    extra = serializers.JSONField(default=dict())
    network_id = serializers.CharField(write_only=True)
    allocation_pools = serializers.JSONField(default=list())

    class Meta:
        model = models.Subnet
        fields = '__all__'
        extra_kwargs = {'id': {'validators': list()}}


class NetworkSyncSerializer(serializers.ModelSerializer):
    extra = serializers.JSONField(default=dict())

    class Meta:
        model = models.Network
        fields = '__all__'
        extra_kwargs = {'id': {'validators': list()}}


class FloatingIpSyncSerializer(serializers.ModelSerializer):
    project_id = serializers.CharField(write_only=True, allow_blank=True, allow_null=True)
    floating_network_id = serializers.CharField(write_only=True)
    port_id = serializers.CharField(write_only=True, allow_blank=True, allow_null=True)
    router_id = serializers.CharField(write_only=True, allow_blank=True, allow_null=True)

    class Meta:
        model = models.FloatingIp
        fields = '__all__'
        extra_kwargs = {'id': {'validators': list()}}


class NetworkRbacSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.NetworkRbac
        fields = '__all__'
        extra_kwargs = {'id': {'validators': list()}}


class RouterSyncSerializer(serializers.ModelSerializer):
    availability_zones = serializers.JSONField(default=list())
    availability_hints = serializers.JSONField(default=list())
    external_fixed_ips = serializers.JSONField(default=list())
    routes = serializers.JSONField(default=list())

    class Meta:
        model = models.Router
        fields = '__all__'
        extra_kwargs = {'id': {'validators': list()}}


class SubnetPoolSyncSerializer(serializers.ModelSerializer):
    prefixes = serializers.JSONField(default=list())

    class Meta:
        model = models.SubnetPool
        fields = '__all__'
        extra_kwargs = {'id': {'validators': list()}}


class SubnetPoolSerializer(serializers.ModelSerializer):
    prefixes = serializers.JSONField(default=list())

    class Meta:
        model = models.SubnetPool
        fields = (
            'id', 'name', 'prefixes', 'default_prefixlen', 'min_prefixlen',
            'max_prefixlen', 'ip_version', 'is_default',
        )


class FloatingNetworkMinSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Network
        fields = ('id', 'name', 'description', 'region')


class PortSerializer(serializers.ModelSerializer):
    fixed_ips = serializers.JSONField()

    class Meta:
        model = models.Port
        exclude = ('sync_version', )


class PortMinSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Port
        fields = ('id', 'name')


class RouterMinSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Router
        fields = ('id', 'name')


class FloatingIpSerializer(serializers.ModelSerializer):
    floating_network = FloatingNetworkMinSerializer(read_only=True)
    port = PortMinSerializer(read_only=True)
    router = RouterMinSerializer(read_only=True)
    associated_object = serializers.SerializerMethodField()

    def get_associated_object(self, floating_ip):
        try:
            port = models.Port.objects.get(floatingip=floating_ip.id)
        except models.Port.DoesNotExist:
            return None
        except models.Port.MultipleObjectsReturned:
            LOG.error('Inconsistent database. Multiple ports with same floating ip found. Floating ip id: {}'.format(
                floating_ip.id))
            return None

        instance = models.Instance.objects.filter(id=port.device_id).first()
        if instance:
            return {'device_type': 'instance', 'id': instance.id, 'name': instance.name}
        else:
            return {'device_type': None, 'id': port.device_id, 'name': None}

    class Meta:
        model = models.FloatingIp
        read_only_fields = (
            'id', 'status', 'project', 'floating_ip_address', 'fixed_ip_address', 'port', 'router',
            'created_at', 'updated_at')
        exclude = ('revision_number', 'sync_version')


class FloatingIpCreateSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    description = serializers.CharField(required=True)

    class Meta:
        model = models.FloatingIp
        fields = ('id', 'floating_network', 'description')


class NetworkSerializerExtra(serializers.ModelSerializer):
    """
    The networks for display are filtered in the user's viewset (own networks and networks access based on rbac.
    Further filtering occurs here. If user doesn't have roles, he will have access to all information on the network,
    with all functions enabled (update, delete, add_subnet, add_router). If user has access_as_shared role, subnets
    are displayed, functions add_subnet and add_router are enabled. He cannot delete, nor modify the network, even if he
    is the owner, because it is shared. If user has access_as_external role, subnets are not displayed, only add_router
    function is enabled. If user has both access_as_external and access_as_shared role, subnets are displayed and only
    add_router function is enabled.
    """
    extra = serializers.JSONField(required=False)
    subnets = serializers.SerializerMethodField()
    allowed_actions = serializers.SerializerMethodField()

    def get_subnets(self, network):
        request = self.context.get('request', None)
        assert request, 'Serializer can only be used with http requests.'
        client = request.user.clients.filter(services__openstack_project__isnull=False).first()
        if client:
            # if user is the owner
            if client.first_project.project_id == network.project:
                subnets = SubnetMinSerializer(instance=network.subnet_set.all(), many=True).data
                for subnet in subnets:
                    subnet['has_edit_permission'] = True
                    subnet['has_delete_permission'] = True
                return subnets

            # A user can the roles access_as_external and access_as_shared simultaneously.
            rbacs = NetworkRbac.objects.filter(object_id=network.id,
                                               target_project__in=['*', client.first_project.project_id])
            external = False
            for rbac in rbacs:
                if rbac.action == 'access_as_shared':
                    subnets = SubnetMinSerializer(instance=network.subnet_set.all(), many=True).data
                    for subnet in subnets:
                        subnet['has_delete_permission'] = client.first_project.project_id == subnet['project_id']
                    return subnets
                if rbac.action == 'access_as_external':
                    external = True
            # if it is external and NOT shared
            if external:
                return None

        else:
            return None

    def get_allowed_actions(self, network):
        request = self.context.get('request', None)
        assert request, 'Serializer can only be used with http requests.'
        client = request.user.clients.filter(services__openstack_project__isnull=False).first()
        allowed = []
        if client:
            allowed = ['update', 'delete', 'add_subnet', 'add_router']
            # if user is the owner
            if client.first_project.project_id == network.project:
                return allowed

            rbacs = NetworkRbac.objects.filter(object_id=network.id,
                                               target_project__in=['*', client.first_project.project_id])
            for rbac in rbacs:
                if rbac.action == 'access_as_external':
                    # no other action is possible
                    return ['add_router']
                if rbac.action == 'access_as_shared':
                    return ['add_subnet', 'add_router']
        return allowed

    class Meta:
        model = models.Network
        exclude = ('sync_version',)


class NetworkCreateSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    subnet = StaffSubnetCreateSerializer(required=False)

    class Meta:
        model = models.Network
        fields = ('id', 'name', 'admin_state_up', 'region', 'description', 'subnet')


class NetworkUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Network
        fields = ('name', 'admin_state_up', 'description')
        read_only_fields = ('id', 'region')

    def to_internal_value(self, data):
        request = self.context.get('request', None)
        assert request, 'Serializer can only be used with http requests.'
        client = request.user.clients.filter(services__openstack_project__isnull=False).first()
        if client:
            # whatever rule the client may have it is enough to know that she cannot edit the network
            if NetworkRbac.objects.filter(object_id=self.instance.id,
                                          target_project__in=['*', client.first_project.project_id]).first():
                raise ValidationError({'detail': _("You don't have permission to update")})
        else:
            raise ValidationError({'detail': _("You don't have permission to update")})

        return super(NetworkUpdateSerializer, self).to_internal_value(data)


class NetworkAutoCreateSerializer(serializers.Serializer):
    region = serializers.CharField(required=False)


class SecurityGroupRuleSyncSerializer(serializers.ModelSerializer):
    security_group_id = serializers.CharField(write_only=True, allow_blank=True, allow_null=True)
    remote_group_id = serializers.CharField(write_only=True, allow_blank=True, allow_null=True)
    project_id = serializers.CharField(write_only=True, allow_blank=True, allow_null=True)

    class Meta:
        model = models.SecurityGroupRule
        fields = '__all__'
        extra_kwargs = {'id': {'validators': list()}}


class SecurityGroupSyncSerializer(serializers.ModelSerializer):
    project_id = serializers.CharField(write_only=True, allow_blank=True, allow_null=True)

    class Meta:
        model = models.SecurityGroup
        fields = '__all__'
        extra_kwargs = {'id': {'validators': list()}}


class RouterCreateSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)

    class Meta:
        model = models.Router
        fields = ('id', 'name', 'description', 'external_network_id', 'admin_state_up', 'region')


class RouterUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Router
        fields = ('name', 'description', 'external_network_id', 'admin_state_up')
        read_only_fields = ('id', 'region')


class SecurityGroupSerializer(serializers.ModelSerializer):
    associated_instances = serializers.SerializerMethodField()

    class Meta:
        model = models.SecurityGroup
        exclude = ('sync_version',)
        read_only_fields = ('associated_instances',)

    def get_associated_instances(self, security_group):
        device_ids = Port.objects.filter(security_groups__contains=security_group.id).values_list('device_id')
        return Instance.objects.filter(id__in=device_ids).values('id', 'name')


class SecurityGroupRuleSerializer(serializers.ModelSerializer):
    remote_group_name = serializers.SerializerMethodField()

    class Meta:
        model = models.SecurityGroupRule
        fields = ('id', 'remote_group', 'remote_group_name', 'description', 'direction', 'protocol', 'ethertype',
                  'port_range_min', 'port_range_max', 'remote_ip_prefix')

    def get_remote_group_name(self, rule):
        return rule.get_remote_group_name()


class SecurityGroupDetailSerializer(serializers.ModelSerializer):
    associated_instances = serializers.SerializerMethodField()
    security_group_rules = SecurityGroupRuleSerializer(many=True)

    class Meta:
        model = models.SecurityGroup
        read_only_fields = ('associated_instances', 'security_group_rules',)
        exclude = ('sync_version',)

    def get_associated_instances(self, security_group):
        device_ids = Port.objects.filter(security_groups__contains=security_group.id).values_list('device_id')
        instances = Instance.objects.filter(id__in=device_ids)
        return [{'id': instance.id, 'name': instance.name} for instance in instances] if instances else []


class SecurityGroupCreateSerializer(serializers.ModelSerializer):
    region = serializers.CharField(write_only=True)

    class Meta:
        model = models.SecurityGroup
        fields = ('id', 'name', 'description', 'region')
        read_only_fields = ('id',)


class SecurityGroupUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SecurityGroup
        fields = ('id', 'name', 'description')
        read_only_fields = ('id', 'region')


class SecurityGroupRuleCreateSerializer(serializers.ModelSerializer):
    security_group_id = serializers.CharField(required=True)
    remote_group_id = serializers.CharField(required=False)

    class Meta:
        model = models.SecurityGroupRule
        exclude = ('sync_version',)
        read_only_fields = ('id',)

    @staticmethod
    def validate_remote_ip_prefix(value):
        if not value:
            return None
        try:
            new_value = ipaddress.ip_network(value)
        except ValueError as e:
            LOG.debug('Invalid remote ip prefix: {}: {}'.format(value, e))
            raise serializers.ValidationError('Invalid remote IP prefix')
        return new_value

    def validate(self, attrs):
        remote_ip_prefix = attrs.get('remote_ip_prefix')
        if remote_ip_prefix:
            attrs['ethertype'] = 'IPv4' if remote_ip_prefix.version == 4 else 'IPv6'
        return super(SecurityGroupRuleCreateSerializer, self).validate(attrs)


class RouterInterfaceSerializer(serializers.ModelSerializer):
    fixed_ips = serializers.JSONField()

    class Meta:
        model = Port
        fields = ('id', 'network_name', 'fixed_ips', 'admin_state_up', )


class RouterSerializer(serializers.ModelSerializer):
    routes = serializers.JSONField(required=False)
    availability_zones = serializers.JSONField(required=False)
    availability_hints = serializers.JSONField(required=False)
    network_name = serializers.ReadOnlyField()

    class Meta:
        model = Router
        exclude = ('sync_version',)


class RouterDetailSerializer(RouterSerializer):
    interfaces = serializers.SerializerMethodField()

    def get_interfaces(self, router):
        return RouterInterfaceSerializer(
            instance=Port.objects.filter(
                device_id=router.id,
                device_owner=getattr(settings, 'ROUTER_PORT_DEVICE_OWNER', 'network:router_interface'),
                project_id=router.project_id
            ),
            many=True
        ).data
