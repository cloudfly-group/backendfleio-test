import json

from fleio.openstack.images import serializers
from fleio.openstack.sync.handler import BaseHandler, retry_on_deadlock


class ImageSyncHandler(BaseHandler):
    serializer_class = serializers.ImageSyncSerializer
    version_field = 'sync_version'

    def serialize(self, data, region, timestamp):
        image_attrs = {"container_format", "disk_format", "created_at", "owner", "size", "id", "status", "updated_at",
                       "checksum", "visibility", "name", "is_public", "protected", "min_disk", "min_ram"}
        image_ext_attrs = {"file", "locations", "schema", "tags", "virtual_size", "kernel_id", "ramdisk_id",
                           "image_url"}

        block_device_mapping = json.loads(data.get('block_device_mapping', '[]'))
        if isinstance(block_device_mapping, list):
            data['volume_snapshot_uuid'] = block_device_mapping[0]['snapshot_id'] if len(block_device_mapping) else None

        data['properties'] = {k: v for (k, v) in data.items() if k not in (image_attrs | image_ext_attrs)}
        data['region_id'] = region
        if 'image_type' in data:
            data['type'] = data.get('image_type')
        data[self.version_field] = self.get_version(timestamp)
        owner = data.get('owner', None)
        if owner and len(owner) > 31:
            data['project_id'] = owner
        hw_qemu_guest_agent = data.get('hw_qemu_guest_agent', 'no')
        if hw_qemu_guest_agent == 'no':
            data['hw_qemu_guest_agent'] = False
        else:
            data['hw_qemu_guest_agent'] = True
        return data


class ImageMemberSyncHandler(BaseHandler):
    serializer_class = serializers.ImageMemberSyncSerializer
    version_field = 'sync_version'

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
