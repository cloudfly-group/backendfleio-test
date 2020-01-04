import copy
import logging
from typing import Optional

from django.conf import settings
from django.utils.timezone import now as utcnow
from django.utils.translation import ugettext_lazy as _
from neutronclient.common import exceptions
from neutronclient.common.exceptions import NotFound

from fleio.openstack.api.neutron import create_security_group_if_missing, neutron_client
from fleio.openstack.api.nova import nova_client
from fleio.openstack.models import FloatingIp as OpenstackFloatingIp
from fleio.openstack.models import Network as OpenstackNetwork
from fleio.openstack.models import Port as OpenstackPort
from fleio.openstack.models import Router as OpenstackRouter
from fleio.openstack.models import SecurityGroup as OpenstackSecurityGroup
from fleio.openstack.models import Subnet as OpenstackSubnet
from fleio.openstack.models import SubnetPool as OpenstackSubnetPool
from fleio.openstack.networking.sync_handlers import NetworkSyncHandler, PortSyncHandler, RouterSyncHandler
from fleio.openstack.networking.sync_handlers import SubnetSyncHandler
from fleio.openstack.settings import plugin_settings

LOG = logging.getLogger(__name__)


class Networks(object):
    def __init__(self, api_session):
        """
        :type api_session: keystoneauth1.session.Session
        """
        self.api_session = api_session

    def auto_create_network(self, project_id, region=None):
        """
        Feature is called 'Get Me A Network' in neutron.
        :returns: created network id
        """
        region = region or plugin_settings.DEFAULT_REGION
        nc = neutron_client(api_session=self.api_session, region_name=region)
        message = nc.get_auto_allocated_topology(project_id=project_id)
        try:
            network_id = message['auto_allocated_topology']['id']
            self.sync_auto_created_objects(nc, network_id, region)
            return network_id
        except KeyError:
            return None

    @staticmethod
    def sync_auto_created_objects(nc, network_id, region):
        # sync network
        network = nc.show_network(network=network_id)
        nsh = NetworkSyncHandler()
        nsh.create_or_update(data=network['network'], region=region, timestamp=utcnow().isoformat())

        # sync subnets
        ssh = SubnetSyncHandler()
        for subnet_id in network['network']['subnets']:
            subnet = nc.show_subnet(subnet=subnet_id)
            ssh.create_or_update(data=subnet['subnet'], region=region, timestamp=utcnow().isoformat())

        # sync ports and router
        ports = nc.list_ports(network_id=network_id)
        nph = PortSyncHandler()
        # more interfaces can have the same router, we need to prevent to sync it each time
        router_ids = list()
        port_ids = list()
        for port in ports['ports']:
            if port['id'] not in port_ids:
                port_ids.append(port['id'])
                nph.create_or_update(data=port, region=region, timestamp=utcnow().isoformat())
                if port['device_owner'] == getattr(settings, 'ROUTER_PORT_DEVICE_OWNER', 'network:router_interface'):
                    Networks.sync_router_and_ports(nc, port, port_ids, region, router_ids)
                    # TODO(erno): synchronize dhcp if implemented in openstack/models

    @staticmethod
    def sync_router_and_ports(nc, port, port_ids, region, router_ids):
        router_id = port['device_id']
        if router_id not in router_ids:
            rsh = RouterSyncHandler()
            router_ids.append(router_id)
            router = nc.show_router(router=router_id)
            rsh.create_or_update(data=router['router'], region=region,
                                 timestamp=utcnow().isoformat())
            router_ports = nc.list_ports(device_id=router_id)
            nph = PortSyncHandler()
            for router_port in router_ports['ports']:
                if router_port['id'] not in port_ids:
                    port_ids.append(router_port['id'])
                    nph.create_or_update(data=router_port, region=region, timestamp=utcnow().isoformat())

    def get(self, network):
        """
        :type network: fleio.openstack.models.Network
        :rtype: Network
        """
        return Network(network_id=network.id, api_session=self.api_session)

    def create(self, kwargs):
        args = copy.deepcopy(kwargs)
        region = args.pop('region', None) or plugin_settings.DEFAULT_REGION
        args.pop('client', None)
        project = None
        if 'project' in args:
            project = args.pop('project')
        if project:
            args['tenant_id'] = project.project_id
        args.pop('sync_version', None)
        if 'router_external' in args:
            args['router:external'] = args.pop('router_external')
        if 'provider_network_type' in args:
            args['provider:network_type'] = args.pop('provider_network_type')
        if 'provider_physical_network' in args and args['provider_physical_network']:
            args['provider:physical_network'] = args['provider_physical_network']
        args.pop('provider_physical_network', None)
        if 'provider_segmentation_id' in args and args['provider_segmentation_id']:
            args['provider:segmentation_id'] = args['provider_segmentation_id']
        args.pop('provider_segmentation_id', None)
        subnet = args.pop('subnet', None)
        nc = neutron_client(api_session=self.api_session, region_name=region)

        network = nc.create_network(body={"network": args})
        if subnet:
            if 'subnetpool_id' in subnet:
                if not subnet['subnetpool_id']:
                    subnet.pop('subnetpool_id')
                elif 'allocation_pools' in subnet and not subnet['allocation_pools']:
                    subnet.pop('allocation_pools')
            if 'cidr' in subnet and not subnet['cidr']:
                subnet.pop('cidr')
            if 'ipv6_ra_mode' in subnet and not subnet['ipv6_ra_mode']:
                subnet.pop('ipv6_ra_mode')
            if 'ipv6_address_mode' in subnet and not subnet['ipv6_address_mode']:
                subnet.pop('ipv6_address_mode')

            subnet['network_id'] = network['network']['id']
            if project:
                subnet['tenant_id'] = project.project_id
            nc.create_subnet(body={"subnet": subnet})
        return network

    def update(self, old_values, new_values):
        args = copy.deepcopy(new_values)
        args.pop('client', None)
        args.pop('project', None)
        args.pop('sync_version', None)
        if 'router_external' in args:
            args['router:external'] = args.pop('router_external')
        nc = neutron_client(api_session=self.api_session, region_name=old_values.region)
        try:
            # TODO(erno): remove block if bug fixed in neutron
            # can't update simultaneously default=True and external=True if both were false, because external will be
            # True and default will remain False ==> two calls are necessary
            if not old_values.router_external and not old_values.is_default \
                    and new_values['is_default'] and new_values['router_external']:
                nc.update_network(network=old_values.id, body={"network": args})
        except KeyError:
            pass

        return nc.update_network(network=old_values.id, body={"network": args})

    def delete_all(self):
        # NOTE(erno): optimize
        for network_id in OpenstackNetwork.objects.values_list('id'):
            Network(network_id=network_id, api_session=self.api_session).delete()

    def config_auto_create_network_options(self, region):
        """
        For auto create network to work an external default network and an ipv4 and/or ipv6 default shared subnet
        pool is/are needed.
        Returns: a list of external networks, shared ipv4 and ipv6 shared subnet pools filtered by region and the
        current valid auto create configuration for <region>.
        """
        if not region:
            return {}

        options = dict()
        options['networks'] = [{'id': n.id, 'name': n.name, 'description': n.description} for n in
                               OpenstackNetwork.objects.filter(region=region, router_external=True)]
        subnetpools = OpenstackSubnetPool.objects.filter(region=region, shared=True)
        options['ipv4_subnetpools'] = [
            {'id': sp.id, 'name': sp.name, 'description': sp.description} for sp in subnetpools if sp.ip_version == 4]
        options['ipv6_subnetpools'] = [
            {'id': sp.id, 'name': sp.name, 'description': sp.description} for sp in subnetpools if sp.ip_version == 6]

        return options

    def get_current_auto_create_config(self, region):
        """
        Returns the current valid configuration for auto creating network for <region>. This means if a default
        external network exists it is returned in the config dict.
        """
        config = dict()
        try:
            network = OpenstackNetwork.objects.get(region=region, router_external=True, is_default=True)
            config['network'] = {'id': network.id, 'name': network.name}
        except OpenstackNetwork.DoesNotExist:
            pass
        except OpenstackNetwork.MultipleObjectsReturned as e:
            LOG.error(e)
        try:
            ipv4_pool = OpenstackSubnetPool.objects.get(region=region, is_default=True, shared=True, ip_version=4)
            config['ipv4_subnetpool'] = {'id': ipv4_pool.id, 'name': ipv4_pool.name}
        except OpenstackSubnetPool.DoesNotExist:
            pass
        except OpenstackSubnetPool.MultipleObjectsReturned as e:
            LOG.error(e)
        try:
            ipv6_pool = OpenstackSubnetPool.objects.get(region=region, is_default=True, shared=True, ip_version=6)
            config['ipv6_subnetpool'] = {'id': ipv6_pool.id, 'name': ipv6_pool.name}
        except OpenstackSubnetPool.DoesNotExist:
            pass
        except OpenstackSubnetPool.MultipleObjectsReturned as e:
            LOG.error(e)
        return config

    def set_network_as_default(self, region, network_id):
        nc = neutron_client(api_session=self.api_session, region_name=region)
        # Openstack can't set a network default, if one is already present
        default_network = OpenstackNetwork.objects.filter(region=region, is_default=True).first()
        if default_network:
            if default_network.id == network_id:
                return {'id': default_network.id, 'name': default_network.name}
            nc.update_network(network=default_network.id, body={"network": {'is_default': False}})
        # TODO(erno): There will be cases for which two openstack calls will be made. Somehow we must make this method
        # atomic
        # if network_id is '' simply unset the default if it exists
        if network_id:
            network = nc.update_network(network=network_id, body={"network": {'is_default': True}})['network']
            return {'id': network['id'], 'name': network['name']}


class Network(object):
    def __init__(self, network_id, api_session=None):
        """
        :type network_id: fleio.openstack.models.Network.id
        """
        self.network_id = network_id
        self.api_session = api_session

    def neutron_api(self, region=None):
        region = region or plugin_settings.DEFAULT_REGION
        assert self.api_session is not None, 'Unable to use neutron_api without an api_session!'
        return neutron_client(self.api_session, region_name=region)

    def delete(self, region=None):
        """Delete the network from Neutron."""
        try:
            self.neutron_api(region=region).delete_network(network=self.network_id)
        except NotFound:
            OpenstackNetwork.objects.filter(id=self.network_id).delete()


class FloatingIps(object):
    def __init__(self, api_session):
        """
        :type api_session: keystoneauth1.session.Session
        """
        self.api_session = api_session

    def get(self, floating_ip):
        """
        :type floating_ip: fleio.openstack.models.FloatingIp
        :rtype: FloatingIp
        """
        return FloatingIp(floating_ip_id=floating_ip.id, api_session=self.api_session)

    def associate_ip(self, floating_ip, port, fixed_ip=None, region=None):
        region = region or plugin_settings.DEFAULT_REGION
        nc = neutron_client(api_session=self.api_session, region_name=region)
        if fixed_ip:
            nc.update_floatingip(floatingip=floating_ip,
                                 body={'floatingip': {'port_id': port, 'fixed_ip_address': str(fixed_ip)}})
        else:
            nc.update_floatingip(floatingip=floating_ip, body={'floatingip': {'port_id': port}})

    def dissociate_ip(self, floating_ip, region=None):
        region = region or plugin_settings.DEFAULT_REGION
        nc = neutron_client(api_session=self.api_session, region_name=region)
        nc.update_floatingip(floatingip=floating_ip, body={'floatingip': {}})

    def create(self, floating_network_id, description, region=None, project_id=None):
        region = region or plugin_settings.DEFAULT_REGION
        nc = neutron_client(api_session=self.api_session, region_name=region)
        args = dict(floating_network_id=floating_network_id, description=description)
        if project_id:
            args['tenant_id'] = project_id
        return nc.create_floatingip(body={'floatingip': args})

    def delete_all(self):
        # NOTE(erno): optimize
        for floating_ip_id in OpenstackFloatingIp.objects.values_list('id'):
            FloatingIp(floating_ip_id=floating_ip_id, api_session=self.api_session).delete()


class FloatingIp(object):
    def __init__(self, floating_ip_id, api_session=None):
        """
        :type floating_ip_id: str, floating IP id
        """
        self.floating_ip_id = floating_ip_id
        self.api_session = api_session

    def neutron_api(self, region=None):
        region = region or plugin_settings.DEFAULT_REGION
        assert self.api_session is not None, 'Unable to use neutron_api without an api_session!'
        return neutron_client(self.api_session, region_name=region)

    def delete(self, region=None):
        """Delete the floating ip from Neutron."""
        try:
            self.neutron_api(region=region).delete_floatingip(floatingip=self.floating_ip_id)
        except exceptions.NotFound:
            OpenstackFloatingIp.objects.filter(id=self.floating_ip_id).delete()


class Subnets(object):
    def __init__(self, api_session):
        """
        :type api_session: keystoneauth1.session.Session
        """
        self.api_session = api_session

    def get(self, subnet):
        """
        :type subnet: fleio.openstack.models.Subnet
        :rtype: Subnet
        """
        return Subnet(subnet_id=subnet.id, api_session=self.api_session)

    def create(self, kwargs):
        args = copy.deepcopy(kwargs)
        network = args.pop('network', None)
        if 'network_id' not in args:
            args['network_id'] = network.id
        region = network.region if network else plugin_settings.DEFAULT_REGION
        args.pop('project', None)
        args.pop('sync_version', None)
        if 'subnetpool_id' in args:
            if not args['subnetpool_id']:
                args.pop('subnetpool_id')
            elif 'allocation_pools' in args and not args['allocation_pools']:
                args.pop('allocation_pools')
        if 'cidr' in args and not args['cidr']:
            args.pop('cidr')
        if 'ipv6_ra_mode' in args and not args['ipv6_ra_mode']:
            args.pop('ipv6_ra_mode')
        if 'ipv6_address_mode' in args and not args['ipv6_address_mode']:
            args.pop('ipv6_address_mode')

        nc = neutron_client(api_session=self.api_session, region_name=region)
        return nc.create_subnet(body={"subnet": args})

    def update(self, old_values, new_values):
        network = OpenstackNetwork.objects.filter(id=old_values.network_id).first()
        region = network.region if network else plugin_settings.DEFAULT_REGION
        new_values.pop('sync_version', None)
        nc = neutron_client(api_session=self.api_session, region_name=region)
        return nc.update_subnet(subnet=old_values.id, body={"subnet": new_values})

    def delete_all(self):
        # NOTE(erno): optimize
        for subnet_id in OpenstackSubnet.objects.values_list('id'):
            Subnet(subnet_id=subnet_id, api_session=self.api_session).delete()


class Subnet(object):
    def __init__(self, subnet_id, api_session=None):
        """
        :type subnet_id: fleio.openstack.models.Subnet.id
        """
        self.subnet_id = subnet_id
        self.api_session = api_session

    def neutron_api(self, region=None):
        region = region or plugin_settings.DEFAULT_REGION
        assert self.api_session is not None, 'Unable to use neutron_api without an api_session!'
        return neutron_client(self.api_session, region_name=region)

    def delete(self, region=None):
        """Delete the subnet from Neutron."""
        try:
            self.neutron_api(region=region).delete_subnet(subnet=self.subnet_id)
        except exceptions.NotFound:
            OpenstackSubnet.objects.filter(id=self.subnet_id).delete()


class SubnetPools(object):
    def __init__(self, api_session):
        """
        :type api_session: keystoneauth1.session.Session
        """
        self.api_session = api_session

    def get(self, subnet_pool):
        """
        :type subnet_pool: fleio.openstack.models.SubnetPool
        :rtype: SubnetPool
        """
        return SubnetPool(subnet_pool_id=subnet_pool.id, api_session=self.api_session)

    def create(self, kwargs):
        args = copy.deepcopy(kwargs)
        region = args.pop('region', None) or plugin_settings.DEFAULT_REGION
        args.pop('client', None)
        args.pop('sync_version', None)
        if 'default_quota' in args and not args['default_quota']:
            args.pop('default_quota')
        if not args.get('project_id', None):
            args.pop('project_id', None)

        nc = neutron_client(api_session=self.api_session, region_name=region)

        return nc.create_subnetpool(body={"subnetpool": args})

    def update(self, id, region, kwargs):
        args = copy.deepcopy(kwargs)
        region = args.pop('region', None) or plugin_settings.DEFAULT_REGION
        args.pop('client', None)
        args.pop('project_id', None)
        args.pop('shared', None)
        args.pop('sync_version', None)
        if 'default_quota' in args and not args['default_quota']:
            args.pop('default_quota')

        nc = neutron_client(api_session=self.api_session, region_name=region)

        return nc.update_subnetpool(subnetpool=id, body={"subnetpool": args})

    def delete_all(self):
        for subnet_pool_id in OpenstackSubnetPool.objects.values_list('id'):
            SubnetPool(subnet_pool_id=subnet_pool_id, api_session=self.api_session).delete()

    def set_subnetpool_as_default(self, region, subnetpool_id, ip_version=4):
        nc = neutron_client(api_session=self.api_session, region_name=region)
        # Openstack can't set a subnetpool default, if one is already present
        default_subnetpool = OpenstackSubnetPool.objects.filter(region=region, shared=True, is_default=True,
                                                                ip_version=ip_version).first()
        if default_subnetpool:
            if default_subnetpool.id == subnetpool_id:
                return {'id': default_subnetpool.id, 'name': default_subnetpool.name}
            nc.update_subnetpool(subnetpool=default_subnetpool.id, body={"subnetpool": {'is_default': False}})
        # TODO(erno): There will be cases for which two openstack calls will be made. Somehow we must make this method
        # atomic
        # if subnetpool_id is '' simply unset the default if it exists
        if subnetpool_id:
            subnetpool = nc.update_subnetpool(subnetpool=subnetpool_id, body={"subnetpool": {'is_default': True}})[
                'subnetpool']
            return {'id': subnetpool['id'], 'name': subnetpool['name']}


class SubnetPool(object):
    def __init__(self, subnet_pool_id, api_session=None):
        """
        :type subnet_pool_id: fleio.openstack.models.SubnetPool.id
        """
        self.subnet_pool_id = subnet_pool_id
        self.api_session = api_session

    def neutron_api(self, region=None):
        region = region or plugin_settings.DEFAULT_REGION
        assert self.api_session is not None, 'Unable to use neutron_api without an api_session!'
        return neutron_client(self.api_session, region_name=region)

    def delete(self, region=None):
        """Delete the subnet pool from Neutron."""
        try:
            self.neutron_api(region=region).delete_subnetpool(subnetpool=self.subnet_pool_id)
        except exceptions.NotFound:
            OpenstackSubnetPool.objects.filter(id=self.subnet_pool_id).delete()


class Ports(object):
    def __init__(self, api_session):
        """
        :type api_session: keystoneauth1.session.Session
        """
        self.api_session = api_session

    def get(self, port):
        """
        :type port: fleio.openstack.models.Port
        :rtype: Port
        """
        return Port(port=port, api_session=self.api_session)

    def create(self, kwargs):
        args = copy.deepcopy(kwargs)
        region = args.pop('region', None) or plugin_settings.DEFAULT_REGION
        args.pop('sync_version', None)
        project = args.get('project', None)
        network = args.get('network', None)
        if project:
            args['tenant_id'] = project
        if network:
            args['network_id'] = network.id

        nc = neutron_client(api_session=self.api_session, region_name=region)

        sgid = create_security_group_if_missing(api_session=self.api_session, region=region,
                                                project_id=args['tenant_id'])
        port = {'network_id': args['network_id'],
                'tenant_id': args['tenant_id'],
                'security_groups': [sgid]}
        if args['fixed_ips']:
            port['fixed_ips'] = args['fixed_ips']

        port = nc.create_port(body={"port": port})

        if args['attach_to'] == 'instance':
            nova = nova_client(api_session=self.api_session, region_name=region)
            nova.servers.interface_attach(server=args['device_id'], port_id=port['port']['id'],
                                          net_id=None, fixed_ip=None)
        args.pop('attach_to', None)
        return port

    def update(self, old_data, kwargs):
        args = copy.deepcopy(kwargs)
        region = args.pop('region', None) or plugin_settings.DEFAULT_REGION
        args.pop('sync_version', None)
        args.pop('project', None)
        subnet_id = args.pop('subnet', None)

        nc = neutron_client(api_session=self.api_session, region_name=region)

        port = {}
        if args['fixed_ips']:
            port['fixed_ips'] = [{'ip_address': fixed_ip['ip_address'], 'subnet_id': subnet_id or fixed_ip['subnet_id']}
                                 for fixed_ip in args['fixed_ips']]
        else:
            port['fixed_ips'] = [{'subnet_id': subnet_id}]

        port = nc.update_port(port=old_data.id, body={"port": port})
        return port

    def delete_all(self):
        [Port(port=port, api_session=self.api_session).delete() for port in OpenstackPort.objects.all()]


class Port(object):
    def __init__(self, port: Optional[OpenstackPort], api_session=None):
        self.port = port
        self.api_session = api_session

    def neutron_api(self, region=None):
        region = region or plugin_settings.DEFAULT_REGION
        assert self.api_session is not None, 'Unable to use neutron_api without an api_session!'
        return neutron_client(self.api_session, region_name=region)

    def delete(self, region=None, port_id=None):
        """Delete the port from Neutron."""
        try:
            self.neutron_api(region=region).delete_port(port=port_id or self.port.id)
        except exceptions.NotFound:
            OpenstackPort.objects.filter(id=port_id or self.port.id).delete()

    def add_ip(self, kwargs):
        args = copy.deepcopy(kwargs)
        region = args.pop('region', None) or plugin_settings.DEFAULT_REGION
        args.pop('sync_version', None)
        args.pop('project', None)
        subnet_id = args.pop('subnet', None)

        nc = neutron_client(api_session=self.api_session, region_name=region)

        port = {}
        if args['fixed_ips']:
            port['fixed_ips'] = [{'ip_address': fixed_ip['ip_address'], 'subnet_id': subnet_id or fixed_ip['subnet_id']}
                                 for fixed_ip in args['fixed_ips']]
        else:
            port['fixed_ips'] = [{'subnet_id': subnet_id}]
        port['fixed_ips'] += self.port.fixed_ips

        port = nc.update_port(port=self.port.id, body={"port": port})
        if self.port.fixed_ips == port['port']['fixed_ips']:
            raise exceptions.BadRequest(
                _('Could not add ip. Possibly subnet configuration is incorrect for automatic IP adding.'))
        return port

    def add_ips(self, kwargs):
        region = kwargs.get('region', None) or plugin_settings.DEFAULT_REGION
        nc = neutron_client(api_session=self.api_session, region_name=region)

        port = nc.update_port(port=self.port.id,
                              body={"port": {'fixed_ips': self.port.fixed_ips + kwargs['fixed_ips']}})
        if self.port.fixed_ips == port['port']['fixed_ips']:
            raise exceptions.BadRequest(
                _('Could not add ips. Possibly subnet configuration is incorrect for automatic IP adding.'))
        return port

    def remove_ip(self, kwargs):
        args = copy.deepcopy(kwargs)
        region = args.pop('region', None) or plugin_settings.DEFAULT_REGION
        args.pop('sync_version', None)
        args.pop('project', None)
        subnet_id = args.pop('subnet', None)

        nc = neutron_client(api_session=self.api_session, region_name=region)

        port = {}
        if args['fixed_ips']:
            port['fixed_ips'] = [{'ip_address': fixed_ip['ip_address'], 'subnet_id': subnet_id or fixed_ip['subnet_id']}
                                 for fixed_ip in args['fixed_ips']]
        else:
            port['fixed_ips'] = [{'subnet_id': subnet_id}]
        port['fixed_ips'] = [fip for fip in self.port.fixed_ips if fip not in port['fixed_ips']]

        port = nc.update_port(port=self.port.id, body={"port": port})
        return port


class Routers(object):
    def __init__(self, api_session):
        """
        :type api_session: keystoneauth1.session.Session
        """
        self.api_session = api_session

    def get(self, router):
        """
        :type router: fleio.openstack.models.Router
        :rtype: Router
        """
        return Router(router_id=router.id, api_session=self.api_session)

    def create(self, kwargs):
        args = copy.deepcopy(kwargs)
        region = args.pop('region', None) or plugin_settings.DEFAULT_REGION
        if hasattr(region, 'id'):
            region = region.id
        project = args.pop('project', None)
        args.pop('client', None)
        external_network_id = args.pop('external_network_id', None)
        if project:
            args['tenant_id'] = project.project_id

        nc = neutron_client(api_session=self.api_session, region_name=region)

        router = nc.create_router(body={"router": args})
        if external_network_id:
            nc.add_gateway_router(router=router['router']['id'], body={'network_id': external_network_id})

        return router

    def update(self, id, region, kwargs):
        args = copy.deepcopy(kwargs)
        region = args.pop('region', None) or plugin_settings.DEFAULT_REGION
        project = args.pop('project', None)
        args.pop('client', None)
        external_network_id = args.pop('external_network_id', None)
        if project:
            args['tenant_id'] = project.project_id
        description = args.get('description', '')
        if description is None:
            description = ''
        args['description'] = description

        nc = neutron_client(api_session=self.api_session, region_name=region)

        router = nc.update_router(router=id, body={"router": args})
        if external_network_id:
            nc.add_gateway_router(router=router['router']['id'], body={'network_id': external_network_id})

        return router

    def delete_all(self):
        for router_id in OpenstackRouter.objects.values_list('id'):
            Router(router_id=router_id, api_session=self.api_session).delete()


class Router(object):
    def __init__(self, router_id, api_session=None):
        """
        :type router_id: fleio.openstack.models.Router.id
        """
        self.router_id = router_id
        self.api_session = api_session

    def neutron_api(self, region=None):
        region = region or plugin_settings.DEFAULT_REGION
        assert self.api_session is not None, 'Unable to use neutron_api without an api_session!'
        return neutron_client(self.api_session, region_name=region)

    def delete(self, region=None):
        """Delete the router from Neutron."""
        try:
            self.neutron_api(region=region).remove_gateway_router(router=self.router_id)
            ports = OpenstackPort.objects.filter(
                device_id=self.router_id,
                device_owner=getattr(settings, 'ROUTER_PORT_DEVICE_OWNER', 'network:router_interface')
            )
            [self.neutron_api(region=region).remove_interface_router(router=self.router_id, body={'port_id': port.id})
             for port in ports]
            self.neutron_api(region=region).delete_router(router=self.router_id)
        except exceptions.NotFound:
            OpenstackRouter.objects.filter(id=self.router_id).delete()

    def add_interface(self, region, subnet, ip=None):
        neutron = self.neutron_api(region=region)
        body = {}
        if ip:
            sub = OpenstackSubnet.objects.get(id=subnet)
            body = {'port': {'fixed_ips': [{'ip_address': ip, 'subnet_id': subnet}], 'network_id': sub.network_id}}
            port = self.neutron_api().create_port(body=body)
            body['port_id'] = port['port']['id']
        else:
            body['subnet_id'] = subnet
        neutron.add_interface_router(router=self.router_id, body=body)

    def remove_interface(self, region, interface_id):
        try:
            self.neutron_api(region=region).remove_interface_router(router=self.router_id,
                                                                    body={'port_id': interface_id})
        except exceptions.NotFound:
            pass


class SecurityGroups(object):
    def __init__(self, api_session):
        """
        :type api_session: keystoneauth1.session.Session
        """
        self.api_session = api_session

    def get(self, security_group):
        """
        :type security_group: fleio.openstack.models.SecurityGroup
        :rtype: SecurityGroup
        """
        return SecurityGroup(security_group_id=security_group.id, api_session=self.api_session)

    def create(self, region, **kwargs):
        nc = neutron_client(api_session=self.api_session, region_name=region)
        return nc.create_security_group(body={"security_group": kwargs})

    def update(self, id, region, kwargs):
        nc = neutron_client(api_session=self.api_session, region_name=region.id)
        return nc.update_security_group(security_group=id, body={"security_group": kwargs})

    def delete_all(self):
        for security_group_id in OpenstackSecurityGroup.objects.values_list('id'):
            SecurityGroup(security_group_id=security_group_id, api_session=self.api_session).delete()


class SecurityGroup(object):
    def __init__(self, security_group_id, api_session=None):
        """
        :type security_group_id: fleio.openstack.models.SecurityGroup.id
        """
        self.security_group_id = security_group_id
        self.api_session = api_session

    def neutron_api(self, region=None):
        region = region or plugin_settings.DEFAULT_REGION
        assert self.api_session is not None, 'Unable to use neutron_api without an api_session!'
        return neutron_client(self.api_session, region_name=region)

    def delete(self, region=None):
        """Delete the security group from Neutron."""
        try:
            self.neutron_api(region=region).delete_security_group(security_group=self.security_group_id)
        except exceptions.NotFound:
            OpenstackSecurityGroup.objects.filter(id=self.security_group_id).delete()

    def create_rule(self, region, **kwargs):
        if 'port_range_min' in kwargs and not kwargs.get('protocol', None):
            raise exceptions.BadRequest(_('If port is given protocol must also be set'))
        self.neutron_api(region=region).create_security_group_rule(body={"security_group_rule": kwargs})

    def delete_rule(self, region, rule_id):
        try:
            self.neutron_api(region=region).delete_security_group_rule(security_group_rule=rule_id)
        except NotFound:
            pass
