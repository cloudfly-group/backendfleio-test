from __future__ import unicode_literals

import json
import logging
import copy

from fleio.openstack.images import serializers
from fleio.openstack.sync.handler import BaseHandler, retry_on_deadlock

LOG = logging.getLogger(__name__)


class ImageEventHandler(BaseHandler):
    serializer_class = serializers.ImageSyncSerializer
    version_field = 'sync_version'

    def __init__(self):
        # NOTE(tomo): image.send not handled, it may not be needed
        # NOTE(erno): the events image.upload and image.activate were removed because on snapshot delete
        # these notifications can come after image.delete (in notifications version 1)
        self.event_handlers = {'image.create': self.create_or_update,
                               'image.update': self.create_or_update,
                               'image.prepare': self.create_or_update,
                               'image.delete': self.delete}

    def serialize(self, data, region, timestamp):
        improp = data.get('properties', dict())
        owner = data.get('owner', None)
        im_data = copy.deepcopy(data)
        im_data['region_id'] = region
        im_data[self.version_field] = self.get_version(timestamp)
        im_data['instance_uuid'] = improp.get('instance_uuid', None)
        # save volume snapshot id
        im_data['volume_snapshot_uuid'] = None
        if 'block_device_mapping' in improp:
            block_device_mapping = json.loads(improp.get('block_device_mapping', '[]'))
            block_device_mapping_dict = block_device_mapping[0] if len(block_device_mapping) else {}
            im_data['volume_snapshot_uuid'] = block_device_mapping_dict.get('snapshot_id', None)
        im_data['os_distro'] = improp.get('os_distro', None)
        im_data['hypervisor_type'] = improp.get('hypervisor_type', None)
        im_data['type'] = improp.get('image_type', 'template')
        im_data['hw_qemu_guest_agent'] = improp.get('hw_qemu_guest_agent', False) == 'yes'
        im_data['os_version'] = improp.get('os_version', None)
        im_data['architecture'] = improp.get('architecture', None)
        is_public = data.get('is_public', None)
        if is_public is not None:
            im_data['visibility'] = 'public' if is_public else data.get('visibility', 'private')
        if owner and len(owner) > 31:
            im_data['project_id'] = owner
        return im_data

    def delete(self, payload, region, timestamp):
        image_id = payload.get('id', None)
        if not image_id:
            LOG.error('Unable to delete image without ID: {}'.format(payload))
        return super(ImageEventHandler, self).delete(image_id, region, timestamp)


class ImageMemberEventHandler(BaseHandler):
    serializer_class = serializers.ImageMemberSyncSerializer
    version_field = 'sync_version'

    def __init__(self):
        self.event_handlers = {'image.member.create': self.create_or_update,
                               'image.member.update': self.create_or_update,
                               'image.member.delete': self.delete}

    @retry_on_deadlock
    def create_if_missing(self, member_id, image_id):
        """
        We will try to create an Image Member object if one doesn't exist yet.
        We need to do this here because Image Members do not have IDs in OpenStack
        and our BaseHandler always require an ID
        """
        db_imm, created = self.model_class.objects.get_or_create(member_id=member_id, image_id=image_id,
                                                                 defaults=dict(member_id=member_id, image_id=image_id))
        return db_imm.id

    def serialize(self, data, region, timestamp):
        data[self.version_field] = self.get_version(timestamp)
        # NOTE(tomo): ImageMember does not have an actual ID in OpenStack
        # and as such, we need to fetch the object from DB by member_id and image_id
        if 'member_id' in data and 'image_id' in data:
            obj_id = self.create_if_missing(data['member_id'], data['image_id'])
            data['id'] = obj_id
        else:
            raise ValueError('Received an invalid ImageMember data: {}'.format(data))
        return data

    def delete(self, payload, region, timestamp):
        if payload.get('member_id', None) is not None and payload.get('image_id', None) is not None:
            self.model_class.objects.filter(member_id=payload.get('member_id'),
                                            image_id=payload.get('image_id')).delete()
        else:
            LOG.error('Unable to delete image member without member_id and image_id'.format(payload))
