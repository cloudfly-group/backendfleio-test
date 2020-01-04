import logging

from django.db.models import Q
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from novaclient.api_versions import APIVersion
from novaclient.client import exceptions
from novaclient.exceptions import NotFound
from novaclient.exceptions import VersionNotFoundForAPIMethod
from retrying import retry

from fleio.core.features import active_features
from fleio.openstack.api.neutron import create_security_group_if_missing
from fleio.openstack.api.neutron import neutron_client
from fleio.openstack.api.nova import nova_client
from fleio.openstack.api.session import get_session
from fleio.openstack.exceptions import ObjectNotFound
from fleio.openstack.instances.instance_status import InstancePowerState
from fleio.openstack.instances.instance_status import InstanceStatus
from fleio.openstack.instances.instance_status import InstanceTask
from fleio.openstack.models import FloatingIp
from fleio.openstack.models import Image
from fleio.openstack.models import Network
from fleio.openstack.models import OpenstackInstanceFlavor
from fleio.openstack.models import Port
from fleio.openstack.networking.api import FloatingIps
from fleio.openstack.settings import plugin_settings
from .keypairs import Keypairs

LOG = logging.getLogger(__name__)


def retry_if_result_is_falsy(result):
    return not result


class Instances(object):
    def __init__(self, api_session):
        """
        :type api_session: keystoneauth1.session.Session
        """
        self.api_session = api_session

    def get(self, db_instance):
        """
        :type db_instance: fleio.openstack.models.Instance
        :rtype: Instance
        """
        return Instance(db_instance, api_session=self.api_session)

    def create(self, name, image, flavor, admin_pass, nics, region_name, user_data, key_name=None, key_content=None,
               block_device_mapping=None, block_device_mapping_v2=None):
        """
        :type name: str or unicode, the instance name
        :type image: str or unicode, the flavor id
        :type flavor: str or unicode
        :type admin_pass: str or unicode, the root/admin password for the instance
        :type nics: dict, network interfaces for the instance
        :type key_name: str or unicode, the ssh keypair name
        :type region_name: str or unicode
        :type key_content: str or unicode
        :type block_device_mapping: dict
        :type block_device_mapping_v2: list of dicts

        :rtype: :class:`novaclient.v2.servers.Server`
        """
        # Create the ssh keypair in Nova if needed
        if key_name and key_content:
            kp = Keypairs(api_session=self.api_session, region_name=region_name)
            nova_key_name = kp.create_if_missing(name=key_name, public_key=key_content)
        else:
            nova_key_name = None
        # Create the default security group if Needed
        # TODO(tomo): Try to deal with the default security group in another way
        sgid = create_security_group_if_missing(api_session=self.api_session, region=region_name)

        nc = nova_client(api_session=self.api_session, region_name=region_name)

        params = dict(
            name=name,
            image=image,
            flavor=flavor,
            nics=nics,
            security_groups=[sgid],
            key_name=nova_key_name,
            block_device_mapping=block_device_mapping,
            block_device_mapping_v2=block_device_mapping_v2
        )
        if plugin_settings.force_config_drive_for_instance_creation:
            params['config_drive'] = True
        if admin_pass:
            params['admin_pass'] = admin_pass
        if user_data:
            params['userdata'] = user_data
        return nc.servers.create(**params)


class Instance(object):
    REBOOT_SOFT, REBOOT_HARD = 'SOFT', 'HARD'
    STATUS = InstanceStatus
    TASK = InstanceTask

    def __init__(self, instance, api_session=None):
        """
        :type instance: fleio.openstack.models.Instance
        """
        self.instance = instance
        self.api_session = api_session
        self._api_instance = None

    @staticmethod
    def _get_admin_session():
        return get_session(auth_url=plugin_settings.AUTH_URL,
                           project_id=plugin_settings.user_project_id,
                           project_domain_id=plugin_settings.project_domain_id,
                           admin_username=plugin_settings.USERNAME,
                           admin_password=plugin_settings.PASSWORD,
                           admin_domain_id=plugin_settings.USER_DOMAIN_ID,
                           timeout=plugin_settings.TIMEOUT)

    @classmethod
    def with_admin_session(cls, instance):
        return cls(instance, api_session=cls._get_admin_session())

    @cached_property
    def admin_api(self):
        """
        :rtype: novaclient.v2.client.Client
        """
        admin_session = self._get_admin_session()
        assert admin_session is not None, 'Unable to use admin_api without a Keystoneauth session'

        return nova_client(api_session=admin_session,
                           region_name=self.instance.region,
                           extensions=True)

    @cached_property
    def compute_api(self):
        """
        :rtype: novaclient.v2.client.Client
        """
        assert self.api_session is not None, 'Unable to use compute_api without a Keystoneauth session'

        return nova_client(api_session=self.api_session,
                           region_name=self.instance.region,
                           extensions=True)

    @property
    def neutron_api(self):
        assert self.api_session is not None, 'Unable to use neutron api without a Keystone session'
        return neutron_client(api_session=self.api_session,
                              region_name=self.instance.region)

    @property
    def api_instance(self):
        if self._api_instance is None:
            self.refresh_from_api()
        return self._api_instance

    def refresh_from_api(self):
        self._api_instance = self.compute_api.servers.get(server=self.uuid)

    @property
    def is_deleting(self):
        if self.instance.task_state:
            return self.instance.task_state.lower() == self.TASK.DELETING.lower()
        else:
            return False

    @property
    def status(self):
        return self.instance.status

    @cached_property
    def uuid(self):
        return self.instance.id

    def get_power_state(self):
        # TODO(tomo): Try to store the power state in DB to avoid an API call ?
        return getattr(self.api_instance, 'OS-EXT-STS:power_state', 0)

    def get_task_state(self):
        # TODO(adrian): we also have this in DB. Is it ok to read it from DB?
        # return getattr(self.api_instance, 'OS-EXT-STS:task_state', None)
        return self.instance.task_state

    def can_be_stopped(self):
        if self.get_task_state() != InstanceTask.POWERING_OFF:
            if self.get_power_state() == InstancePowerState.RUNNING:
                return True
        return False

    def can_be_started(self):
        if self.get_task_state() not in (InstanceTask.POWERING_ON,
                                         InstanceTask.RESUMING,
                                         InstanceTask.DELETING):
            if self.get_power_state() in (InstancePowerState.SHUTDOWN,
                                          InstancePowerState.SHUTOFF):
                return True
        return False

    def rebuild(self, instance_id, image_id, password=None, name=None, userdata=None):
        self.compute_api.servers.rebuild(
            server=instance_id,
            image=image_id,
            password=password,
            name=name,
            userdata=userdata,
        )

    def interface_list(self):
        return self.compute_api.servers.interface_list(server=self.uuid)

    def update_status(self):
        """Get the instance status from OpenStack and update in db."""
        status = getattr(self.api_instance, 'OS-EXT-STS:vm_state', 'unknown')
        instance_task = getattr(self.api_instance, 'OS-EXT-STS:task_state', None)
        self.instance.update_status(status, instance_task)

    def start(self):
        self.compute_api.servers.start(server=self.uuid)
        if self.instance.stopped_by_fleio:
            self.instance.stopped_by_fleio = False
            self.instance.save()

    def stop(self, stopped_by_fleio=False):
        self.compute_api.servers.stop(server=self.uuid)
        if stopped_by_fleio:
            self.instance.stopped_by_fleio = stopped_by_fleio
            self.instance.save()

    def reboot(self, reboot_type=REBOOT_SOFT):
        self.compute_api.servers.reboot(server=self.uuid, reboot_type=reboot_type)

    def rename(self, new_name):
        self.compute_api.servers.update(server=self.uuid, name=new_name)

    def rescue(self, image=None, password=None):
        return self.compute_api.servers.rescue(server=self.uuid, image=image, password=password)

    def unrescue(self):
        return self.compute_api.servers.unrescue(server=self.uuid)

    def resize(self, flavor):
        return self.compute_api.servers.resize(server=self.uuid, flavor=flavor)

    def confirm_resize(self):
        self.compute_api.servers.confirm_resize(server=self.uuid)

    def revert_resize(self):
        self.compute_api.servers.revert_resize(server=self.uuid)

    def system_log(self, length=30):
        return self.compute_api.servers.get_console_output(server=self.uuid, length=length)

    def get_vnc_url(self, console_type='novnc'):
        return self.compute_api.servers.get_vnc_console(server=self.uuid, console_type=console_type)

    def get_spice_url(self, console_type='spice-html5'):
        return self.compute_api.servers.get_spice_console(server=self.uuid, console_type=console_type)

    def lock(self):
        return self.compute_api.servers.lock(server=self.uuid)

    def unlock(self):
        return self.compute_api.servers.unlock(server=self.uuid)

    def suspend(self):
        return self.compute_api.servers.suspend(server=self.uuid)

    def resume(self):
        return self.compute_api.servers.resume(server=self.uuid)

    def delete(self):
        """Delete the instance from both OpenStack and local db"""

        ports_ids = []
        try:
            ports = self.instance.ports.all()
            for port in ports:
                ports_ids.append(port.id)
        except Exception as e:
            LOG.debug(e)
        try:
            self.compute_api.servers.delete(server=self.uuid)
        except NotFound:
            self.instance.delete()
        else:
            # Delete all instance ports after deleting the instance
            # Nova only deletes the ports associated when creating the instance
            for port_id in ports_ids:
                try:
                    self.neutron_api.delete_port(port=port_id)
                except Exception as e:
                    del e  # we are not interested in exception here

    def attach_volume(self, volume_id, device=None):
        return self.compute_api.volumes.create_server_volume(server_id=self.uuid,
                                                             volume_id=volume_id,
                                                             device=device)

    def detach_volume(self, volume_id):
        return self.compute_api.volumes.delete_server_volume(server_id=self.uuid,
                                                             volume_id=volume_id)

    def list_attached_volumes(self):
        return self.compute_api.volumes.get_server_volumes(server_id=self.uuid)

    def diagnostics(self):
        return self.compute_api.servers.diagnostics(server=self.uuid)

    def create_snapshot(self, name):
        snapshot_uuid = self.compute_api.servers.create_image(server=self.uuid, image_name=name)
        return snapshot_uuid

    def rebuild_images(self):
        """
        Return a queryset containing the images allowed for rebuild.
        :rtype: django.db.models.query.Queryset
        """
        # TODO(tomo): Allow image sharing between clients ?
        templates = Image.objects.filter(status='active').filter(
            Q(type__in=['template', 'application'], region=self.instance.region, project__isnull=True))
        client_images = Image.objects.filter(status='active').filter(Q(
            type__in=['snapshot', 'backup', 'deleted'],
            region=self.instance.region,
            project_id=self.instance.project_id))
        return templates, client_images

    def rescue_images(self):
        # TODO(tomo): Select only images available for rescue!
        return self.rebuild_images()

    def resize_flavors(self, staff_request=False):
        """
        Return a queryset containing the flavors allowed for resize.
        Filter by client groups if the instance has a project associated
        with a Fleio client.
        :rtype: django.db.models.query.Queryset
        """
        project_id = self.instance.project_id
        show_in_fleio = True
        if staff_request:
            show_in_fleio = None
        try:
            instance_related_image = self.instance.image
        except Image.DoesNotExist:
            instance_related_image = None
        if project_id:
            qs = OpenstackInstanceFlavor.objects.get_for_project(
                project_id=project_id,
                disabled=False,
                region=self.instance.region,
                deleted=False,
                is_public=True,
                show_in_fleio=show_in_fleio
            ).order_by('memory_mb')
        else:
            qs = OpenstackInstanceFlavor.objects.filter(
                disabled=False,
                region=self.instance.region,
                deleted=False,
                is_public=True,
                show_in_fleio=show_in_fleio
            ).order_by('memory_mb')
        if instance_related_image:
            if instance_related_image.flavors.count() + instance_related_image.flavor_groups.count() > 0:
                qs = qs.filter(
                    Q(images__id=instance_related_image.id) | Q(flavor_group__images__id=instance_related_image.id)
                )

        if not staff_request and not active_features.is_enabled(
                'openstack.instances.resize.allow_resize_to_less_disk_space'
        ):
            qs = qs.filter(root_gb__gte=self.instance.flavor.root_gb)

        return qs

    def get_public_port_or_none(self):
        """Retrieve the port connected to the public network."""
        if hasattr(self.instance, 'ports'):
            public_nets = Network.objects.filter(router_external=True).values('id')
            if public_nets:
                public_port = self.instance.ports.filter(network_id__in=public_nets).first()
                if public_port is not None:
                    return public_port
            return self.instance.ports.first()

    def get_actions(self):
        """Retrieve the instances actions."""
        # TODO(erno): paginate list
        resources = self.compute_api.instance_action.list(self.uuid)
        result = list()
        resources.reverse()
        for resource in resources:
            resource_dict = resource.to_dict()
            resource_dict.pop('instance_uuid', None)
            resource_dict.pop('project_id', None)
            resource_dict.pop('user_id', None)
            start_time = parse_datetime(resource_dict['start_time'])
            start_time = start_time.replace(tzinfo=timezone.utc)
            resource_dict['start_time'] = start_time

            result.insert(0, resource_dict)
        return result

    def get_action_details(self, request_id):
        action_details = self.compute_api.instance_action.get(self.uuid, request_id)

        for event in action_details.events:
            start_time = parse_datetime(event['start_time'])
            start_time = start_time.replace(tzinfo=timezone.utc)
            event['start_time'] = start_time

            if event['finish_time'] is not None:
                finish_time = parse_datetime(event['finish_time'])
                finish_time = finish_time.replace(tzinfo=timezone.utc)
                event['finish_time'] = finish_time

        action_details_dict = action_details.to_dict()

        start_time = parse_datetime(action_details_dict['start_time'])
        start_time = start_time.replace(tzinfo=timezone.utc)
        action_details_dict['start_time'] = start_time

        return action_details_dict

    def change_password(self, password):
        """
        Change the administrator password.
        :param password: The new password
        :type password: string
        """
        return self.compute_api.servers.change_password(server=self.uuid, password=password)

    def reset_state(self, state):
        """
        Reset the state of the instance to active or error.
        :param state: The new state
        :type state: string
        """
        return self.admin_api.servers.reset_state(server=self.uuid, state=state)

    @retry(retry_on_result=retry_if_result_is_falsy, wait_fixed=2000, stop_max_attempt_number=30)
    def wait_for_instance_deleted(self):
        try:
            self.refresh_from_api()
        except exceptions.NotFound:
            return True
        return False

    def shelve(self):
        self.compute_api.servers.shelve(server=self.uuid)

    def unshelve(self):
        self.compute_api.servers.unshelve(server=self.uuid)

    def add_floating_ip(self, floating_ip, fixed_ip=None):
        try:
            if fixed_ip:
                self.compute_api.servers.add_floating_ip(server=self.uuid, address=floating_ip, fixed_address=fixed_ip)
            else:
                self.compute_api.servers.add_floating_ip(server=self.uuid, address=floating_ip)
        # TODO(erno): removed in openstack pike, refactor logic after we support only opestack >= pike
        except (VersionNotFoundForAPIMethod, AttributeError):
            try:
                f_ip = FloatingIp.objects.get(floating_ip_address=floating_ip)
            except (FloatingIp.DoesNotExist, FloatingIp.MultipleObjectsReturned):
                raise ObjectNotFound('Floating ip not found')
            if fixed_ip:
                port = Port.objects.filter(device_id=self.uuid, fixed_ips__contains=str(fixed_ip)).first()
            else:
                port = Port.objects.filter(device_id=self.uuid).first()
            if port:
                FloatingIps(self.api_session).associate_ip(f_ip.id, port.id, fixed_ip, self.instance.region)
            else:
                raise ObjectNotFound('No ports found to associate')

    def remove_floating_ip(self, floating_ip):
        try:
            self.compute_api.servers.remove_floating_ip(server=self.uuid, address=floating_ip)
        # TODO(erno): removed in openstack pike, refactor logic after we support only OpenStack >= pike
        except (VersionNotFoundForAPIMethod, AttributeError):
            try:
                f_ip = FloatingIp.objects.get(floating_ip_address=floating_ip)
            except (FloatingIp.DoesNotExist, FloatingIp.MultipleObjectsReturned):
                raise ObjectNotFound('Floating ip not found')
            FloatingIps(self.api_session).dissociate_ip(f_ip.id, self.instance.region)

    def migrate(self, kwargs):
        api_version = APIVersion(plugin_settings.COMPUTE_API_VERSION)
        if kwargs.get('live_migrate', None):
            if api_version <= APIVersion('2.24'):
                self.compute_api.servers.live_migrate(
                    server=self.uuid,
                    host=kwargs['hypervisor'],
                    block_migration=kwargs['block_migration'],
                    disk_over_commit=kwargs.get('over_commit', False),
                )
            elif api_version <= APIVersion('2.29'):
                self.compute_api.servers.live_migrate(
                    server=self.uuid,
                    host=kwargs['hypervisor'],
                    block_migration=kwargs['block_migration'],
                )
            elif api_version <= APIVersion('2.67'):
                self.compute_api.servers.live_migrate(
                    server=self.uuid,
                    host=kwargs['hypervisor'],
                    block_migration=kwargs['block_migration'],
                    force=kwargs.get('over_commit', False),
                )
            else:
                self.compute_api.servers.live_migrate(
                    server=self.uuid,
                    host=kwargs['hypervisor'],
                    block_migration=kwargs['block_migration'],
                )
        else:
            if api_version < APIVersion('2.56'):
                self.compute_api.servers.migrate(self.uuid)
            else:
                self.compute_api.servers.migrate(self.uuid, host=kwargs['hypervisor'])

    def abort_migrate(self):
        migration_list = self.compute_api.server_migrations.list(self.uuid)
        if migration_list:
            self.compute_api.server_migrations.live_migration_abort(self.uuid, migration_list[0].id)
        else:
            raise ObjectNotFound(_('Migration not found'))

    def associate_security_group(self, group):
        self.compute_api.servers.add_security_group(server=self.uuid, security_group=group)

    def dissociate_security_group(self, group):
        self.compute_api.servers.remove_security_group(server=self.uuid, security_group=group)
