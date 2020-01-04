import copy
import logging
import uuid

import cinderclient.exceptions
from django.db import transaction

from fleio.activitylog.utils.activity_helper import activity_helper
from fleio.openstack.api.cinder import cinder_client
from fleio.openstack.api.identity import IdentityAdminApi
from fleio.openstack.models import Volume
from fleio.openstack.models import VolumeType
from fleio.openstack.sync.handler import BaseHandler
from fleio.openstack.sync.utils import retry_on_deadlock
from fleio.openstack.tasks import sync_volume_extra_details
from fleio.openstack.volumes.serializers import (
    QosSpecsSyncSerializer, VolumeAttachmentSyncSerializer, VolumeSyncSerializer,
    VolumeTypeExtraSpecSyncSerializer, VolumeTypeSyncSerializer, VolumeTypeToProjectSyncSerializer
)

LOG = logging.getLogger(__name__)


class VolumeAttachmentHandlerBase(BaseHandler):
    serializer_class = VolumeAttachmentSyncSerializer
    version_field = 'sync_version'

    def serialize(self, data, region, timestamp):
        # NOTE(tomo): attachments don't have a region because we can get the region
        # from the volume or instance. The version is the same as the volume.
        new_att = copy.deepcopy(data)
        if 'id' not in new_att:
            new_att['id'] = new_att.pop('attachment_id', None)
        new_att[self.version_field] = self.get_version(timestamp)
        return new_att


class VolumeSyncHandler(BaseHandler):
    serializer_class = VolumeSyncSerializer
    version_field = 'sync_version'

    def serialize(self, data, region, timestamp):
        """Accepts a cinder Volume class"""
        serialized = data.to_dict()
        serialized[self.version_field] = self.get_version(timestamp)
        serialized['region'] = region
        if 'tenant_id' in serialized:
            serialized['project_id'] = serialized.get('tenant_id')
        elif 'os-vol-tenant-attr:tenant_id' in serialized:
            serialized['project_id'] = serialized.get('os-vol-tenant-attr:tenant_id')
        serialized['type'] = serialized.get('volume_type', None)
        serialized['extra'] = dict()
        for attr in ('attachments', 'os-vol-host-attr:host', 'encrypted', 'metadata', 'os-vol-mig-status-attr:name_id',
                     'os-vol-tenant-attr:tenant_id', 'volume_image_metadata'):
            if attr in serialized:
                serialized['extra'].setdefault(attr, serialized.get(attr))
        return serialized

    def create_or_update(self, volume, region, timestamp):
        super(VolumeSyncHandler, self).create_or_update(data=volume, region=region, timestamp=timestamp)
        # Sync attachments too
        vol_dict = volume.to_dict()
        LOG.debug('Checking attachments: {}'.format(vol_dict.get('attachments', list())))
        for attachment in vol_dict.get('attachments', list()):
            VolumeAttachmentHandlerBase().create_or_update(data=attachment, region=region, timestamp=timestamp)
        # Delete volume attachments with an older sync version
        version = self.get_version(timestamp=timestamp)
        VolumeAttachmentSyncSerializer.Meta.model.objects.filter(volume_id=vol_dict['id'],
                                                                 sync_version__lt=version).delete()

    def delete(self, volume_id, region=None, timestamp=None):
        LOG.debug('Deleting volume and attachments from database: %s' % volume_id)
        with transaction.atomic():
            deleted, vol_num = super(VolumeSyncHandler, self).delete(volume_id, region, timestamp)
            # Detele attachments
            VolumeAttachmentSyncSerializer.Meta.model.objects.filter(volume_id=volume_id).delete()
        if not deleted:
            LOG.debug('Volume already deleted: %s' % volume_id)
        else:
            LOG.debug('Deleted {} volumes'.format(vol_num))
        return deleted, vol_num


class VolumeHandler(BaseHandler):
    serializer_class = VolumeSyncSerializer

    def __init__(self, api_session=None):
        self.api_session = api_session or IdentityAdminApi().session
        self.event_handlers = {'volume.update.start': self.create_or_update,
                               'volume.create.start': self.create_or_update,
                               'volume.delete.start': self.create_or_update,
                               'volume.attach.start': self.create_or_update,
                               'volume.detach.start': self.create_or_update,
                               'volume.resize.start': self.create_or_update,
                               'volume.update.end': self.update_end,
                               'volume.create.end': self.create_end,
                               'volume.delete.end': self.delete,
                               'volume.attach.end': self.create_or_update_attachment,
                               'volume.detach.end': self.delete_attachment,
                               'volume.resize.end': self.create_or_update,
                               'volume.revert.start': self.create_or_update,
                               'volume.revert.end': self.update_end,
                               'volume.retype': self.create_or_update,
                               'volume.exists': self.create_or_update,
                               'compute.instance.volume.attach': self.volume_attach}

        self.error_handlers = {'scheduler.create_volume': self.create_or_update}

    def update_end(self, data, region, timestamp):
        if 'volume_id' in data:
            activity_helper.start_generic_activity(
                category_name='volume', activity_class='volume extra details synchronization',
                volume_id=data['volume_id']
            )
            sync_volume_extra_details.delay(volume_id=data['volume_id'], region_name=region)
            activity_helper.end_activity()
        return super().create_or_update(data=data, region=region, timestamp=timestamp)

    def create_end(self, data, region, timestamp):
        if 'volume_id' in data:
            activity_helper.start_generic_activity(
                category_name='volume', activity_class='volume extra details synchronization',
                volume_id=data['volume_id']
            )
            sync_volume_extra_details.delay(volume_id=data['volume_id'], region_name=region)
            activity_helper.end_activity()
        return super().create_or_update(data=data, region=region, timestamp=timestamp)

    def get_volume_from_api(self, volume_id, region, api_session=None):
        api_session = api_session or self.api_session
        cc = cinder_client(api_session=api_session, region_name=region)
        try:
            volume = cc.volumes.get(volume_id)
        except cinderclient.exceptions.NotFound:
            LOG.debug('Unable to get volume missing in OpenStack: {}'.format(volume_id))
            return None
        return volume

    def serialize(self, data, region, timestamp):
        data[self.version_field] = self.get_version(timestamp)
        data['region'] = region
        data['project_id'] = data.get('project_id', data.get('tenant_id', None))
        # NOTE(tomo): See if we already have this volume uuid in our db.
        # this can also be a volume type name
        volume_type = data.get('volume_type')
        volume_type_name = volume_type
        if volume_type:
            try:
                uuid.UUID(volume_type)
            except Exception as e:
                LOG.debug('Volume type not uuid {}'.format(e))
            else:
                try:
                    existing_vtype = VolumeType.objects.get(volume_type_id=volume_type)
                    volume_type_name = existing_vtype.name or volume_type
                except (VolumeType.DoesNotExist, VolumeType.MultipleObjectsReturned):
                    pass
        data['type'] = volume_type_name
        data['extra'] = dict()
        if 'volume_id' in data:
            data['id'] = data['volume_id']
        if 'display_name' in data:
            data['name'] = data['display_name']
        for attr in ('volume_attachment', 'os-vol-host-attr:host', 'encrypted', 'metadata',
                     'os-vol-mig-status-attr:name_id'):
            if attr in data:
                data['extra'].setdefault(attr, data.get(attr))
        return data

    def create_or_update_attachment(self, data, region, timestamp):
        super(VolumeHandler, self).create_or_update(data=data, region=region, timestamp=timestamp)
        for attachment in data.get('volume_attachment', list()):
            attachment['server_id'] = attachment['instance_uuid']
            VolumeAttachmentHandlerBase().create_or_update(data=attachment, region=region, timestamp=timestamp)

    def delete_attachment(self, data, region, timestamp):
        # NOTE(erno): detach events are different for different openstack versions, after we introduce versioned
        # notifications refactor this to avoid making a call to cinder
        volume_id = data.get('volume_id')
        # Validate the data
        if not volume_id:
            LOG.warning('Unable to update volume without id')
            return
        volume = self.get_volume_from_api(volume_id=volume_id, region=region)
        if volume is None:
            LOG.debug('Volume not found, deleting: %s' % volume_id)
            return self.delete(payload=data, region=region, timestamp=timestamp)
        VolumeSyncHandler().create_or_update(volume=volume, region=region, timestamp=timestamp)

    def volume_attach(self, data, region, timestamp):
        # NOTE(erno): in openstack pike the status will be changed only to 'in-use' after the
        # 'compute.instance.volume.attach' event, so we assume that by reaching this event the operation has been
        # completed successfully, therefore volume status can be set to 'in-use' (to avoid a call to cinder to query
        # the volume status)
        # maybe after openstack >= pike refactor handler
        try:
            volume = Volume.objects.get(id=data.get('volume_id', None))
            volume.status = 'in-use'
            volume.save()
        except (Volume.DoesNotExist, Volume.MultipleObjectsReturned):
            pass

    def delete(self, payload, region=None, timestamp=None):
        volume_id = payload.get('volume_id', None)
        if not volume_id:
            LOG.warning('Unable to delete volume without id: {}'.format(payload))
            return
        return super(VolumeHandler, self).delete(obj_id=volume_id, region=region, timestamp=timestamp)


class VolumeTypeToProjectSyncHandler(BaseHandler):
    serializer_class = VolumeTypeToProjectSyncSerializer

    def serialize(self, data, region, timestamp):
        serialized = data.to_dict()
        serialized[self.version_field] = self.get_version(timestamp)
        serialized['id'] = serialized['volume_type_id'] + serialized['project_id']
        return serialized


class VolumeTypeExtraSpecSyncHandler(BaseHandler):
    serializer_class = VolumeTypeExtraSpecSyncSerializer

    def serialize(self, data, region, timestamp):
        data[self.version_field] = self.get_version(timestamp)
        data['id'] = data['volume_type_id'] + data['key']
        return data


class VolumeTypeSyncHandler(BaseHandler):
    serializer_class = VolumeTypeSyncSerializer

    def serialize(self, data, region, timestamp):
        serialized = data.to_dict()
        serialized['volume_type_id'] = serialized.pop('id', None)
        serialized[self.version_field] = self.get_version(timestamp)
        serialized['region'] = region
        return serialized


class QoSSyncHandler(BaseHandler):
    serializer_class = QosSpecsSyncSerializer

    def serialize(self, data, region, timestamp):
        serialized = data.to_dict()
        serialized[self.version_field] = self.get_version(timestamp)
        serialized['qos_specs_id'] = serialized.pop('id', None)
        return serialized


class VolumeTypeHandler(BaseHandler):
    serializer_class = VolumeTypeSyncSerializer
    version_field = 'sync_version'

    def __init__(self):
        # NOTE(erno): no notifications are coming for associating/dissociating volume types to/from projects
        self.event_handlers = {'volume_type.create': self.create_or_update,
                               'volume_type.update': self.create_or_update,
                               'volume_type.delete': self.delete,
                               'qos_specs.associate': self.qos_associate,
                               'qos_specs.disassociate': self.qos_dissociate
                               }

    def qos_associate(self, data, region, timestamp):
        association = dict()
        association['qos_specs_id'] = data['id']
        association['volume_type_id'] = data['type_id']
        association[self.version_field] = self.get_version(timestamp)
        return self.sync(data=association)

    def qos_dissociate(self, data, region, timestamp):
        dissociation = dict()
        dissociation['qos_specs_id'] = None
        dissociation['volume_type_id'] = data['type_id']
        dissociation[self.version_field] = self.get_version(timestamp)
        return self.sync(data=dissociation)

    def serialize(self, data, region, timestamp):
        volume_types = copy.deepcopy(data['volume_types'])
        volume_types['volume_type_id'] = volume_types.pop('id', None)
        volume_types[self.version_field] = self.get_version(timestamp)
        volume_types['region'] = region
        volume_types['updated_at'] = volume_types.get('updated_at', None) or timestamp
        return volume_types

    def delete(self, data, region, timestamp):
        try:
            obj_id = data['volume_types']['id']
            return super(VolumeTypeHandler, self).delete(obj_id, region, timestamp)
        except KeyError:
            LOG.warning('Volume type ID required')
            return None


class VolumeTypeExtraSpecHandler(BaseHandler):
    serializer_class = VolumeTypeExtraSpecSyncSerializer
    version_field = 'sync_version'

    def __init__(self):
        self.event_handlers = {'volume_type_extra_specs.create': self.create_or_update,
                               'volume_type_extra_specs.delete': self.delete
                               }

    def serialize(self, data, region, timestamp):
        volume_type_extra_specs = dict()
        volume_type_extra_specs['key'] = list(data['specs'])[0]  # NOTE(tomo): Py23 list(iterator)
        volume_type_extra_specs['value'] = data['specs'][volume_type_extra_specs['key']]
        volume_type_extra_specs['volume_type_id'] = data['type_id']
        volume_type_extra_specs[self.version_field] = self.get_version(timestamp)
        volume_type_extra_specs['updated_at'] = volume_type_extra_specs['created_at'] = timestamp
        volume_type_extra_specs['id'] = volume_type_extra_specs['volume_type_id'] + volume_type_extra_specs['key']
        return volume_type_extra_specs

    @retry_on_deadlock
    def delete(self, data, region, timestamp):
        return self.model_class.objects.filter(volume_type__volume_type_id=data['type_id'], key=data['id']).delete()


class QoSSpecHandler(BaseHandler):
    serializer_class = QosSpecsSyncSerializer
    version_field = 'sync_version'

    def __init__(self, api_session=None):
        self.api_session = api_session or IdentityAdminApi().session
        self.event_handlers = {'qos_specs.create': self.create_or_update,
                               'qos_specs.update': self.create_or_update,
                               'qos_specs.delete': self.delete,
                               'qos_specs.delete_keys': self.create_or_update
                               }
        self.error_handlers = {'qos_specs.create': self.create_error}

    def serialize(self, data, region, timestamp):
        qos_spec = data.to_dict()
        qos_spec[self.version_field] = self.get_version(timestamp)
        qos_spec['updated_at'] = qos_spec['created_at'] = timestamp
        qos_spec['qos_specs_id'] = qos_spec.pop('id', None)
        return qos_spec

    def get_qos_spec_from_api(self, payload, region, api_session=None):
        name = payload.get('name', None)
        id = payload.get('id', None)
        if not name and not id:
            LOG.warning('Unable to get QoS spec without a name or id')
            return None
        api_session = api_session or self.api_session
        cc = cinder_client(api_session=api_session, region_name=region)
        try:
            # name is unique in openstack
            if name:
                qos_spec = cc.qos_specs.find(name=name)
            else:
                qos_spec = cc.qos_specs.get(id)
        except cinderclient.exceptions.NotFound:
            LOG.debug('Unable to get QoS spec missing in OpenStack: {}'.format(name or id))
            return None
        return qos_spec

    def create_or_update(self, payload, region, timestamp):
        qos_spec = self.get_qos_spec_from_api(payload, region)
        if qos_spec is None:
            LOG.debug('QoS spec not found, deleting: %s' % payload.get('name', payload.get('id')))
            return self.delete(data=payload, region=region, timestamp=timestamp)
        return super(QoSSpecHandler, self).create_or_update(data=qos_spec, region=region, timestamp=timestamp)

    @retry_on_deadlock
    def delete(self, data, region, timestamp):
        name = data.get('name', None)
        id = data.get('id', None)
        if not name and not id:
            LOG.warning('Unable to delete QoS spec without a name or id')
            return None
        if name:
            return self.model_class.objects.filter(name=name).delete()
        else:
            return self.model_class.objects.filter(qos_specs_id=id).delete()

    def create_error(self, payload, region, timestamp):
        try:
            error_message = payload['error_message']['msg']
        except KeyError:
            error_message = 'Unable to create QoS spec {}'.format(payload.get('name', None))
        LOG.error(error_message)
