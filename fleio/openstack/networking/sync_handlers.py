from __future__ import unicode_literals

import copy

from django.db import IntegrityError

from fleio.openstack.models.network import NetworkTag
from fleio.openstack.sync.handler import BaseHandler
from fleio.openstack.networking import serializers


class NetworkSyncHandler(BaseHandler):
    serializer_class = serializers.NetworkSyncSerializer
    version_field = 'sync_version'

    def serialize(self, data, region, timestamp):
        new_data = copy.deepcopy(data)
        new_data['region'] = region
        new_data[self.version_field] = self.get_version(timestamp)
        new_data.setdefault('project', data.get('tenant_id', None))
        # Set other attributes
        new_data['router_external'] = data.get('router:external', False)
        # Set the provider attributes
        tags = new_data.get('tags')
        if tags and len(tags):
            for tag in tags:
                try:
                    NetworkTag.objects.create(tag_name=tag)
                except (Exception, IntegrityError):
                    pass
        new_data['extra'] = dict()
        for attr in ('provider:physical_network', 'provider:network_type', 'provider:segmentation_id',
                     'availability_zones'):
            if attr in data:
                new_data['extra'].setdefault(attr, data.get(attr))
        return new_data

    def create_or_update(self, data, region, timestamp):
        model_instance = super().create_or_update(data=data, region=region, timestamp=timestamp)
        if model_instance:
            tags = data.get('tags')
            if tags and len(tags):
                # remove tags that do not exist anymore on the network
                tags_to_remove = model_instance.network_tags.all().exclude(tag_name__in=tags)
                if tags_to_remove:
                    for tag in tags_to_remove:
                        model_instance.network_tags.remove(tag)
                # add already added db_tags to the network
                db_tags = NetworkTag.objects.filter(tag_name__in=tags)
                for db_network_tag in db_tags:
                    model_instance.network_tags.add(db_network_tag)


class PortSyncHandler(BaseHandler):
    serializer_class = serializers.PortSyncSerializer
    version_field = 'sync_version'

    def serialize(self, data, region, timestamp):
        new_data = copy.deepcopy(data)
        new_data[self.version_field] = self.get_version(timestamp)
        new_data.setdefault('project_id', data.get('tenant_id', None))
        new_data['extra'] = dict()
        for attr in ('allocation_pools', 'ipv6_address_mode', 'ipv6_ra_mode', 'host_routes', 'dns_nameservers',
                     'binding:vif_type'):
            if attr in data:
                new_data['extra'].setdefault(attr, data.get(attr))
        return new_data


class SubnetSyncHandler(BaseHandler):
    serializer_class = serializers.SubnetSyncSerializer
    version_field = 'sync_version'

    def serialize(self, data, region, timestamp):
        new_data = copy.deepcopy(data)
        new_data[self.version_field] = self.get_version(timestamp)
        new_data.setdefault('project_id', new_data.get('tenant_id', None))
        new_data['extra'] = dict()
        for attr in ('ipv6_address_mode', 'ipv6_ra_mode', 'host_routes', 'dns_nameservers'):
            if attr in new_data:
                new_data['extra'].setdefault(attr, new_data.get(attr))
        return new_data


class FloatingIPSyncHandler(BaseHandler):
    serializer_class = serializers.FloatingIpSyncSerializer
    version_field = 'sync_version'

    def serialize(self, data, region, timestamp):
        new_data = copy.deepcopy(data)
        new_data[self.version_field] = self.get_version(timestamp)
        new_data['project_id'] = data.get('project_id', data.get('tenant_id', None))
        return new_data


class NetworkRbacSyncHandler(BaseHandler):
    serializer_class = serializers.NetworkRbacSerializer
    version_field = 'sync_version'

    def serialize(self, data, region, timestamp):
        new_data = copy.deepcopy(data)
        new_data['project_id'] = data.get('tenant_id')
        new_data['target_project'] = data.get('target_tenant')
        new_data[self.version_field] = self.get_version(timestamp=timestamp)
        return new_data


class RouterSyncHandler(BaseHandler):
    serializer_class = serializers.RouterSyncSerializer

    def serialize(self, data, region, timestamp):
        new_data = copy.deepcopy(data)
        new_data[self.version_field] = self.get_version(timestamp)
        new_data['project_id'] = data.get('tenant_id', data.get('project_id', None))
        new_data['region'] = region
        external_gateway_info = data.get('external_gateway_info', None)
        if external_gateway_info:
            new_data['external_network_id'] = external_gateway_info.get('network_id', None)
            new_data['external_fixed_ips'] = external_gateway_info.get('external_fixed_ips', None)
            new_data['enable_snat'] = external_gateway_info.get('enable_snat', None)
        return new_data


class SubnetPoolSyncHandler(BaseHandler):
    serializer_class = serializers.SubnetPoolSyncSerializer

    def serialize(self, data, region, timestamp):
        data[self.version_field] = self.get_version(timestamp)
        data['project_id'] = data.get('tenant_id', data.get('project_id', None))
        data['region'] = region
        return data


class SecurityGroupRuleSyncHandler(BaseHandler):
    serializer_class = serializers.SecurityGroupRuleSyncSerializer

    def serialize(self, data, region, timestamp):
        new_data = copy.deepcopy(data)
        new_data[self.version_field] = self.get_version(timestamp)
        new_data['region'] = region
        new_data['project_id'] = data.get('project_id', data.get('tenant_id', None))
        return new_data


class SecurityGroupsSyncHandler(BaseHandler):
    serializer_class = serializers.SecurityGroupSyncSerializer

    def serialize(self, data, region, timestamp):
        new_data = copy.deepcopy(data)
        new_data[self.version_field] = self.get_version(timestamp)
        new_data['region'] = region
        new_data['project_id'] = data.get('project_id', data.get('tenant_id', None))
        return new_data

    def create_or_update(self, data, region, timestamp):
        # NOTE(tomo): Handle security group rules sync here too
        sec_rules = data.get('security_group_rules', list())
        if len(sec_rules):
            sg_handler = SecurityGroupRuleSyncHandler()
            for sgr in sec_rules:
                sg_handler.create_or_update(data=sgr, region=region, timestamp=timestamp)
        return super(SecurityGroupsSyncHandler, self).create_or_update(data, region, timestamp)
