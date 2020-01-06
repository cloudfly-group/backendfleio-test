from __future__ import unicode_literals

import logging

from fleio.openstack.instances import serializers
from fleio.openstack.instances.instance_status import InstanceStatus
from fleio.openstack.instances.instance_status import InstanceTask
from fleio.openstack.models import Instance
from fleio.openstack.models import Image
from fleio.openstack.models import OpenstackInstanceFlavor
from fleio.openstack.sync.handler import BaseHandler


LOG = logging.getLogger(__name__)


class InstanceSyncHandler(BaseHandler):
    serializer_class = serializers.InstanceSyncSerializer
    version_field = 'sync_version'

    @staticmethod
    def get_addresses(addresses):
        result = list()
        for net_label, value_list in iter(addresses.items()):
            for address in value_list:
                new_addr = dict(version=address['version'],
                                vif_mac=address['OS-EXT-IPS-MAC:mac_addr'],
                                floating_ips=list(),
                                label=net_label,
                                address=address['addr'],
                                type=address['OS-EXT-IPS:type'],
                                meta=dict())
                result.append(new_addr)
        return result

    def serialize(self, data, region, timestamp):
        instance = data.to_dict()
        instance['project_id'] = instance['tenant_id']
        instance['region'] = region
        instance[self.version_field] = self.get_version(timestamp)
        instance['flavor'] = data.flavor.get('id', None)
        if not instance['flavor']:
            flavor_name = data.flavor.get('original_name', None) or data.flavor.get('name', None)
            # name is unique for flavor so we can get away with this query
            try:
                flavor = OpenstackInstanceFlavor.objects.get(name=flavor_name, region__id=region)
            except (OpenstackInstanceFlavor.MultipleObjectsReturned, OpenstackInstanceFlavor.DoesNotExist) as e:
                LOG.error('Error getting flavor for instance {0}. Reason {1}'.format(instance.get('id', None), e))
            else:
                instance['flavor'] = flavor.id
        if 'id' in instance.get('image', dict()):
            image_id = instance['image'].get('id', None)
            image_found = None
            if image_id:
                # images were synced before, we should find it in db, otherwise it means it is an instance whose
                # related image was deleted
                image_found = Image.objects.filter(id=image_id).first()
            if image_found:
                instance['image'] = image_id
            else:
                instance['image'] = None
        else:
            instance['image'] = None
        if not len(instance['accessIPv4']):
            instance['accessIPv4'] = None
        if not len(instance['accessIPv6']):
            instance['accessIPv6'] = None
        if not len(instance['config_drive']):
            instance['config_drive'] = False
        # Reshape addresses to be the same as the fixed_ips from events
        instance['addresses'] = self.get_addresses(instance['addresses'])
        instance['availability_zone'] = instance.get('OS-EXT-AZ:availability_zone', None)
        instance['auto_disk_config'] = instance.get('OS-DCF:diskConfig', 'MANUAL') == 'AUTO'
        instance['power_state'] = instance.get('OS-EXT-STS:power_state', 0)
        instance['task_state'] = instance.get('OS-EXT-STS:task_state', None)
        instance['vm_state'] = instance.get('OS-EXT-STS:vm_state', None)
        instance['status'] = instance.get('vm_state', 'unknown')
        instance['volumes_attached'] = instance.get('os-extended-volumes:volumes_attached', list())
        instance['launched_at'] = instance.get('OS-SRV-USG:launched_at', None)

        db_instance = Instance.objects.filter(id=instance['id']).first()

        # set fleio specific status if needed
        if db_instance and db_instance.booted_from_iso:
            if instance['status'] == InstanceStatus.RESCUED:
                instance['status'] = InstanceStatus.BOOTED_FROM_ISO

            if instance['task_state'] == InstanceTask.RESCUING:
                instance['task_state'] = InstanceTask.BOOTING_FROM_ISO

            if instance['task_state'] == InstanceTask.UNRESCUING:
                instance['task_state'] = InstanceTask.UNMOUNTING_AND_REBOOTING

        return instance
