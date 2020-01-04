import json
import logging
from typing import Optional
from uuid import uuid4
from datetime import timedelta

import celery
from cinderclient import exceptions as cinder_exceptions
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now as utcnow
from glanceclient import exc as glance_exceptions
from novaclient import exceptions as nova_exceptions

from fleio.activitylog.utils.activity_helper import activity_helper
from fleio.celery import app
from fleio.conf.exceptions import ConfigException
from fleio.core.models import AppUser, Operation
from fleio.openstack.api.cinder import cinder_client
from fleio.openstack.api.glance import glance_client
from fleio.openstack.api.identity import IdentityAdminApi
from fleio.openstack.api.neutron import delete_project_security_groups
from fleio.openstack.api.nova import nova_client
from fleio.openstack.container_infra.sync_process import sync_coe
from fleio.openstack.images.api import Image as APIImage  # noqa
from fleio.openstack.images.api import Images
from fleio.openstack.images.api import Images as APIImages
from fleio.openstack.images.tasks import import_image_from_file, upload_empty_qcow2_image
from fleio.openstack.images.tasks import import_image_from_url
from fleio.openstack.images.tasks import upload_zero_filled_image
from fleio.openstack.instances.operations import InstanceDeletion
from fleio.openstack.volume_backups.tasks import sync_volume_backup_extra_details
from fleio.openstack.volumes.tasks import sync_volume_extra_details
from fleio.openstack.instances.api import Instance
from fleio.openstack.instances.instance_status import InstancePowerState, InstanceStatus
from fleio.openstack.metrics import GnocchiMetrics
from fleio.openstack.models import FloatingIp as OpenstackFloatingIp
from fleio.openstack.models import Image
from fleio.openstack.models import Image as ModelImage
from fleio.openstack.models import Instance as ModelInstance
from fleio.openstack.models import Network as OpenstackNetwork
from fleio.openstack.models import OpenstackRegion
from fleio.openstack.models import Port as OpenstackPort
from fleio.openstack.models import Project as OpenstackProject
from fleio.openstack.models import Router as OpenstackRouter
from fleio.openstack.models import Subnet as OpenstackSubnet
from fleio.openstack.models import Hypervisor
from fleio.openstack.models import SubnetPool as OpenstackSubnetPool
from fleio.openstack.models import Volume as OpenstackVolume
from fleio.openstack.models.image import OpenStackImageStatus
from fleio.openstack.models.image import OpenStackImageVisibility
from fleio.openstack.networking.api import FloatingIp
from fleio.openstack.networking.api import Network
from fleio.openstack.networking.api import Port
from fleio.openstack.networking.api import Port as APIPort  # noqa
from fleio.openstack.networking.api import Ports as APIPorts
from fleio.openstack.networking.api import Router
from fleio.openstack.networking.api import Subnet
from fleio.openstack.networking.api import SubnetPool
from fleio.openstack.hypervisors.api import Hypervisors
from fleio.openstack.hypervisors.sync_handlers import HypervisorSyncHandler
from fleio.openstack.osapi import OSApi
from fleio.openstack.project import Project
from fleio.openstack.settings import plugin_settings
from fleio.openstack.signals import signals as user_signals
from fleio.openstack.signals.signals import instance_boot_from_iso
from fleio.openstack.signals.signals import instance_create
from fleio.openstack.users.api import OpenStackUserApi
from fleio.openstack.regions.sync_process import sync_regions
from fleio.utils.misc import wait_for

from fleio.openstack.dns.utils import create_or_update_ptr, get_default_ptr_format
from designateclient import exceptions as designate_exceptions

from fleio.openstack.signals.signals import openstack_error

# TODO: we should not import from staff
from fleiostaff.openstack import signals as staff_signals

LOG = logging.getLogger(__name__)

# Just to keep the qa styling happy. We need to import these tasks to be able
# to use celery always eager in tests and to also be able to import these in
# images/api to avoid circular dependencies
EXTERNAL_IMPORTABLE_TASKS = (
    import_image_from_file, import_image_from_url, sync_volume_backup_extra_details, sync_volume_extra_details
)

AUTH_CACHE = dict()


class InstanceTaskException(Exception):
    pass


@app.task(max_retries=settings.TASK_RETRIES, name='Create instance volume')
def create_instance_volume(project_id, project_domain_id, region_name, source_type,
                           source_id, volume_size, volume_type):
    os_api = OSApi(project=project_id,
                   domain=project_domain_id)
    new_volume = os_api.volumes.create(name=None,
                                       size=volume_size,
                                       region_name=region_name,
                                       type=volume_type,
                                       source_type=source_type,
                                       source_id=source_id)

    return new_volume.id


@app.task(bind=True,
          max_retries=settings.TASK_RETRIES,
          name='Wait for volume status',
          default_retry_delay=5,
          autoretry_for=(cinder_exceptions.NotFound,))
def wait_for_volume_status(self, volume_id, project_id, project_domain_id, region_name, status):
    if volume_id:
        os_api = OSApi(project=project_id,
                       domain=project_domain_id)
        cc = cinder_client(api_session=os_api.get_session(), region_name=region_name)
        volume = cc.volumes.get(volume_id)
        if volume.status != status:
            self.retry(countdown=5)
        else:
            return volume_id
    return None


@app.task(bind=True, max_retries=settings.TASK_RETRIES, name='Create instance')
def create_instance_task(
        self, volume_id, project_id, project_domain_id, region_name, name, image, flavor,
        nics, block_device_mapping_v2, block_device_mapping, user_data=None, user_id=None, admin_pass=None,
        key_name=None, key_content=None
):
    os_api = OSApi(project=project_id,
                   domain=project_domain_id)
    boot_device = None
    if block_device_mapping_v2:
        for block_device in block_device_mapping_v2:
            if block_device.get('boot_index') == '0':
                boot_device = block_device
    if boot_device and volume_id:  # NOTE(tomo): Boot from volume with a volume type specified
        boot_device['source_type'] = 'volume'
        boot_device['uuid'] = volume_id
    try:
        server = os_api.instances.create(name=name,
                                         image=image,
                                         flavor=flavor,
                                         admin_pass=admin_pass,
                                         nics=nics,
                                         region_name=region_name,
                                         key_name=key_name,
                                         key_content=key_content,
                                         user_data=user_data,
                                         block_device_mapping=block_device_mapping,
                                         block_device_mapping_v2=block_device_mapping_v2)
    except Exception as e:
        openstack_error.send(
            sender='create_instance_task',
            event_type='fleio_instance_create',
            payload=dict(exception=str(e)),
            region=region_name,
        )
        raise e

    if user_id:
        user = AppUser.objects.filter(id=user_id).first()
        if user:
            instance_create.send(sender=__name__, user=user, username=user.username,
                                 instance_id=server.id, request=None)

    activity_helper.add_current_activity_params(object_id=server.id)

    return server.id


@app.task(bind=True, max_retries=settings.TASK_RETRIES, name='Start instance', resource_type='Instance')
def start_instance(self, instance_id, retry_until_completed=False, **kwargs):
    """
    Start an openstack instance.
    Retries several time to ensure that instance starts.
    """
    del kwargs  # unused

    # intentionally let this throw an error to fail task if UUID not found in DB
    db_instance = ModelInstance.objects.get(id=instance_id)

    instance = Instance.with_admin_session(instance=db_instance)

    # FIXME(tomo): Deal with instances in failed states or other states

    if not retry_until_completed:
        try:
            instance.start()
        except nova_exceptions.ClientException as e:
            raise InstanceTaskException(str(e))
    else:
        if (instance.get_power_state() == InstancePowerState.RUNNING) and (instance.get_task_state() is None):
            LOG.debug('Success: instance is started')
            return
        seconds_to_wait = 2 ** self.request.retries
        if instance.can_be_started():
            LOG.debug('call start')
            instance.start()
            return
        else:
            # can't start instance right now, let's retry later
            LOG.debug('Let\'s retry in {} seconds'.format(seconds_to_wait))
            raise self.retry(countdown=seconds_to_wait)


@app.task(bind=True, max_retries=settings.TASK_RETRIES, name='Stop instance', resource_type='Instance')
def stop_instance(self, instance_id, retry_until_completed=False, stopped_by_fleio=True, **kwargs):
    """
    Stops an openstack instance.
    Retries several time to ensure that instance stops.
    """
    del kwargs  # unused

    # intentionally let this throw an error to fail task if UUID not found in DB
    db_instance = ModelInstance.objects.get(id=instance_id)

    instance = Instance.with_admin_session(instance=db_instance)

    if not retry_until_completed:
        try:
            instance.stop(stopped_by_fleio=stopped_by_fleio)
        except nova_exceptions.ClientException as e:
            raise InstanceTaskException(str(e))
    else:
        power_state = instance.get_power_state()
        if power_state in (InstancePowerState.SHUTDOWN, InstancePowerState.SHUTOFF):
            LOG.debug('Success: instance is stopped')
            return
        elif power_state in (InstancePowerState.CRASHED, InstancePowerState.SUSPENDED, InstancePowerState.FAILED):
            LOG.error('Warning: instance in failed state can\'t be stopped')
            return

        seconds_to_wait = 2 ** self.request.retries
        if instance.can_be_stopped():
            LOG.debug('call stop')
            instance.stop(stopped_by_fleio=stopped_by_fleio)
            return
        else:
            # can't stop instance right now, let's retry later
            LOG.debug('Let\'s retry in {} seconds'.format(seconds_to_wait))
            raise self.retry(countdown=seconds_to_wait)


@app.task(bind=True, max_retries=settings.TASK_RETRIES, name='Suspend openstack project', resource_type='Project')
def suspend_project(self, project_id, **kwargs):
    del self  # unused

    reason = kwargs.get('reason')
    try:
        project = Project.with_admin_session(project_id)
    except ConfigException:
        LOG.info('Cannot suspend project as openstack settings are missing/incorrect')
        return
    project.disable(reason=reason)

    task_list = list()

    for instance in project.instances.filter(terminated_at__isnull=True):
        task_list.append(stop_instance.s(instance.pk, True))

    celery.group(task_list).apply_async()


@app.task(bind=True, max_retries=settings.TASK_RETRIES, name='Resume openstack project', resource_type='Project')
def resume_project(self, project_id, **kwargs):
    del self, kwargs  # unused

    try:
        project = Project.with_admin_session(project_id)
    except ConfigException:
        LOG.info('Cannot resume project as openstack settings are missing/incorrect')
        return
    project.enable()

    task_list = list()

    for instance in project.instances.filter(terminated_at__isnull=True, stopped_by_fleio=True):
        # start only those instances stopped by fleio, if client stopped instance, do not start it
        task_list.append(start_instance.s(instance.pk, True))

    celery.group(task_list).apply_async()


@app.task(bind=True, max_retries=settings.TASK_RETRIES, name='Delete all openstack images', resource_type='Project')
def delete_openstack_images(self, project_id, user_id: Optional[int] = None):
    del self  # unused

    image_ids = ModelImage.objects.filter(project_id=project_id).values_list('id', 'region')
    parallel_tasks = [
        delete_openstack_image.si(
            image_id, region, project_id, user_id=user_id,
        ) for (image_id, region) in image_ids
    ]
    celery.group(parallel_tasks).apply_async()


@app.task(bind=True, max_retries=settings.TASK_RETRIES, name='Delete openstack API users', resource_type='Project')
def delete_openstack_apiusers(self, project_id):
    del self  # unused

    os_api = IdentityAdminApi()
    os_user_api = OpenStackUserApi(keystone_client=os_api.client)

    role_assignments = os_user_api.list_role_assignments(project=project_id, include_names=True)

    # NOTE(Marius): If a user has more than one role on a project then they will have two entries for that user.
    users = [role_assignment.user
             for role_assignment in role_assignments
             if role_assignment.user['name'] != plugin_settings.username]

    unique_users = {user['id']: user for user in users}
    for user_id in unique_users.keys():
        os_user_api.delete_user(user_id)


@app.task(bind=True, max_retries=settings.TASK_RETRIES, name='Delete openstack image', resource_type='Image')
def delete_openstack_image(self, image_id, region, project_id, user_id: Optional[int] = None):
    del self  # unused

    project = Project.with_admin_session(project_id, cache=AUTH_CACHE)
    gc = glance_client(api_session=project.api_session, region_name=region)
    try:
        db_image = ModelImage.objects.filter(id=image_id).first()
        if db_image.protected:
            gc.images.update(image_id=image_id, protected=False)
        gc.images.delete(image_id=image_id)

        user = AppUser.objects.filter(id=user_id).first()

        if user and db_image:
            if user.is_staff:
                staff_signals.staff_delete_image.send(
                    sender=__name__, user=user, user_id=user.id,
                    image_name=db_image.name, image_id=db_image.id,
                    username=user.username,
                )
            else:
                user_signals.user_delete_image.send(
                    sender=__name__, user=user, user_id=user.id,
                    image_name=db_image.name, image_id=db_image.id,
                    username=user.username,
                )

    except glance_exceptions.NotFound:
        ModelImage.objects.filter(id=image_id).delete()


@app.task(bind=True, max_retries=settings.TASK_RETRIES, name='Delete all openstack instances', resource_type='Project')
def delete_openstack_instances(self, project_id, user_id: Optional[int] = None):
    del self  # unused

    instances = ModelInstance.objects.filter(project_id=project_id).values_list('id', 'region')
    parallel_tasks = [
        delete_openstack_instance.si(
            instance_id, region, project_id, user_id=user_id,
        ) for (instance_id, region) in instances
    ]
    celery.group(parallel_tasks).apply_async()
    return [instance_id for (instance_id, region) in instances]


@app.task(bind=True, max_retries=settings.TASK_RETRIES, name='Delete openstack instance', resource_type='Instance')
def delete_openstack_instance(self, instance_id, region, project_id, user_id: Optional[int] = None):
    del self  # unused

    project = Project.with_admin_session(project_id, cache=AUTH_CACHE)
    nc = nova_client(api_session=project.api_session, region_name=region, extensions=True)
    try:
        user = AppUser.objects.filter(id=user_id).first()
        db_instance = ModelInstance.objects.filter(id=instance_id).first()
        nc.servers.delete(server=instance_id)
        if user and db_instance:
            if user.is_staff:
                staff_signals.staff_delete_instance.send(
                    sender=__name__, user=user, user_id=user.id,
                    instance_name=db_instance.name, instance_id=instance_id,
                    username=user.username
                )
            else:
                user_signals.user_delete_instance.send(
                    sender=__name__, user=user, user_id=user.id,
                    instance_name=db_instance.name, instance_id=instance_id,
                    username=user.username
                )
    except nova_exceptions.NotFound:
        ModelInstance.objects.filter(id=instance_id).delete()
    else:
        Operation.objects.create(
            operation_type=InstanceDeletion.name,
            primary_object_id=instance_id,
            params=json.dumps({
                'region': region,
            })
        )


@app.task(bind=True, max_retries=settings.TASK_RETRIES, name='Delete all openstack volumes', resource_type='Project')
def delete_openstack_volumes(self, project_id, user_id: Optional[int] = None):
    del self  # unused

    volumes = OpenstackVolume.objects.filter(project_id=project_id).values_list('id', 'region')
    parallel_tasks = [
        delete_openstack_volume.si(
            volume_id, region, project_id, user_id=user_id,
        ) for (volume_id, region) in volumes
    ]
    celery.group(parallel_tasks).apply_async()


@app.task(bind=True, max_retries=settings.TASK_RETRIES, name='Delete openstack volume', resource_type='Volume')
def delete_openstack_volume(self, volume_id, region, project_id, user_id: Optional[int] = None):
    del self  # unused

    project = Project.with_admin_session(project_id, cache=AUTH_CACHE)
    cc = cinder_client(api_session=project.api_session, region_name=region)
    try:
        db_volume = OpenstackVolume.objects.filter(id=volume_id).first()
        user = AppUser.objects.filter(id=user_id).first()
        cc.volumes.delete(volume=volume_id)

        if user and db_volume:
            if user.is_staff:
                staff_signals.staff_delete_volume.send(
                    sender=__name__, user=user, user_id=user.id,
                    volume_name=db_volume.name, volume_id=db_volume.id,
                    username=user.username,
                )
            else:
                user_signals.user_delete_volume.send(
                    sender=__name__, user=user, user_id=user.id,
                    volume_name=db_volume.name, volume_id=db_volume.id,
                    username=user.username,
                )

    except cinder_exceptions.NotFound:
        OpenstackVolume.objects.filter(id=volume_id).delete()


@app.task(bind=True, max_retries=settings.TASK_RETRIES,
          name='Delete openstack security groups', resource_type='Project')
def delete_openstack_project_security_groups(self, instances_list, project_id):
    del self  # unused

    project = Project.with_admin_session(project_id)
    api_session = project.api_session
    delete_project_security_groups(
        api_session=api_session, project_id=project.project_id, instances_list=instances_list
    )


@app.task(bind=True, max_retries=settings.TASK_RETRIES,
          name='Delete openstack gnocchi metrics', resource_type='Project')
def delete_openstack_gnocchi_metrics(self, project_id):
    del self  # unused

    project = Project.with_admin_session(project_id)
    api_session = project.api_session
    GnocchiMetrics(api_session=api_session).delete_resources(project_id=project.project_id)


@app.task(bind=True, max_retries=settings.TASK_RETRIES, name='Delete openstack project', resource_type='Project')
def delete_openstack_project(self, project_id, mark_deleted=False):
    del self  # unused
    # we never delete the project in our db when terminating service, mark_deleted indicates that
    if mark_deleted:
        db_project = OpenstackProject.objects.filter(project_id=project_id).first()
        if db_project:
            db_project.deleted = True
            db_project.save()
    project = Project.with_admin_session(project_id)
    project.delete()


@app.task(bind=True, max_retries=settings.TASK_RETRIES, name='Delete all openstack resources', resource_type='Project')
def delete_client_project_resources(self, project_id, user_id: Optional[int] = None, mark_project_as_deleted=True):
    """Delete project and all it's resources"""
    project = Project.with_admin_session(project_id)
    seconds_to_wait = 2 ** self.request.retries
    try:
        project.disable(reason='terminating')
        parallel_tasks = [
            delete_openstack_images.si(project_id=project_id, user_id=user_id),
            celery.chain(
                delete_openstack_instances.s(project_id=project_id, user_id=user_id),
                delete_openstack_project_security_groups.s(project_id=project_id),
            ),
            delete_openstack_volumes.si(project_id=project_id, user_id=user_id),
            delete_openstack_network_resources.si(project_id=project_id, user_id=user_id),
            delete_openstack_apiusers.si(project_id=project_id)
        ]

        # run resource deletion in parallel, but BEFORE project deletion
        parallel_group = celery.group(*parallel_tasks)
        fin_chord = parallel_group | celery.chain(
            [
                delete_openstack_gnocchi_metrics.si(project_id=project_id),
                delete_openstack_project.si(project_id=project_id, mark_deleted=mark_project_as_deleted)
            ]
        )
        celery.chain(fin_chord).apply_async()

    except Exception as e:
        LOG.error(e)
        raise self.retry(exc=e, countdown=seconds_to_wait)


@app.task(bind=True, max_retries=settings.TASK_RETRIES,
          name='Delete all openstack network resources', resource_type='Project')
def delete_openstack_network_resources(self, project_id, user_id: Optional[int] = None):
    del self  # unused

    sequential_tasks = [
        delete_openstack_project_routers.si(project_id=project_id),
        delete_openstack_project_ports.si(project_id=project_id),
        delete_openstack_project_subnets.si(project_id=project_id),
        delete_openstack_project_subnetpools.si(project_id=project_id),
        delete_openstack_project_networks.si(project_id=project_id, user_id=user_id),
        delete_openstack_project_floating_ips.si(project_id=project_id)
    ]
    celery.chain(*sequential_tasks).apply_async()


@app.task(bind=True, max_retries=settings.TASK_RETRIES, name='Delete all openstack networks', resource_type='Project')
def delete_openstack_project_networks(self, project_id, user_id: Optional[int] = None):
    del self  # unused

    networks = OpenstackNetwork.objects.filter(project=project_id).values_list('id', 'region')
    parallel_tasks = [
        delete_openstack_network.si(
            network_id, region, project_id, user_id=user_id,
        ) for (network_id, region) in networks
    ]
    celery.group(parallel_tasks).apply_async()


@app.task(bind=True, max_retries=settings.TASK_RETRIES, name='Delete openstack network', resource_type='Network')
def delete_openstack_network(self, network_id, region, project_id, user_id: Optional[int] = None):
    del self  # unused

    db_network = OpenstackNetwork.objects.filter(id=network_id).first()
    user = AppUser.objects.filter(id=user_id)

    project = Project.with_admin_session(project_id, cache=AUTH_CACHE)
    Network(network_id=network_id, api_session=project.api_session).delete(region=region)

    if user and db_network:
        if user.is_staff:
            staff_signals.staff_delete_network.send(
                sender=__name__, user=user, user_id=user.id,
                network_name=db_network.name, network_id=db_network.id,
                username=user.username
            )
        else:
            user_signals.user_delete_network.send(
                sender=__name__, user=user, user_id=user.id,
                network_name=db_network.name, network_id=db_network.id,
                username=user.username
            )


@app.task(bind=True, max_retries=settings.TASK_RETRIES, name='Delete all openstack ports', resource_type='Project')
def delete_openstack_project_ports(self, project_id):
    del self  # unused

    ports = OpenstackPort.objects.filter(project_id=project_id).values_list('id', 'network__region')
    parallel_tasks = [
        delete_openstack_port.si(
            port_id, region, project_id,
        ) for (port_id, region) in ports
    ]
    celery.group(parallel_tasks).apply_async()


@app.task(bind=True, max_retries=settings.TASK_RETRIES, name='Delete openstack port', resource_type='Port')
def delete_openstack_port(self, port_id, region, project_id):
    del self  # unused

    project = Project.with_admin_session(project_id, cache=AUTH_CACHE)
    Port(port=None, api_session=project.api_session).delete(region=region, port_id=port_id)


@app.task(bind=True, max_retries=settings.TASK_RETRIES, name='Delete all openstack subnets', resource_type='Project')
def delete_openstack_project_subnets(self, project_id):
    del self  # unused

    subnets = OpenstackSubnet.objects.filter(project_id=project_id).values_list('id', 'network__region')
    parallel_tasks = [
        delete_openstack_subnet.si(
            subnet_id, region, project_id,
        ) for (subnet_id, region) in subnets
    ]
    celery.group(parallel_tasks).apply_async()


@app.task(bind=True, max_retries=settings.TASK_RETRIES, name='Delete openstack subnet', resource_type='Subnet')
def delete_openstack_subnet(self, subnet_id, region, project_id):
    del self  # unused

    project = Project.with_admin_session(project_id, cache=AUTH_CACHE)
    Subnet(subnet_id=subnet_id, api_session=project.api_session).delete(region=region)


@app.task(bind=True, max_retries=settings.TASK_RETRIES,
          name='Delete all openstack subnetpools', resource_type='Project')
def delete_openstack_project_subnetpools(self, project_id):
    del self  # unused

    subnet_pools = OpenstackSubnetPool.objects.filter(project_id=project_id).values_list('id', 'region')
    parallel_tasks = [
        delete_openstack_subnetpool.si(
            subnet_pool_id, region, project_id,
        ) for (subnet_pool_id, region) in subnet_pools
    ]
    celery.group(parallel_tasks).apply_async()


@app.task(bind=True, max_retries=settings.TASK_RETRIES, name='Delete openstack subnetpool', resource_type='Subnetpool')
def delete_openstack_subnetpool(self, subnet_pool_id, region, project_id):
    del self  # unused

    project = Project.with_admin_session(project_id, cache=AUTH_CACHE)
    SubnetPool(subnet_pool_id=subnet_pool_id, api_session=project.api_session).delete(region=region)


@app.task(bind=True, max_retries=settings.TASK_RETRIES,
          name='Delete all openstack floating ips', resource_type='Project')
def delete_openstack_project_floating_ips(self, project_id):
    del self  # unused

    floating_ips = OpenstackFloatingIp.objects.filter(
        project_id=project_id
    ).values_list(
        'id', 'floating_network__region'
    )
    parallel_tasks = [
        delete_openstack_floating_ip.si(
            floating_ip_id, region, project_id,
        ) for (floating_ip_id, region) in floating_ips
    ]
    celery.group(parallel_tasks).apply_async()


@app.task(bind=True, max_retries=settings.TASK_RETRIES,
          name='Delete openstack floating ip', resource_type='Floating ip')
def delete_openstack_floating_ip(self, floating_ip_id, region, project_id):
    del self  # unused

    project = Project.with_admin_session(project_id, cache=AUTH_CACHE)
    FloatingIp(floating_ip_id=floating_ip_id, api_session=project.api_session).delete(region=region)


@app.task(bind=True, max_retries=settings.TASK_RETRIES, name='Delete all openstack routers', resource_type='Project')
def delete_openstack_project_routers(self, project_id):
    del self  # unused

    routers = OpenstackRouter.objects.filter(project_id=project_id).values_list('id', 'region')
    parallel_tasks = [
        delete_openstack_router.si(
            router_id, region, project_id,
        ) for (router_id, region) in routers
    ]
    celery.group(parallel_tasks).apply_async()


@app.task(bind=True, max_retries=settings.TASK_RETRIES, name='Delete openstack router', resource_type='Router')
def delete_openstack_router(self, router_id, region, project_id):
    del self  # unused

    project = Project.with_admin_session(project_id, cache=AUTH_CACHE)
    Router(router_id=router_id, api_session=project.api_session).delete(region=region)


@app.task(bind=True, max_retries=settings.TASK_RETRIES, name='Move openstack instance', resource_type='instance')
def move_instance_task(self, instance_id: str, destination_project_id: str):
    del self  # unused

    # intentionally let this throw an error to fail task if UUID not found in DB
    db_instance = ModelInstance.objects.get(id=instance_id)
    api_instance = Instance.with_admin_session(instance=db_instance)
    destination_project = OpenstackProject.objects.get(project_id=destination_project_id)

    identity_admin_api = IdentityAdminApi()

    unique_name = '{}.{}.{}'.format('move', api_instance.instance.id, uuid4())
    if api_instance.instance.status == 'active':
        api_instance.stop()
        if not wait_for(
            lambda: ModelInstance.objects.get(id=api_instance.instance.id).status == 'stopped',
            max_time=300,
        ):
            raise InstanceTaskException(_('Move instance: failed to stop source instance'))
        api_instance.instance.refresh_from_db()

    api_instance.create_snapshot(unique_name)
    if not wait_for(
        lambda: ModelImage.objects.filter(name=unique_name).count() > 0,
        max_time=300,
    ):
        raise InstanceTaskException(_('Move instance: failed to create source instance snapshot'))
    if not wait_for(
        lambda: ModelImage.objects.filter(name=unique_name).first().status == OpenStackImageStatus.ACTIVE,
        max_time=300,
    ):
        raise InstanceTaskException(_('Move instance: failed to create source instance snapshot'))

    db_image = ModelImage.objects.get(name=unique_name)
    os_image = APIImages(api_session=identity_admin_api.session).get(image=db_image)  # type: APIImage
    os_image.set_visibility(visibility=OpenStackImageVisibility.SHARED)
    os_image.create_member(member_project_id=destination_project.project_id)

    nics = []
    for port in OpenstackPort.objects.filter(device_id=api_instance.instance.id).all():
        if port.network:
            nic = {
                'net-id': port.network.id,
            }
            if len(port.fixed_ips) > 0:
                api_port = APIPorts(api_session=identity_admin_api.session).get(port=port)  # type: APIPort
                args = {
                    'region': api_instance.instance.region,
                    'fixed_ips': [port.fixed_ips[0]]
                }
                api_port.remove_ip(
                    kwargs=args
                )
                nic['v4-fixed-ip'] = port.fixed_ips[0]['ip_address']
                del port.fixed_ips[0]
                port.save()
            nics.append(nic)

    new_instance_id = create_instance_task(
        volume_id=None,
        project_id=destination_project.project_id,
        project_domain_id=destination_project.project_domain_id,
        region_name=api_instance.instance.region,
        name=api_instance.instance.name,
        image=db_image.id,
        flavor=api_instance.instance.flavor_id,
        admin_pass=None,
        nics=nics,
        key_name=None,
        key_content=None,
        block_device_mapping_v2=None,
        block_device_mapping=None
    )

    if not wait_for(lambda: ModelInstance.objects.filter(id=new_instance_id).count() > 0, max_time=600):
        raise InstanceTaskException(_('Move instance: failed to create instance from snapshot'))

    if not wait_for(lambda: ModelInstance.objects.filter(id=new_instance_id).first().status == 'active', max_time=600):
        raise InstanceTaskException(_('Move instance: failed to create instance from snapshot'))

    if not wait_for(lambda: not ModelInstance.objects.filter(id=new_instance_id).first().task_state, max_time=600):
        raise InstanceTaskException(_('Move instance: failed to create instance from snapshot'))

    os_image.delete()

    for port in OpenstackPort.objects.filter(device_id=api_instance.instance.id).all():
        if port.network:
            new_instance_port = OpenstackPort.objects.filter(
                device_id=new_instance_id,
                network__id=port.network.id
            ).first()
            if new_instance_port:
                api_port = APIPorts(api_session=identity_admin_api.session).get(port=port)  # type: APIPort
                new_instance_api_port = APIPorts(
                    api_session=identity_admin_api.session
                ).get(port=new_instance_port)  # type: APIPort
                for index in range(len(port.fixed_ips)):
                    args = {
                        'region': api_instance.instance.region,
                        'fixed_ips': [port.fixed_ips[index]]
                    }
                    api_port.remove_ip(
                        kwargs=args
                    )
                    new_instance_api_port.add_ip(
                        kwargs=args
                    )

    api_instance.rename('{} ({})'.format(api_instance.instance.name, _('MOVED')))

    return True


@app.task(max_retries=settings.TASK_RETRIES, name='Create instance from ISO')
def create_instance_from_iso_task(
        volume_id, project_id, project_domain_id, region_name, name, image, flavor, nics, block_device_mapping_v2,
        block_device_mapping, user_data, admin_pass=None, key_name=None, key_content=None, **create_args
):
    boot_image_id = image
    identity_admin_api = IdentityAdminApi()

    # wait for image
    if not wait_for(lambda: Image.objects.filter(id=boot_image_id).first().status == OpenStackImageStatus.ACTIVE, 600):
        raise InstanceTaskException(_('Upload image failed '))
    region = OpenstackRegion.objects.get(id=region_name)
    boot_image_model = Image.objects.get(id=boot_image_id)
    unique_name = '{}'.format(uuid4())
    os_image_api = Images(api_session=identity_admin_api.session)

    # copy properties starting with hw_ to new image
    extra_properties = {}
    prefixes = getattr(settings, 'OPENSTACK_CREATE_FROM_ISO_PROPERTY_PREFIXES', [])
    for property_name in boot_image_model.properties:  # type: str
        for prefix in prefixes:
            if property_name.startswith(prefix):
                extra_properties[property_name] = boot_image_model.properties[property_name]

    owner = project_id if project_id else identity_admin_api.project_id
    disk_format = getattr(settings, 'OPENSTACK_CREATE_FROM_ISO_IMAGE_TYPE', 'raw')

    try:
        new_image = os_image_api.create(
            owner=owner,
            name=unique_name,
            min_disk=1,
            min_ram=1,
            container_format='bare',
            disk_format=disk_format,
            visibility='community',
            protected=False,
            architecture=boot_image_model.architecture,
            os_distro=boot_image_model.os_distro,
            os_version=boot_image_model.os_version,
            region=region,
            hypervisor_type=boot_image_model.hypervisor_type,
            file=None,
            url=None,
            source=None,
            properties=extra_properties,
        )
    except Exception as e:
        del e  # unused
        LOG.exception(
            'Create instance failed. (owner: {}, disk_format: {}, extra_properties: {}'.format(
                owner, disk_format, extra_properties
            )
        )
        return None
    else:
        try:
            if disk_format == 'qcow2':
                upload_empty_qcow2_image(new_image.id, region_name=region_name, disk_size_in_bytes=1)
            else:
                upload_zero_filled_image(new_image.id, region_name=region_name, length_in_bytes=1)
        except Exception as e:
            LOG.exception('Failed to create temporary image when booting from iso: {}'.format(e))
            try:
                db_image = Image.objects.get(id=new_image.id)
                os_image_api.get(image=db_image).delete()
            except Exception as e:
                LOG.exception('Failed to delete image: {}'.format(e))
            return None

        instance_id = create_instance_task(
            volume_id=volume_id, project_id=project_id, project_domain_id=project_domain_id, region_name=region_name,
            name=name, image=new_image.id, flavor=flavor, admin_pass=admin_pass, nics=nics, key_name=key_name,
            key_content=key_content, block_device_mapping_v2=block_device_mapping_v2, user_data=user_data,
            block_device_mapping=block_device_mapping, **create_args,
        )

        activity_helper.add_current_activity_params(object_id=instance_id)

        if not wait_for(lambda: ModelInstance.objects.filter(id=instance_id).first(),
                        max_time=300):
            raise InstanceTaskException(_('Failed to create instance'))
        if not wait_for(lambda: ModelInstance.objects.filter(id=instance_id).first().status == 'active',
                        max_time=300):
            raise InstanceTaskException(_('Failed to create instance'))
        if not wait_for(lambda: not ModelInstance.objects.filter(id=instance_id).first().task_state,
                        max_time=300):
            raise InstanceTaskException(_('Failed to create instance'))

        try:
            db_image = Image.objects.get(id=new_image.id)
            os_image_api.get(image=db_image).delete()
        except Exception as e:
            LOG.exception('Failed to delete image: {}'.format(e))

        instance_model = ModelInstance.objects.get(id=instance_id)
        instance_model.booted_from_iso = True
        instance_model.save()
        instance_api = Instance.with_admin_session(instance=instance_model)
        instance_api.rescue(image=boot_image_id)

        signal_boot_from_iso.delay(instance_id=instance_id, is_new_instance=True)

        return instance_id


@app.task(max_retries=settings.TASK_RETRIES, name='Signal boot from iso')
def signal_boot_from_iso(instance_id, is_new_instance: bool = False):
    if wait_for(
            lambda: ModelInstance.objects.filter(id=instance_id).first().status == InstanceStatus.BOOTED_FROM_ISO,
            max_time=300,
    ):
        instance_boot_from_iso.send(sender=__name__, instance_id=instance_id, is_new_instance=is_new_instance)


@app.task(
    bind=True,
    throws=(designate_exceptions.Base, designate_exceptions.RemoteError,),
    max_retries=settings.TASK_RETRIES,
    name='Set default PTR',
    resouce_type='Port'
)
def set_default_ptr(self, region_name, fixed_ips=None, on_port_update=False, port_id=None):
    del self  # unused
    if on_port_update:
        # on port update, compare ips already existing in db with those received from openstack, and set default
        # PTR for those that are not in db (newly allocated ips)
        if port_id:
            try:
                db_port = OpenstackPort.objects.get(id=port_id)
            except OpenstackPort.DoesNotExist:
                pass
            else:
                received_existing_ips = dict()  # used to hold ips received from openstack that are also in our db
                db_existing_ips = dict()  # used to hold ips existing in current ports
                for fixed_ip in db_port.fixed_ips:
                    db_existing_ips[fixed_ip.get('ip_address', 'invalid')] = True
                for fixed_ip in fixed_ips:
                    ip_address = fixed_ip.get('ip_address', None)
                    if ip_address:
                        if db_existing_ips.get(ip_address, None):
                            # ip already exists, do not override PTR
                            received_existing_ips[ip_address] = True
                        else:
                            # this is a newly allocated ip, set default PTR
                            try:
                                ptr_format_for_ip = get_default_ptr_format(ip=ip_address)
                                if ptr_format_for_ip is not None:
                                    create_or_update_ptr(
                                        ip=ip_address,
                                        record=ptr_format_for_ip,
                                        region_name=region_name
                                    )
                            except (designate_exceptions.Base, designate_exceptions.RemoteError) as e:
                                LOG.error('Error when trying to set default PTR: {}'.format(str(e)))
                                raise e
                # now check if there are de-allocated ips (existent in db but not received from openstack)
                for db_existing_ip, value in db_existing_ips.items():
                    if db_existing_ip != 'invalid':
                        if received_existing_ips.get(db_existing_ip, None):
                            pass
                        else:
                            # this is a de-allocated ip, set default PTR
                            try:
                                ptr_format_for_ip = get_default_ptr_format(ip=db_existing_ip)
                                if ptr_format_for_ip is not None:
                                    create_or_update_ptr(
                                        ip=db_existing_ip,
                                        record=ptr_format_for_ip,
                                        region_name=region_name
                                    )
                            except (designate_exceptions.Base, designate_exceptions.RemoteError) as e:
                                LOG.error('Error when trying to set default PTR: {}'.format(str(e)))
                                raise e
    else:
        # set default PTR for given ips
        for fixed_ip in fixed_ips:
            ip_address = fixed_ip.get('ip_address', None)
            if ip_address:
                try:
                    ptr_format_for_ip = get_default_ptr_format(ip=ip_address)
                    if ptr_format_for_ip is not None:
                        create_or_update_ptr(
                            ip=ip_address,
                            record=ptr_format_for_ip,
                            region_name=region_name
                        )
                except (designate_exceptions.Base, designate_exceptions.RemoteError) as e:
                    LOG.error('Error when trying to set default PTR: {}'.format(str(e)))
                    raise e


@app.task(
    bind=True,
    max_retries=settings.TASK_RETRIES,
    name='Hypervisors background synchronization',
    resource_type='Hypervisor',
)
def sync_hypervisors(self):
    del self  # unused
    now = utcnow()
    timestamp = now.isoformat()
    deletion_timestamp = (now - timedelta(hours=1)).isoformat()
    hh = HypervisorSyncHandler()
    version_to_delete = hh.get_version(deletion_timestamp)
    all_regions = sync_regions(auth_cache=AUTH_CACHE)
    try:
        for region in all_regions:
            for hypervisor in Hypervisors(api_session=IdentityAdminApi().session).get_hypervisors(region=region.id):
                hh.create_or_update(data=hypervisor, region=region.id, timestamp=timestamp)
            # delete hypervisors that were not synced in a version represented by a time less than one hour ago
            delete_filter = {'{}__lt'.format(hh.version_field): version_to_delete, 'region': region.id}
            Hypervisor.objects.filter(**delete_filter).delete()
    except Exception as e:
        LOG.error(str(e))
        return


@app.task(bind=True, max_retries=settings.TASK_RETRIES, name='Clusters background synchronization',
          resouce_type='Cluster')
def sync_clusters_in_background(self, project_id=None, region=None):
    """Used to sync clusters once a notification arrives"""
    del self  # unused
    sync_coe(region_id=region, auth_cache=AUTH_CACHE, project_id=project_id)
