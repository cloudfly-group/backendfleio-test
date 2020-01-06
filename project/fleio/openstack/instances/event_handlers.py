from __future__ import unicode_literals

import logging
import copy
import hashlib

from typing import Optional, Tuple

from fleio.openstack.tasks import sync_hypervisors
from fleio.openstack.api.identity import IdentityAdminApi
from fleio.openstack.api.nova import nova_client

from fleio.openstack.instances import serializers
from fleio.openstack.instances.instance_status import InstancePowerState
from fleio.openstack.instances.instance_status import InstanceStatus
from fleio.openstack.instances.instance_status import InstanceTask
from fleio.openstack.sync.handler import BaseHandler

from fleio.openstack.models import Instance
from fleio.openstack.models import Image
from fleio.openstack.models import Hypervisor

LOG = logging.getLogger(__name__)


class InstanceEventHandler(BaseHandler):
    serializer_class = serializers.InstanceSyncSerializer
    version_field = 'sync_version'

    def __init__(self):
        self.event_handlers = {'compute.instance.create.end': self.create_or_update,
                               'compute.instance.update': self.create_or_update,
                               'compute.instance.power_off.end': self.create_or_update,
                               'compute.instance.power_on.end': self.create_or_update,
                               'compute.instance.resize.end': self.create_or_update,
                               'compute.instance.resize.revert.end': self.create_or_update,
                               'compute.instance.finish_resize.end': self.create_or_update,
                               'compute.instance.resize.confirm.end': self.create_or_update,
                               'compute.instance.rescue.end': self.create_or_update,
                               'compute.instance.unrescue.end': self.create_or_update,
                               'compute.instance.rebuild.end': self.create_or_update,
                               'compute.instance.migrate.end': self.create_or_update,
                               'compute.instance.shutdown.end': self.create_or_update,
                               'compute.instance.delete.end': self.delete,
                               'compute.instance.create.start': self.create_or_update,
                               'compute.instance.delete.start': self.create_or_update}

        self.error_handlers = {}
        self.admin_api_session = IdentityAdminApi().session

    @staticmethod
    def _generate_host_id(project_id: str, host_name: str) -> str:
        to_hash = '{}{}'.format(project_id, host_name)
        to_hash = to_hash.encode('utf-8')
        sha_hash = hashlib.sha224(to_hash)
        return sha_hash.hexdigest()

    @staticmethod
    def _get_db_hypervisor_name(received_host: Optional[str], region: str) -> Optional[str]:
        """checks if the hypervisor exists in db, otherwise create it in the database and finally return host name"""
        hypervisor = Hypervisor.objects.filter(host_name=received_host, region=region).first()
        if hypervisor:
            return hypervisor.host_name
        # hypervisor does not exist in db, resynchronize hypervisors and return received_host
        sync_hypervisors.delay()
        return received_host

    def _get_hypervisor_host_name(self, instance_id: str, region: str) -> Optional[str]:
        """gets host name from 'OS-EXT-SRV-ATTR:host' attribute found on instances"""
        nc = nova_client(api_session=self.admin_api_session, region_name=region)
        try:
            nc_instance = nc.servers.get(instance_id)
        except Exception as e:
            LOG.error(str(e))
            return None
        return getattr(nc_instance, 'OS-EXT-SRV-ATTR:host', None)

    def resolve_host_id_and_host_name_from_hashed_value(self, sha_value, instance_id, region) -> Tuple[str, str]:
        """return host id hashed value along with host name after it is found"""
        resolved_host_name = self._get_hypervisor_host_name(instance_id=instance_id, region=region)
        return sha_value, resolved_host_name

    def resolve_host_id_and_host_name_from_name(self, received_hostname, region, project_id,
                                                db_hypervisor: Hypervisor = None) -> Tuple[str, str]:
        """return host id hashed value (generated using the name and project id) and the host name"""
        if db_hypervisor:
            resolved_host_name = db_hypervisor.host_name
        else:
            resolved_host_name = self._get_db_hypervisor_name(received_host=received_hostname, region=region)
        resolved_host_id = self._generate_host_id(
            project_id=project_id,
            host_name=resolved_host_name
        )
        return resolved_host_id, resolved_host_name

    def serialize(self, data, region, timestamp):
        instance = copy.deepcopy(data)
        instance['id'] = instance['instance_id']
        instance['region'] = region
        instance[self.version_field] = self.get_version(timestamp)
        instance['project_id'] = instance['tenant_id']
        instance['name'] = instance['display_name']
        if 'fixed_ips' in instance:
            instance['addresses'] = instance['fixed_ips']
        instance['accessIPv4'] = instance['access_ip_v4']
        instance['accessIPv6'] = instance['access_ip_v6']
        instance['flavor'] = instance['instance_flavor_id']

        # resolve hypervisor id and host name because sometimes notification comes as an id (sha224 hashed using the
        # project id and host name) sometimes as a name
        received_host = instance['host']
        db_instance = Instance.objects.filter(id=instance['id']).first()
        resolved_host_id = None
        resolved_host_name = None

        if received_host and db_instance and db_instance.host_name == received_host:
            # if received host is actually the host name, save it as it is and generate just the hostId
            resolved_host_id, resolved_host_name = self.resolve_host_id_and_host_name_from_name(
                received_hostname=received_host, region=region, project_id=instance['project_id']
            )
        elif received_host:
            db_hypervisor = Hypervisor.objects.filter(host_name=received_host).first()
            if db_hypervisor:
                # if received host is related to a db hypervisor, it means this is actually the host name
                resolved_host_id, resolved_host_name = self.resolve_host_id_and_host_name_from_name(
                    received_hostname=received_host,
                    region=region,
                    project_id=instance['project_id'],
                    db_hypervisor=db_hypervisor,
                )
            elif db_instance:
                # if no db_hypervisor found it is either hashed value or a hypervisor not in fleio db
                if ((received_host == db_instance.hostId and not db_instance.host_name) or
                        received_host != db_instance.hostId):
                    # treat case when it is most likely a hashed value
                    resolved_host_id, resolved_host_name = self.resolve_host_id_and_host_name_from_hashed_value(
                        sha_value=received_host, instance_id=instance['id'], region=region
                    )
                else:
                    # treat case when it is actually a host name (may be not existent in fleio hypervisors table)
                    resolved_host_id, resolved_host_name = self.resolve_host_id_and_host_name_from_name(
                        received_hostname=received_host, region=region, project_id=instance['project_id']
                    )

        instance['hostId'] = resolved_host_id if resolved_host_id else received_host
        instance['host_name'] = resolved_host_name if resolved_host_name else None

        if 'image_ref_url' in instance and len(instance['image_ref_url']) > 30:
            image_id = instance['image_ref_url'].split('/')[-1] or None
            image_in_db = None
            # we should find image in db, otherwise it means it is an instance whose
            # related image was deleted
            if image_id:
                image_in_db = Image.objects.filter(id=image_id).first()
            if image_in_db:
                instance['image'] = image_id
            else:
                instance['image'] = None
        # if 'image_meta' in instance and instance['image_meta'].get('base_image_ref', None):
        #     instance['image'] = instance['image_meta']['base_image_ref']
        instance['task_state'] = instance.get('new_task_state', instance.get('state_description', None))
        instance['vm_state'] = instance['state']
        instance['updated'] = timestamp  # FIXME(tomo): we use timestamp, but this is not accurate
        instance['status'] = instance['state']
        if len(instance.get('launched_at', '')) < 10:
            instance['launched_at'] = None
        if len(instance.get('created_at', '')) < 10:
            instance['created'] = None
        else:
            instance['created'] = instance['created_at']
        if len(instance.get('terminated_at', '')) < 10:
            instance['terminated_at'] = None

        # set fleio specific status if needed
        if db_instance and db_instance.booted_from_iso:
            if instance['status'] == InstanceStatus.RESCUED:
                instance['status'] = InstanceStatus.BOOTED_FROM_ISO

            if instance['task_state'] == InstanceTask.RESCUING:
                instance['task_state'] = InstanceTask.BOOTING_FROM_ISO

            if instance['task_state'] == InstanceTask.UNRESCUING:
                instance['task_state'] = InstanceTask.UNMOUNTING_AND_REBOOTING

        return instance

    def delete(self, data, region, timestamp):
        instance_id = data.get('instance_id', None)
        if instance_id is None:
            LOG.error('Unable to delete instance without instance_id: {}'.format(data))
        return super(InstanceEventHandler, self).delete(instance_id, region, timestamp)

    def create_or_update(self, data, region, timestamp):
        if 'state' in data and 'old_state' in data:
            if data['state'] == 'deleted' and data['old_state'] == 'deleted':
                self.delete(data=data, region=region, timestamp=timestamp)
            else:
                super().create_or_update(data=data, region=region, timestamp=timestamp)
        else:
            super().create_or_update(data=data, region=region, timestamp=timestamp)


class VersionedInstanceEventHandler(BaseHandler):
    serializer_class = serializers.InstanceSyncSerializer
    version_field = 'sync_version'

    def __init__(self):
        self.event_handlers = {'instance.create.end': self.create_or_update,
                               'instance.create.start': self.create_or_update,
                               'instance.update': self.create_or_update,
                               'instance.reboot.start': self.create_or_update,
                               'instance.reboot.end': self.create_or_update,
                               'instance.power_off.start': self.create_or_update,
                               'instance.power_off.end': self.create_or_update,
                               'instance.power_on.start': self.create_or_update,
                               'instance.power_on.end': self.create_or_update,
                               'instance.resize.start': self.create_or_update,
                               'instance.resize.end': self.create_or_update,
                               'instance.resize_revert.start': self.create_or_update,
                               'instance.resize_revert.end': self.create_or_update,
                               'instance.resize_finish.start': self.create_or_update,
                               'instance.resize_finish.end': self.create_or_update,
                               'instance.resize.confirm.end': self.create_or_update,
                               'instance.rescue.start': self.create_or_update,
                               'instance.rescue.end': self.create_or_update,
                               'instance.unrescue.end': self.create_or_update,
                               'instance.unrescue.start': self.create_or_update,
                               'instance.rebuild.start': self.create_or_update,
                               'instance.rebuild.end': self.create_or_update,
                               'instance.migrate.end': self.create_or_update,
                               'instance.shutdown.start': self.create_or_update,
                               'instance.shutdown.end': self.create_or_update,
                               'instance.delete.end': self.delete,
                               'instance.delete.start': self.create_or_update,
                               'instance.live_migration_abort.end': self.create_or_update,
                               'instance.live_migration_abort.start': self.create_or_update,
                               'instance.live_migration_rollback.end': self.create_or_update,
                               'instance.live_migration_rollback.start': self.create_or_update,
                               'instance.pause.end': self.create_or_update,
                               'instance.pause.start': self.create_or_update,
                               'instance.unpause.end': self.create_or_update,
                               'instance.unpause.start': self.create_or_update,
                               'instance.restore.end': self.create_or_update,
                               'instance.restore.start': self.create_or_update,
                               'instance.resume.end': self.create_or_update,
                               'instance.resume.start': self.create_or_update,
                               'instance.shelve.end': self.create_or_update,
                               'instance.shelve.start': self.create_or_update,
                               'instance.unshelve.end': self.create_or_update,
                               'instance.unshelve.start': self.create_or_update,
                               'instance.soft_delete.end': self.create_or_update,
                               'instance.soft_delete.start': self.create_or_update,
                               'instance.suspend.end': self.create_or_update,
                               'instance.suspend.start': self.create_or_update}

        self.error_handlers = {'instance.reboot.error': self.create_or_update,
                               'instance.rebuild.error': self.create_or_update,
                               'instance.resize.error': self.create_or_update,
                               'instance.create.error': self.create_or_update}

    def serialize(self, data, region, timestamp):
        instance = copy.deepcopy(data['nova_object.data'])
        instance['id'] = instance['uuid']
        instance['region'] = region
        instance[self.version_field] = self.get_version(timestamp)
        instance['name'] = instance['display_name']
        instance['project_id'] = instance.get('project_id', instance.get('tenant_id', None))
        instance['auto_disk_config'] = instance['auto_disk_config'] != 'MANUAL'
        instance['flavor'] = instance['flavor']['nova_object.data']['flavorid']
        instance['hostId'] = instance['host']
        instance['image'] = instance['image_uuid']
        instance['task_state'] = instance['task_state']
        instance['vm_state'] = instance['power_state']
        created = instance.get('created_at', instance.get('launched_at', None))
        if created:
            instance['created'] = created
        try:
            instance['power_state'] = getattr(InstancePowerState, instance['power_state'].upper())
        except AttributeError:
            instance['power_state'] = 0
        instance['updated'] = instance['updated_at']
        instance['status'] = instance['state']
        if 'fault' in instance and not instance['fault']:
            instance.pop('fault')
        return instance

    def delete(self, data, region, timestamp):
        try:
            instance_id = data['nova_object.data']['uuid']
        except KeyError:
            instance_id = None
            LOG.error('Unable to delete instance without instance_id: {}'.format(data))
        return super(VersionedInstanceEventHandler, self).delete(instance_id, region, timestamp)
