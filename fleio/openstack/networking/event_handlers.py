from __future__ import unicode_literals
import logging
import copy

from django.conf import settings
from django.db import IntegrityError

from fleio.openstack.api.identity import IdentityAdminApi
from fleio.openstack.api.neutron import neutron_client
from neutronclient.common.exceptions import NotFound
from fleio.openstack.models import NetworkTag, Subnet
from fleio.openstack.networking.sync_handlers import PortSyncHandler
from fleio.openstack.signals.signals import port_created
from fleio.openstack.sync.handler import BaseHandler
from fleio.openstack.networking import serializers

from fleio.openstack.tasks import set_default_ptr

LOG = logging.getLogger(__name__)


class PortEventHandler(BaseHandler):
    serializer_class = serializers.PortSyncSerializer
    version_field = 'sync_version'

    def __init__(self):
        self.event_handlers = {'port.update.end': self.port_update_end,
                               'port.create.end': self.create,
                               'port.delete.end': self.delete,
                               'router.interface.create': self.create_router_interface,
                               'router.interface.delete': self.delete_router_interface}

    def port_update_end(self, data, region, timestamp):
        port = data.get('port', {})
        fixed_ips = port.get('fixed_ips', [])
        if (getattr(settings, 'PTR_DEFAULT_FORMAT', None) is not None or
                getattr(settings, 'PTR_DEFAULT_FORMAT_IPV6', None) is not None):
            set_default_ptr.delay(
                fixed_ips=fixed_ips,
                region_name=region,
                on_port_update=True,
                port_id=port.get('id', None)
            )
        return super().create_or_update(data=data, region=region, timestamp=timestamp)

    def serialize(self, data, region, timestamp):
        port = data['port']
        new_data = copy.deepcopy(port)
        new_data[self.version_field] = self.get_version(timestamp)
        new_data['project_id'] = port.get('project_id', port.get('tenant_id', None))
        new_data['extra'] = dict()
        for attr in ('allocation_pools', 'ipv6_address_mode', 'ipv6_ra_mode', 'host_routes', 'dns_nameservers',
                     'binding:vif_type'):
            if attr in port:
                new_data['extra'].setdefault(attr, port.get(attr))
        return new_data

    def create(self, data, region, timestamp):
        port = data.get('port', {})
        device_id = port.get('device_id', None)
        fixed_ips = port.get('fixed_ips', [])
        # set default PTR for newly allocated ips
        if (getattr(settings, 'PTR_DEFAULT_FORMAT', None) is not None or
                getattr(settings, 'PTR_DEFAULT_FORMAT_IPV6', None) is not None):
            set_default_ptr.delay(
                fixed_ips=fixed_ips,
                region_name=region,
            )
        if len(fixed_ips) > 0:
            ip_addresses = ','.join([allocated_ip.get('ip_address', None) for allocated_ip in fixed_ips])
        else:
            ip_addresses = None
        port_created.send(sender=__name__, port_id=port['id'], ips=ip_addresses, instance_id=device_id)
        return self.create_or_update(data=data, region=region, timestamp=timestamp)

    def create_router_interface(self, data, region, timestamp):
        try:
            port_id = data['router_interface']['port_id']
        except KeyError:
            return

        admin_session = IdentityAdminApi().session
        nc = neutron_client(api_session=admin_session, region_name=region)
        try:
            port = nc.show_port(port=port_id)['port']
            PortSyncHandler().create_or_update(data=port, region=None, timestamp=timestamp)
        except NotFound:
            pass

    def delete(self, payload, region, timestamp):
        port = payload.get('port', {})
        fixed_ips = port.get('fixed_ips', [])
        # reset PTR for de-allocated ips
        if (getattr(settings, 'PTR_DEFAULT_FORMAT', None) is not None or
                getattr(settings, 'PTR_DEFAULT_FORMAT_IPV6', None) is not None):
            set_default_ptr.delay(
                fixed_ips=fixed_ips,
                region_name=region,
            )

        obj_id = payload.get('port_id', None)
        if not obj_id:
            LOG.error('Unable to delete port without port_id: {}'.format(payload))
        return super(PortEventHandler, self).delete(obj_id, region, timestamp)

    def delete_router_interface(self, payload, region, timestamp):
        try:
            obj_id = payload['router_interface']['port_id']
        except KeyError:
            obj_id = None
            LOG.error('Unable to delete port without port_id: {}'.format(payload))
        return super(PortEventHandler, self).delete(obj_id, region, timestamp)


class NetworkEventHandler(BaseHandler):
    serializer_class = serializers.NetworkSyncSerializer
    version_field = 'sync_version'

    def __init__(self):
        self.event_handlers = {'network.delete.end': self.delete,
                               'network.create.end': self.create_or_update,
                               'network.update.end': self.create_or_update}

    def serialize(self, data, region, timestamp):
        net_payload = data['network']
        network = copy.deepcopy(net_payload)
        network['region'] = region
        network[self.version_field] = self.get_version(timestamp)
        network['project'] = net_payload.get('tenant_id', None)
        # Set other attributes
        network['router_external'] = net_payload.get('router:external', False)
        # Set the provider attributes
        network['extra'] = dict()
        for attr in ('provider:physical_network', 'provider:network_type', 'provider:segmentation_id',
                     'availability_zones'):
            if attr in net_payload:
                network['extra'].setdefault(attr, net_payload.get(attr))
        return network

    def create_or_update(self, data, region, timestamp):
        model_instance = super().create_or_update(data=data, region=region, timestamp=timestamp)
        if model_instance:
            network_data = data.get('network')
            tags = None
            if network_data:
                tags = network_data.get('tags')
            if tags and len(tags):
                # remove tags that do not exist anymore on the network
                tags_to_remove = model_instance.network_tags.all().exclude(tag_name__in=tags)
                if tags_to_remove:
                    for tag in tags_to_remove:
                        model_instance.network_tags.remove(tag)
                # add tags to network
                available_tags = NetworkTag.objects.filter(tag_name__in=tags)
                for network_tag in available_tags:
                    model_instance.network_tags.add(network_tag)
                if available_tags.count() < len(tags):
                    # try to create new tags only if received tags count is less than db tags count
                    for tag in tags:
                        try:
                            network_tag = NetworkTag.objects.create(tag_name=tag)
                        except (Exception, IntegrityError):
                            network_tag = NetworkTag.objects.filter(tag_name=tag).first()
                        if network_tag:
                            model_instance.network_tags.add(network_tag)

    def delete(self, payload, region, timestamp):
        net_id = payload.get('network_id', None)
        if not net_id:
            LOG.error('Unable to delete network without network_id: {}'.format(payload))
        # delete subnets allocated to the network
        Subnet.objects.filter(network_id=net_id).delete()
        return super(NetworkEventHandler, self).delete(net_id, region, timestamp)


class NetworkRbacEventHandler(BaseHandler):
    serializer_class = serializers.NetworkRbacSerializer
    version_field = 'sync_version'

    def __init__(self):
        self.event_handlers = {'rbac_policy.create.end': self.create_or_update,
                               'rbac_policy.update.end': self.create_or_update,
                               'rbac_policy.delete.end': self.delete,
                               'network.create.end': self.create_from_network,
                               'network.delete.end': self.delete_from_network,
                               'network.update.end': self.create_from_network}

    @staticmethod
    def get_network_rbac(network_id, region):
        """
        Network creation and deletion does not trigger rbac events even
        if rbac rules are created if the network is shared or external, in Mitaka.
        We sync directly from the API just in case.
        """
        rbac_policies = dict(rbac_policies=list())
        try:
            admin_session = IdentityAdminApi().session
            nc = neutron_client(api_session=admin_session, region_name=region)
            rbac_policies = nc.list_rbac_policies(retrieve_all=True, object_id=network_id)
        except Exception as e:
            LOG.exception(e)
        return rbac_policies

    def create_from_network(self, payload, region, timestamp):
        """Creating a new shared or external network automatically
        creates RBAC rules without events, in Mitaka
        We automatically generate a sync from API.
        """
        network_id = payload['network']['id']
        rbac_policies = self.get_network_rbac(network_id, region)
        for policy in rbac_policies['rbac_policies']:
            self.create_or_update(data=dict(rbac_policy=policy), region=region, timestamp=timestamp)

    def delete_from_network(self, payload, region, timestamp):
        net_id = payload['network_id']
        return self.model_class.objects.filter(object_type='network', object_id=net_id).delete()

    def serialize(self, data, region, timestamp):
        rbac_policy = copy.deepcopy(data['rbac_policy'])
        rbac_policy['target_project'] = rbac_policy['target_tenant']
        rbac_policy['project_id'] = rbac_policy['tenant_id']
        rbac_policy[self.version_field] = self.get_version(timestamp)
        return rbac_policy

    def delete(self, payload, region, timestamp):
        policy_id = payload['rbac_policy_id']
        if not policy_id:
            LOG.error('Unable to delete Network RBAC policy with missing ')
        return super(NetworkRbacEventHandler, self).delete(policy_id, region, timestamp)


class SubnetEventHandler(BaseHandler):
    serializer_class = serializers.SubnetSyncSerializer
    version_field = 'sync_version'

    def __init__(self):
        self.event_handlers = {'subnet.create.end': self.create_or_update,
                               'subnet.update.end': self.create_or_update,
                               'subnet.delete.end': self.delete}

    def serialize(self, payload, region, timestamp):
        subnet = copy.deepcopy(payload['subnet'])
        subnet[self.version_field] = self.get_version(timestamp)
        subnet['project_id'] = subnet.get('tenant_id', None)
        subnet['extra'] = dict()
        for attr in ('ipv6_address_mode', 'ipv6_ra_mode', 'host_routes', 'dns_nameservers'):
            if attr in subnet:
                subnet['extra'].setdefault(attr, subnet.get(attr))
        return subnet

    def delete(self, payload, region, timestamp):
        subnet_id = payload.get('subnet_id')
        if not subnet_id:
            LOG.error('Unable to delete subnet without subnet_id: {}'.format(payload))
            return
        return super(SubnetEventHandler, self).delete(subnet_id, region, timestamp)


class SubnetPoolEventHandler(BaseHandler):
    serializer_class = serializers.SubnetPoolSyncSerializer
    version_field = 'sync_version'

    def __init__(self):
        self.event_handlers = {'subnetpool.create.end': self.create_or_update,
                               'subnetpool.update.end': self.create_or_update,
                               'subnetpool.delete.end': self.delete}

    def serialize(self, payload, region, timestamp):
        subnet_pool = copy.deepcopy(payload['subnetpool'])
        subnet_pool[self.version_field] = self.get_version(timestamp)
        subnet_pool['project_id'] = subnet_pool.get('tenant_id', None)
        subnet_pool['region'] = region
        return subnet_pool

    def delete(self, payload, region, timestamp):
        subnet_id = payload.get('subnetpool_id')
        if not subnet_id:
            LOG.error('Unable to delete subnet pool without subnetpool_id: {}'.format(payload))
            return
        return super(SubnetPoolEventHandler, self).delete(subnet_id, region, timestamp)


class FloatingIPEventHandler(BaseHandler):
    serializer_class = serializers.FloatingIpSyncSerializer
    version_field = 'sync_version'

    def __init__(self):
        self.event_handlers = {'floatingip.create.end': self.create_or_update,
                               'floatingip.update.end': self.create_or_update,
                               'floatingip.delete.end': self.delete}

    def serialize(self, data, region, timestamp):
        floating_ip = copy.deepcopy(data['floatingip'])
        floating_ip[self.version_field] = self.get_version(timestamp)
        floating_ip['project_id'] = floating_ip.get('project_id', floating_ip.get('tenant_id', None))
        if floating_ip.get('updated_at', None) is None:
            floating_ip['updated_at'] = timestamp
            # FIXME(tomo): Save the created_at date for Mitaka and below ?
        # FIXME(erno): https://bugs.launchpad.net/neutron/+bug/1593793, after this bug is fixed remove if/else below
        if floating_ip.get('port_id', None) and floating_ip.get('status', None) == 'DOWN':
            floating_ip['status'] = 'ACTIVE'
        return floating_ip

    def delete(self, payload, region, timestamp):
        fip_id = payload.get('floatingip_id', None)
        if fip_id is None:
            LOG.error('Could not delete floating ip')
            return
        return super(FloatingIPEventHandler, self).delete(fip_id, region, timestamp)


class RouterEventHandler(BaseHandler):
    serializer_class = serializers.RouterSyncSerializer
    version_field = 'sync_version'

    def __init__(self):
        self.event_handlers = {'router.create.end': self.create_or_update,
                               'router.update.end': self.create_or_update,
                               'router.delete.end': self.delete}

    def serialize(self, data, region, timestamp):
        router = data['router']
        new_data = copy.deepcopy(router)
        new_data[self.version_field] = self.get_version(timestamp)
        new_data['project_id'] = router.get('tenant_id', router.get('project_id', None))
        new_data['region'] = region
        external_gateway_info = router.get('external_gateway_info', None)
        if external_gateway_info:
            new_data['external_network_id'] = external_gateway_info.get('network_id', None)
            new_data['external_fixed_ips'] = external_gateway_info.get('external_fixed_ips', None)
            new_data['enable_snat'] = external_gateway_info.get('enable_snat', None)
        return new_data

    def delete(self, payload, region, timestamp):
        obj_id = payload.get('router_id', None)
        if not obj_id:
            LOG.error('Unable to delete port without router_id: {}'.format(payload))
        return super(RouterEventHandler, self).delete(obj_id, region, timestamp)


class SecurityGroupEventHandler(BaseHandler):
    serializer_class = serializers.SecurityGroupSyncSerializer
    version_field = 'sync_version'

    def __init__(self):
        self.event_handlers = {'security_group.create.end': self.create_or_update,
                               'security_group.update.end': self.create_or_update,
                               'security_group.delete.end': self.delete}

    def serialize(self, data, region, timestamp):
        security_group = data['security_group']
        new_data = copy.deepcopy(security_group)
        new_data[self.version_field] = self.get_version(timestamp)
        new_data['region'] = region
        new_data['project_id'] = security_group.get('project_id', security_group.get('tenant_id', None))
        return new_data

    def create_or_update(self, data, region, timestamp):
        # NOTE(tomo): Handle security group rules sync here too
        sec_rules = data.get('security_group', dict()).get('security_group_rules', list())
        if len(sec_rules):
            sgr_serializer = SecurityGroupRuleEventHandler()
            for sgr in sec_rules:
                sgr_serializer.create_or_update(data={'security_group_rule': sgr}, region=region, timestamp=timestamp)
        return super(SecurityGroupEventHandler, self).create_or_update(data, region, timestamp)

    def delete(self, payload, region, timestamp):
        sec_gr = payload.get('security_group', None)
        if sec_gr is None:
            # Note(tomo): Notifications differ based on version...
            sec_gr_id = payload.get('security_group_id', None)
        else:
            sec_gr_id = sec_gr['id']
        return super(SecurityGroupEventHandler, self).delete(sec_gr_id, region, timestamp)


class SecurityGroupRuleEventHandler(BaseHandler):
    serializer_class = serializers.SecurityGroupRuleSyncSerializer
    version_field = 'sync_version'

    def __init__(self):
        self.event_handlers = {'security_group_rule.create.end': self.create_or_update,
                               'security_group_rule.delete.end': self.delete}

    def serialize(self, data, region, timestamp):
        security_group = data['security_group_rule']
        new_data = copy.deepcopy(security_group)
        new_data[self.version_field] = self.get_version(timestamp)
        new_data['project_id'] = security_group.get('project_id', security_group.get('tenant_id', None))
        return new_data

    def delete(self, payload, region, timestamp):
        sec_grr = payload.get('security_group_rule')
        return super(SecurityGroupRuleEventHandler, self).delete(sec_grr['id'], region, timestamp)
