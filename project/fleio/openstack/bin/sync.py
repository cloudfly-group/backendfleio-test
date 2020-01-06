import logging
import sys
import threading
from os import environ
from os import path
import json

import django
from django.conf import settings
from django.utils.timezone import now as utcnow
from glanceclient.exc import CommunicationError
from keystoneauth1.exceptions import (ClientException, ConnectFailure, ConnectTimeout, DiscoveryFailure,
                                      EndpointNotFound, NotFound, Unauthorized)
from neutronclient.common.exceptions import NotFound as NeutronNotFoundException
from requests.exceptions import SSLError
from six.moves.urllib.parse import urlparse

from novaclient.api_versions import APIVersion

current_path = path.dirname(path.abspath(__file__))
fleio_path = path.dirname(path.dirname(path.dirname(current_path)))

sys.path.append(fleio_path)
environ.setdefault("DJANGO_SETTINGS_MODULE", "fleio.settings")
django.setup()

LOG = logging.getLogger(__name__)

from fleio.celery import app  # noqa

from fleio.openstack.api import identity  # noqa
from fleio.openstack.api.cinder import cinder_client  # noqa
from fleio.openstack.api.glance import glance_client  # noqa
from fleio.openstack.api.nova import nova_client  # noqa
from fleio.openstack.api.neutron import neutron_client  # noqa
from fleio.openstack.hypervisors.api import Hypervisors  # noqa

from fleio.openstack.discovery import PublicEndpoint  # noqa

from fleio.openstack.instances.sync_handlers import InstanceSyncHandler  # noqa
from fleio.openstack.hypervisors.sync_handlers import HypervisorSyncHandler  # noqa

from fleio.openstack.images.sync_handlers import ImageSyncHandler  # noqa
from fleio.openstack.images.sync_handlers import ImageMemberSyncHandler  # noqa

from fleio.openstack.models import FloatingIp  # noqa
from fleio.openstack.models import Image  # noqa
from fleio.openstack.models import Instance  # noqa
from fleio.openstack.models import Network  # noqa
from fleio.openstack.models import OpenstackInstanceFlavor  # noqa
from fleio.openstack.models import Port  # noqa
from fleio.openstack.models import SecurityGroup  # noqa
from fleio.openstack.models import Subnet  # noqa
from fleio.openstack.models import SubnetPool  # noqa
from fleio.openstack.models import Volume  # noqa
from fleio.openstack.models import VolumeType  # noqa
from fleio.openstack.models import VolumeTypeExtraSpec  # noqa
from fleio.openstack.models import Project  # noqa
from fleio.openstack.models import Hypervisor  # noqa
from fleio.openstack.models import OpenstackRole  # noqa

from fleio.openstack.networking.serializers import FloatingIpSyncSerializer  # noqa
from fleio.openstack.networking.sync_handlers import NetworkSyncHandler  # noqa
from fleio.openstack.networking.sync_handlers import SubnetPoolSyncHandler  # noqa
from fleio.openstack.networking.sync_handlers import NetworkRbacSyncHandler  # noqa
from fleio.openstack.networking.sync_handlers import PortSyncHandler  # noqa
from fleio.openstack.networking.sync_handlers import RouterSyncHandler  # noqa
from fleio.openstack.networking.sync_handlers import SubnetSyncHandler  # noqa
from fleio.openstack.networking.sync_handlers import FloatingIPSyncHandler  # noqa
from fleio.openstack.networking.sync_handlers import SecurityGroupsSyncHandler  # noqa

from fleio.openstack.container_infra.sync_process import sync_coe as sync_coe_process  # noqa

from fleio.openstack.projects.sync_handlers import ProjectSyncHandler  # noqa

from fleio.openstack.settings import plugin_settings  # noqa

from fleio.openstack.volumes.notification_handler import QoSSyncHandler  # noqa
from fleio.openstack.volume_backups.notification_handler import VolumeBackupSyncHandler  # noqa
from fleio.openstack.volume_snapshots.notification_handler import VolumeSnapshotSyncHandler  # noqa
from fleio.openstack.volumes.notification_handler import VolumeSyncHandler  # noqa
from fleio.openstack.volumes.notification_handler import VolumeTypeSyncHandler  # noqa
from fleio.openstack.volumes.notification_handler import VolumeTypeExtraSpecSyncHandler  # noqa
from fleio.openstack.volumes.notification_handler import VolumeTypeToProjectSyncHandler  # noqa
from fleio.openstack.regions.sync_process import sync_regions as sync_regions_process  # noqa


# Timestamp used for calculating the models versions
timestamp = utcnow().isoformat()

AUTH_CACHE = dict()


def get_keystone_admin():
    # Initialize a keystone client
    return identity.IdentityAdminApi(request_session=AUTH_CACHE)


def sync_regions():
    """Add missing regions to fleio db that are present in OpenStack"""
    return sync_regions_process(auth_cache=AUTH_CACHE)


def sync_roles(region_id=None):
    """Sync openstack roles"""
    del region_id  # unused
    synced_roles = list()
    kc = get_keystone_admin().client
    for role in kc.roles.list():
        synced_roles.append(role.id)
        db_role, created = OpenstackRole.objects.get_or_create(
            id=role.id,
            name=role.name,
        )
        if created:
            LOG.info('Adding openstack role {} to fleio database'.format(role.name))

    OpenstackRole.objects.exclude(id__in=synced_roles).delete()
    return OpenstackRole.objects.all()


def sync_projects():
    project_sync_handler = ProjectSyncHandler()
    projects_to_process = get_keystone_admin().client.projects.list()
    if projects_to_process:
        for project in projects_to_process:
            project_sync_handler.create_or_update(project, region=None, timestamp=timestamp)

    # cleanup not synced projects but keep those marked as deleted (kept for revenue data)
    Project.objects.exclude(deleted=True).filter(sync_version__lt=project_sync_handler.get_version(timestamp)).delete()


def sync_images(region_id=None):
    imh = ImageSyncHandler()
    member_handler = ImageMemberSyncHandler()
    gc = glance_client(api_session=get_keystone_admin().session, region_name=region_id, version='2')
    # Retrieve images using pagination
    has_more = True
    list_limit = 50
    marker = None
    try:
        while has_more:
            images = gc.images.list(limit=list_limit, marker=marker)
            if not images:
                break
            image_count = 0
            for image in images:
                imh.create_or_update(image, region=region_id, timestamp=timestamp)
                marker = image.id
                image_count += 1
                # Sync image members here because we can only get members per image
                if image.get('visibility') == 'shared':
                    for member in gc.image_members.list(image_id=image.id):
                        member_handler.create_or_update(member, region=region_id, timestamp=timestamp)
            has_more = image_count == list_limit
    except EndpointNotFound as e:
        LOG.error(str(e))
        return
    version = imh.get_version(timestamp)
    delete_filter = {'{}__lt'.format(imh.version_field): version, 'region__id': region_id}
    imh.model_class.objects.filter(**delete_filter).delete()
    # Delete older image member records
    member_version = member_handler.get_version(timestamp)
    member_delete_filter = {
        '{}__lt'.format(member_handler.version_field): member_version,
        'image__region__id': region_id
    }
    member_handler.model_class.objects.filter(**member_delete_filter).delete()


def sync_coe(region_id=None):
    sync_coe_process(region_id=region_id, auth_cache=AUTH_CACHE)


def sync_instances(region_id=None):
    ih = InstanceSyncHandler()
    nc = nova_client(api_session=get_keystone_admin().session, region_name=region_id)
    try:
        for instance in nc.servers.list(detailed=True, search_opts={'all_tenants': '1'}):
            ih.create_or_update(instance, region=region_id, timestamp=timestamp)
    except EndpointNotFound as e:
        LOG.error(str(e))
        return
    version = ih.get_version(timestamp)
    delete_filter = {'{}__lt'.format(ih.version_field): version, 'region': region_id}
    ih.model_class.objects.filter(**delete_filter).delete()


def sync_hypervisors(region_id=None):
    hh = HypervisorSyncHandler()

    try:
        for hypervisor in Hypervisors(api_session=get_keystone_admin().session).get_hypervisors(region=region_id):
            hh.create_or_update(data=hypervisor, region=region_id, timestamp=timestamp)
    except Exception as e:
        LOG.error(str(e))
        return
    # delete hypervisors that were not synced in the current version
    version = hh.get_version(timestamp)
    delete_filter = {'{}__lt'.format(hh.version_field): version, 'region': region_id}
    Hypervisor.objects.filter(**delete_filter).delete()


def sync_volumes(cinder, region_id=None):
    vh = VolumeSyncHandler()
    has_more = True
    marker = None
    list_limit = 50
    try:
        while has_more:
            volumes = cinder.volumes.list(detailed=True,
                                          limit=list_limit,
                                          search_opts={'all_tenants': '1'},
                                          marker=marker)
            if not volumes:
                break
            has_more = len(volumes) == list_limit
            marker = volumes[-1].id
            for volume in volumes:
                vh.create_or_update(volume=volume, region=region_id, timestamp=timestamp)
    except EndpointNotFound as e:
        LOG.error(str(e))
        return

    # Delete all volumes with a version less than our current sync version
    # TODO(tomo): Volumes deleted between version and now, are not removed
    version = vh.get_version(timestamp)
    vh.model_class.objects.filter(region=region_id, sync_version__lt=version).delete()


def sync_volume_backups(cinder, region_id=None):
    sync_handler = VolumeBackupSyncHandler()
    has_more = True
    marker = None
    list_limit = 50
    try:
        while has_more:
            volume_backups = cinder.backups.list(
                detailed=True, limit=list_limit, search_opts={'all_tenants': True}, marker=marker
            )
            if not volume_backups:
                break
            has_more = len(volume_backups) == list_limit
            marker = volume_backups[-1].id
            for volume_backup in volume_backups:
                sync_handler.create_or_update(data=volume_backup, region=region_id, timestamp=timestamp)
    except EndpointNotFound as e:
        LOG.error(str(e))
        return
    version = sync_handler.get_version(timestamp=timestamp)
    VolumeBackupSyncHandler.serializer_class.Meta.model.objects.filter(sync_version__lt=version).delete()


def sync_volume_snapshots(cinder, region_id=None):
    sync_handler = VolumeSnapshotSyncHandler()
    has_more = True
    marker = None
    list_limit = 50
    try:
        while has_more:
            volume_snapshots = cinder.volume_snapshots.list(
                detailed=True, limit=list_limit, search_opts={'all_tenants': True}, marker=marker
            )
            if not volume_snapshots:
                break
            has_more = len(volume_snapshots) == list_limit
            marker = volume_snapshots[-1].id
            for volume_snapshot in volume_snapshots:
                sync_handler.create_or_update(data=volume_snapshot, region=region_id, timestamp=timestamp)
    except EndpointNotFound as e:
        LOG.error(str(e))
        return
    version = sync_handler.get_version(timestamp=timestamp)
    VolumeSnapshotSyncHandler.serializer_class.Meta.model.objects.filter(sync_version__lt=version).delete()


def sync_volume_types(volume_types, region=None):
    sync_handler = VolumeTypeSyncHandler()
    for volume_type in volume_types:
        sync_handler.create_or_update(data=volume_type, region=region, timestamp=timestamp)
    version = sync_handler.get_version(timestamp)
    VolumeTypeSyncHandler.serializer_class.Meta.model.objects.filter(region__id=region,
                                                                     sync_version__lt=version).delete()


def sync_volume_type_extra_specs(volume_type):
    sync_handler = VolumeTypeExtraSpecSyncHandler()
    for key, value in iter(volume_type.extra_specs.items()):
        sync_handler.create_or_update(
            data={
                'volume_type_id': volume_type.id,
                'key': key, 'value': value
            },
            region=None,
            timestamp=timestamp
        )
    version = sync_handler.get_version(timestamp)
    VolumeTypeExtraSpecSyncHandler.serializer_class.Meta.model.objects.filter(volume_type_id=volume_type.id,
                                                                              sync_version__lt=version).delete()


def sync_volume_type_to_projects(volume_type_to_projects):
    sync_handler = VolumeTypeToProjectSyncHandler()
    for volume_type_to_project in volume_type_to_projects:
        sync_handler.create_or_update(data=volume_type_to_project, region=None, timestamp=timestamp)
    version = sync_handler.get_version(timestamp)
    # FIXME(tomo): Delete from specific region only
    VolumeTypeToProjectSyncHandler.serializer_class.Meta.model.objects.filter(sync_version__lt=version).delete()


def sync_qos_specs(qos_specs):
    sync_handler = QoSSyncHandler()
    qos_spec_model = QoSSyncHandler.serializer_class.Meta.model
    for qos_spec in qos_specs:
        sync_handler.create_or_update(data=qos_spec, region=None, timestamp=timestamp)
    version = sync_handler.get_version(timestamp)
    # FIXME(tomo): Delete from specific region only
    qos_spec_model.objects.filter(sync_version__lt=version).delete()


def sync_cinder(region_id=None):
    assert region_id is not None, 'Unable to sync cinder objects without a region'
    cc = cinder_client(api_session=get_keystone_admin().session, region_name=region_id)
    try:
        volume_types = cc.volume_types.list()
    except EndpointNotFound as e:
        LOG.error(str(e))
        return
    sync_volume_types(volume_types=volume_types, region=region_id)
    for volume_type in volume_types:
        sync_volume_type_extra_specs(volume_type=volume_type)
        if not volume_type.is_public:
            volume_type_to_projects = cc.volume_type_access.list(volume_type=volume_type.id)
            sync_volume_type_to_projects(volume_type_to_projects=volume_type_to_projects)
    qos_specs = cc.qos_specs.list()
    sync_qos_specs(qos_specs=qos_specs)
    sync_volumes(cc, region_id)
    sync_volume_backups(cinder=cc, region_id=region_id)
    sync_volume_snapshots(cinder=cc, region_id=region_id)


def sync_floating_ips(floating_ips, region_id=None):
    fsh = FloatingIPSyncHandler()
    floating_ip_model = FloatingIpSyncSerializer.Meta.model
    for ip in floating_ips:
        fsh.create_or_update(data=ip, region=None, timestamp=timestamp)
    # Remove floating ips cached in Fleio but missing in OpenStack
    version = fsh.get_version(timestamp)
    floating_ip_model.objects.filter(sync_version__lt=version, floating_network__region=region_id).delete()


def sync_networks(networks, region_id=None):
    assert region_id is not None, 'Unable to sync networks without a region'
    nsh = NetworkSyncHandler()
    for network in networks:
        nsh.create_or_update(data=network, region=region_id, timestamp=timestamp)
    # Remove networks cached in Fleio but missing in OpenStack
    version = nsh.get_version(timestamp)
    nsh.serializer_class.Meta.model.objects.filter(region=region_id, sync_version__lt=version).delete()


def sync_subnets(subnets, region_id=None):
    ssh = SubnetSyncHandler()
    for subnet in subnets:
        ssh.create_or_update(data=subnet, region=None, timestamp=timestamp)
    # Remove subnets cached in Fleio but missing in OpenStack
    version = ssh.get_version(timestamp)
    ssh.model_class.objects.filter(sync_version__lt=version, network__region=region_id).delete()


def sync_ports(ports, region_id):
    nph = PortSyncHandler()
    for port in ports:
        nph.create_or_update(data=port, region=None, timestamp=timestamp)
    # Remove ports cached in Fleio but missing in OpenStack
    version = nph.get_version(timestamp)
    nph.model_class.objects.filter(sync_version__lt=version, network__region=region_id).delete()


def sync_network_rbacs(rbac_rules):
    nsr = NetworkRbacSyncHandler()
    for rule in rbac_rules:
        nsr.create_or_update(data=rule, region=None, timestamp=timestamp)
    version = nsr.get_version(timestamp)
    # FIXME(tomo): Delete from specific region only
    nsr.model_class.objects.filter(sync_version__lt=version).delete()


def sync_routers(routers, region_id):
    rsh = RouterSyncHandler()
    for router in routers:
        rsh.create_or_update(data=router, region=region_id, timestamp=timestamp)
    # Remove routers cached in Fleio but missing in OpenStack
    version = rsh.get_version(timestamp)
    # FIXME(tomo): Delete from specific region only
    rsh.model_class.objects.filter(sync_version__lt=version, region=region_id).delete()


def sync_subnet_pools(subnet_pools, region_id):
    sph = SubnetPoolSyncHandler()
    for subnet_pool in subnet_pools:
        sph.create_or_update(data=subnet_pool, region=region_id, timestamp=timestamp)
    version = sph.get_version(timestamp)
    sph.model_class.objects.filter(sync_version__lt=version, region=region_id).delete()


def sync_networking(region_id=None):
    nc = neutron_client(api_session=get_keystone_admin().session, region_name=region_id)
    try:
        networks = nc.list_networks(retrieve_all=True).get('networks', list())
    except EndpointNotFound as e:
        LOG.error(str(e))
        return
    sync_networks(networks=networks, region_id=region_id)
    subnets = nc.list_subnets(retrieve_all=True).get('subnets', list())
    sync_subnets(subnets=subnets, region_id=region_id)
    ports = nc.list_ports(retrieve_all=True).get('ports', list())
    sync_ports(ports=ports, region_id=region_id)
    try:
        floating_ips = nc.list_floatingips(retrieve_all=True).get('floatingips', list())
    except NeutronNotFoundException:
        LOG.warning('Openstack not configured for floating ips')
    else:
        sync_floating_ips(floating_ips, region_id=region_id)
    rbac_rules = nc.list_rbac_policies(retrieve_all=True).get('rbac_policies', list())
    sync_network_rbacs(rbac_rules)
    try:
        routers = nc.list_routers(retrieve_all=True).get('routers', list())
    except NeutronNotFoundException:
        LOG.warning('Openstack not configured for routers')
    else:
        sync_routers(routers, region_id=region_id)
    subnet_pools = nc.list_subnetpools(retrieve_all=True).get('subnetpools', list())
    sync_subnet_pools(subnet_pools, region_id=region_id)


def sync_security_groups(region_id=None):
    nc = neutron_client(api_session=get_keystone_admin().session, region_name=region_id)
    # FIXME(tomo): Support pagination when available
    try:
        sec_groups = nc.list_security_groups(retrieve_all=True)
    except EndpointNotFound as e:
        LOG.error(str(e))
        return
    sg_handler = SecurityGroupsSyncHandler()
    for sg in sec_groups.get('security_groups', list()):
        sg_handler.create_or_update(data=sg, region=region_id, timestamp=timestamp)
    # Remove missing sg rules
    version = sg_handler.get_version(timestamp)
    sg_handler.model_class.objects.filter(region__id=region_id, sync_version__lt=version).delete()


def sync_flavors(region_id=None):
    def _get_int_or_zero(value):
        """Convert to int or return 0 if unable to convert."""
        try:
            int_value = int(value)
        except ValueError:
            int_value = 0
        return int_value

    def _update_flavor(dbf, openstack_flavor):
        dbf.name = openstack_flavor.name
        dbf.vcpus = openstack_flavor.vcpus
        dbf.root_gb = _get_int_or_zero(openstack_flavor.disk)
        dbf.memory_mb = _get_int_or_zero(openstack_flavor.ram)
        dbf.swap = _get_int_or_zero(openstack_flavor.swap)
        dbf.is_public = openstack_flavor.is_public
        dbf.region_id = region_id
        dbf.disabled = getattr(openstack_flavor, 'OS-FLV-DISABLED:disabled', False)
        dbf.ephemeral_gb = _get_int_or_zero(openstack_flavor.ephemeral)
        dbf.deleted = False
        properties = openstack_flavor.get_keys()
        dbf.properties = json.dumps(properties)
        if not dbf.description:
            dbf.description = openstack_flavor.name
        dbf.save()

    # Get flavors from API
    try:
        api_flavors = nova_client(api_session=get_keystone_admin().session, region_name=region_id).\
            flavors.list(is_public=None)
    except EndpointNotFound as e:
        LOG.error(str(e))
        return
    existing_flavors = []
    for f in api_flavors:
        try:
            db_flv = OpenstackInstanceFlavor.objects.get(id=f.id)
            existing_flavors.append(db_flv.id)
        except OpenstackInstanceFlavor.DoesNotExist:
            LOG.info('Attempting to create missing flavor: %s ' % f.name)
            # Get the region object in DB
            try:
                db_flv = OpenstackInstanceFlavor.objects.create(id=f.id,
                                                                name=f.name,
                                                                memory_mb=_get_int_or_zero(f.ram),
                                                                vcpus=f.vcpus,
                                                                swap=_get_int_or_zero(f.swap),
                                                                root_gb=f.disk,
                                                                ephemeral_gb=_get_int_or_zero(f.ephemeral),
                                                                is_public=f.is_public,
                                                                disabled=getattr(f, 'OS-FLV-DISABLED:disabled', False),
                                                                region_id=region_id,
                                                                show_in_fleio=True,
                                                                description=f.name,
                                                                properties=json.dumps(f.get_keys()))
                existing_flavors.append(db_flv.id)
            except Exception as e:
                LOG.error('Unable to create flavor %s: %s' % (f.name, e))
            # Go to the next flavor if not found.
            continue

        # If found, update it's records:
        _update_flavor(db_flv, f)
    # Remove missing flavors from region
    OpenstackInstanceFlavor.objects.exclude(id__in=existing_flavors).filter(region__id=region_id).delete()


def set_api_versions():
    """
    Updates or creates OpenStack SERVICES with their corresponding API version.

    This takes into consideration multi-region OpenStacks. It evaluates each service and its API version and sets
    the supported API version across all regions in Fleio db.
    """
    api_session = get_keystone_admin().session
    service_catalog = api_session.auth.get_access(api_session).service_catalog
    available_services = [service['type'] for service in service_catalog.catalog]
    available_versions = {}

    def get_service_versions(service_type):
        try:
            endpoint = PublicEndpoint(api_session=api_session, service_type=service_type)
            endpoint_versions = endpoint.version_data

            if endpoint_versions:
                for version in endpoint_versions:
                    version_value = None
                    # NOTE(tomo): list(filter()) # py2 and 3 compatibility
                    endpoint = list(filter(lambda link: link['rel'] == 'self', version['links']))[0]['href']
                    status = version['status']

                    if 'version' in version and version['version']:
                        version_value = version.get('version')
                    elif 'id' in version:
                        version_value = version.get('id')
                    if service_type not in available_versions:
                        available_versions[service_type] = {endpoint: {status: [version_value]}}
                    elif endpoint not in available_versions[service_type]:
                        available_versions[service_type][endpoint] = {status: [version_value]}
                    else:
                        if status not in available_versions[service_type][endpoint]:
                            available_versions[service_type][endpoint][status] = [version_value]
                        else:
                            available_versions[service_type][endpoint][status].append(version_value)
        except KeyError:
            LOG.error('Unexpected api response for service: {}'.format(service_type))
        except ClientException as e:
            LOG.error('{}'.format(e))

    for service in available_services:
        if service not in settings.FLEIO_API_VERSIONS:
            continue
        else:
            get_service_versions(service)

    def get_all_versions(urls_with_versions):
        all_versions = {}
        parsed_urls = []
        for url, data in urls_with_versions.items():
            url = urlparse(url).hostname

            if url not in parsed_urls:
                parsed_urls.append(url)
                all_versions[url] = [value[0] for k, value in iter(data.items())]
            else:
                for k, api_version in iter(data.items()):
                    all_versions[url].append(api_version[0])

        return all_versions

    def get_min_max_versions(versions):
        """Converts services api_version from 'str' to 'float' and returns the compatible min and max values found."""
        min_version, max_version = [], []

        for endpoint_versions in versions.items():
            parsed_versions = []
            for version_value in endpoint_versions[1]:
                string_version = version_value

                if 'v' in string_version:
                    string_version = string_version[1:]

                if '.' not in string_version:
                    string_version += '.0'

                parsed_versions.append(APIVersion(string_version))

            min_version.append(min(parsed_versions))
            max_version.append(max(parsed_versions))

        return min(min_version), min(max_version)

    if available_versions:
        for service in available_versions:
            service_versions = get_all_versions(available_versions[service])

            if service_versions:
                compatible_min_version, compatible_max_version = get_min_max_versions(service_versions)

                if compatible_max_version <= APIVersion(settings.FLEIO_API_VERSIONS[service]['max_version']):
                    f_api_version = compatible_max_version
                elif compatible_min_version >= APIVersion(settings.FLEIO_API_VERSIONS[service]['min_version']):
                    f_api_version = compatible_min_version
                else:
                    f_api_version = compatible_max_version

                if f_api_version:
                    if '-' in service:
                        service = service.replace('-', '_')
                    setattr(plugin_settings, '{}_api_version'.format(service.lower()), f_api_version.get_string())

        plugin_settings.save()


def delete_objects_from_unused_regions(current_regions):
    """
    Delete OpenStack objects from regions no longer used.
    Will delete all cloud objects in other regions than :param current_regions:."
    """
    # TODO(adrian): we still have to delete objects that are not related to a region. I.e. based on project ID.
    Instance.objects.exclude(region__in=current_regions).delete()
    Image.objects.exclude(region__in=current_regions).delete()
    OpenstackInstanceFlavor.objects.exclude(region__in=current_regions).delete()
    Subnet.objects.exclude(network__region__in=current_regions).delete()
    Port.objects.exclude(network__region__in=current_regions).delete()
    FloatingIp.objects.exclude(floating_network__region__in=current_regions).delete()
    SubnetPool.objects.exclude(region__in=current_regions).delete()
    Network.objects.exclude(region__in=current_regions).delete()
    OpenstackInstanceFlavor.objects.exclude(region__in=current_regions).delete()
    SecurityGroup.objects.exclude(region__in=current_regions).delete()
    Volume.objects.exclude(region__in=current_regions).delete()
    VolumeTypeExtraSpec.objects.exclude(volume_type__region__in=current_regions).delete()
    VolumeType.objects.exclude(region__in=current_regions).delete()


def sync_openstack_objects():
    try:
        all_regions = sync_regions()
        LOG.debug('Calling sync_regions')
        set_api_versions()
        LOG.debug('Syncing OpenStack services with their corresponding API Versions')
    except SSLError:
        LOG.error('Keystone SSL certificate is invalid')
    except Exception as e:
        LOG.exception(e)
    else:
        procedures = [sync_coe, sync_roles, sync_hypervisors, sync_images, sync_instances, sync_networking, sync_cinder,
                      sync_security_groups, ]
        # must sync flavors before instances to get the flavor when syncing instances
        try:
            for region in all_regions:
                sync_flavors(region_id=region.id)
            sync_projects()
        except Exception as e:
            LOG.exception('Exception {} when sync flavor and projects, ignoring'.format(e))

        for procedure in procedures:
            try:
                if not all_regions:
                    LOG.error('You have no regions defined, please check your configuration.')
                    break
                for region in all_regions:
                    LOG.info('Calling {} for region {}'.format(procedure, region.id))
                    tp = threading.Thread(target=procedure, args=(region.id,))
                    tp.start()
            except (NotFound, Unauthorized, AssertionError, ConnectTimeout,
                    ConnectFailure, DiscoveryFailure, CommunicationError, EndpointNotFound) as e:
                if isinstance(e, NotFound) or isinstance(e, ConnectTimeout) or isinstance(e, CommunicationError) \
                        or isinstance(e, ConnectFailure) or isinstance(e, DiscoveryFailure):
                    LOG.error(
                        "{} The URL you are trying to use is {}, please fix.".format(e,
                                                                                     plugin_settings.AUTH_URL))
                elif isinstance(e, Unauthorized):
                    LOG.error("{} OpenStack Authentication failed,"
                              " please check your credentials and/or OpenStack settings.".format(e))
                elif isinstance(e, AssertionError):
                    LOG.error("{} The tenant(project) you are trying to use is: "
                              "{} , please fix.".format(e, plugin_settings.USER_PROJECT_ID))
                elif isinstance(e, EndpointNotFound):
                    LOG.error("{}".format(e))
            except Exception as e:
                LOG.error(e)

            delete_objects_from_unused_regions(all_regions)


@app.task(
    bind=True, max_retries=settings.TASK_RETRIES, autoretry_for=(Exception,), name='Sync openstack objects',
)
def sync_openstack_objects_task(self):
    del self  # unused
    global timestamp
    timestamp = utcnow().isoformat()
    sync_openstack_objects()


if __name__ == '__main__':

    if len(sys.argv) > 1 and sys.argv[1] == '--debug':
        LOG.setLevel(logging.DEBUG)

    sync_openstack_objects()
