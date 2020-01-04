import logging

from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from fleio.openstack.models import Network, Project, Subnet

LOG = logging.getLogger(__name__)


class StaffSubnetSerializer(serializers.ModelSerializer):
    extra = serializers.JSONField(required=False)
    client_id = serializers.SerializerMethodField()
    client_full_name = serializers.SerializerMethodField()

    class Meta:
        model = Subnet
        exclude = ('sync_version',)

    def get_client_id(self, subnet):
        project = Project.objects.filter(project_id=subnet.project_id).first()
        if project and project.service:
            return project.service.client.id
        else:
            return None

    def get_client_full_name(self, subnet):
        project = Project.objects.filter(project_id=subnet.project_id).first()
        if project and project.service:
            client = project.service.client
            return '{0} {1}'.format(client.first_name, client.last_name)
        else:
            return _('n/a')


class StaffSubnetCreateSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    allocation_pools = serializers.JSONField(default=list())
    cidr = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    dns_nameservers = serializers.JSONField(default=list())
    host_routes = serializers.JSONField(default=list())
    ipv6_ra_mode = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    ipv6_address_mode = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    gateway_ip = serializers.IPAddressField(required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = Subnet
        read_only_fields = ('project_id', 'created_at', 'updated_at', 'extra')
        exclude = ('network',)

    def validate_allocation_pools(self, allocation_pools):
        if allocation_pools:
            for allocation_pool in list(allocation_pools):
                if not ('start' in allocation_pool and 'end' in allocation_pool):
                    raise serializers.ValidationError(
                        _('Format: [{"start":"ip1", "end":"ip2"}, {"start":"ip3", "end":"ip4"}] is required'))
                else:
                    if not allocation_pool['start'] and not allocation_pool['end']:
                        allocation_pools.remove(allocation_pool)

        return allocation_pools

    def validate_dns_nameservers(self, dns_nameservers):
        if dns_nameservers:
            for dns_nameserver in list(dns_nameservers):
                if 'ip' not in dns_nameserver:
                    raise serializers.ValidationError(
                        _('Format: [{"ip":"ip1"}, {"ip":"ip2"}] is required'))
                else:
                    if not dns_nameserver['ip']:
                        dns_nameservers.remove(dns_nameserver)

        return dns_nameservers

    def validate_host_routes(self, host_routes):
        if host_routes:
            for host_route in list(host_routes):
                if not ('destination' in host_route and 'nexthop' in host_route):
                    raise serializers.ValidationError(
                        _('Format: [{"destination":"CIDR1", "nexthop":"IP1"}, '
                          '{"destination":"CIDR2", "nexthop":"IP2"}] is required'))
                else:
                    if not host_route['destination'] and not host_route['nexthop']:
                        host_routes.remove(host_route)

        return host_routes

    def to_internal_value(self, data):
        """
        Perform any data modification here.
        to_internal_value is called before .validate() and after each field is validated.
        """
        # if 'allocation_pools' in data and not data['allocation_pools']:
        #     data.pop('allocation_pools')
        value = super(StaffSubnetCreateSerializer, self).to_internal_value(data)

        request = self.context.get('request', None)
        assert request, 'Serializer can only be used with http requests.'

        if '' == value.get('gateway_ip', None):
            value['gateway_ip'] = None

        if 'prefixlen' in data:
            value['prefixlen'] = data['prefixlen']
        if ('subnetpool_id' in value and not value['subnetpool_id']) or 'subnetpool_id' not in value:
            if ('cidr' in value and not value['cidr']) or 'cidr' not in value:
                raise ValidationError({'detail': _('Either cidr or a subnetpool must be specified')})
        if 'subnetpool_id' in value and value['subnetpool_id']:
            if value['allocation_pools']:
                raise ValidationError({'detail': _('Allocation_pools allowed only for specific subnet requests')})
        if 'dns_nameservers' in value:
            dns_nameservers_copy = list(value['dns_nameservers'])
            value['dns_nameservers'] = list()
            for dns_nameserver in dns_nameservers_copy:
                value['dns_nameservers'].append(dns_nameserver['ip'])

        if 'network_id' in data:
            network = Network.objects.filter(id=data['network_id']).first()
            if not network:
                raise ValidationError({'detail': _('Unable to find the network.')})
            value['network'] = network
            try:
                value['project'] = Project.objects.get(project_id=network.project)
            except Project.DoesNotExist:
                LOG.error('Project {} not found'.format(network.project))
                pass

        return value


class StaffSubnetUpdateSerializer(serializers.ModelSerializer):
    dns_nameservers = serializers.JSONField(default=list())
    host_routes = serializers.JSONField(default=list())
    gateway_ip = serializers.IPAddressField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = Subnet
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'extra', 'project_id',
                            'network_id', 'subnetpool_id', 'cidr', 'ip_version')

    allocation_pools = serializers.JSONField(default=list())

    def validate_allocation_pools(self, allocation_pools):
        if allocation_pools:
            for allocation_pool in allocation_pools:
                if not ('start' in allocation_pool and 'end' in allocation_pool):
                    raise serializers.ValidationError(
                        _('Format: [{"start":"ip1", "end":"ip2"}, {"start":"ip3", "end":"ip4"}] is required'))
        return allocation_pools

    @staticmethod
    def validate_dns_nameservers(dns_nameservers):
        if dns_nameservers:
            for dns_nameserver in list(dns_nameservers):
                if 'ip' not in dns_nameserver:
                    raise serializers.ValidationError(
                        _('Format: [{"ip":"ip1"}, {"ip":"ip2"}] is required'))
                else:
                    if not dns_nameserver['ip']:
                        dns_nameservers.remove(dns_nameserver)

        return dns_nameservers

    @staticmethod
    def validate_host_routes(host_routes):
        if host_routes:
            for host_route in list(host_routes):
                if not ('destination' in host_route and 'nexthop' in host_route):
                    raise serializers.ValidationError(
                        _('Format: [{"destination":"CIDR1", "nexthop":"IP1"}, '
                          '{"destination":"CIDR2", "nexthop":"IP2"}] is required'))
                else:
                    if not host_route['destination'] and not host_route['nexthop']:
                        host_routes.remove(host_route)

        return host_routes

    def to_internal_value(self, data):
        """
        Perform any data modification here.
        to_internal_value is called before .validate() and after each field is validated.
        """
        # if 'allocation_pools' in data and not data['allocation_pools']:
        #     data.pop('allocation_pools')
        value = super(StaffSubnetUpdateSerializer, self).to_internal_value(data)

        request = self.context.get('request', None)
        assert request, 'Serializer can only be used with http requests.'

        if 'dns_nameservers' in value:
            dns_nameservers_copy = list(value['dns_nameservers'])
            value['dns_nameservers'] = list()
            for dns_nameserver in dns_nameservers_copy:
                value['dns_nameservers'].append(dns_nameserver['ip'])

        if 'gateway_ip' in value:
            if value['gateway_ip'] == '':
                value['gateway_ip'] = None

        return value
