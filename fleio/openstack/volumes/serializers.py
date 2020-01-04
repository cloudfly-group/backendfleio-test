import logging
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from fleio.openstack import models
from fleio.openstack.models import VolumeAttachments, VolumeSnapshot
from fleio.openstack.settings import OSConfig
from fleio.openstack.instances.serializers import InstanceSerializer

LOG = logging.getLogger(__name__)


class VolumeAttachmentSerializerMin(serializers.ModelSerializer):
    instance = InstanceSerializer(read_only=True)

    class Meta:
        model = models.VolumeAttachments
        exclude = ('extra', )


class OpenStackVolumeSerializerMin(serializers.ModelSerializer):
    size_increment = serializers.SerializerMethodField()
    number_of_snapshots = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Volume
        fields = ('id', 'name', 'region', 'description', 'status', 'size', 'type', 'display_name', 'size_increment',
                  'number_of_snapshots', 'bootable')

    @staticmethod
    def get_number_of_snapshots(volume):
        return VolumeSnapshot.objects.filter(volume=volume).count()

    @staticmethod
    def get_size_increment(volume):
        conf = OSConfig()
        volume_size_increments = conf.volume_size_increments
        if volume_size_increments:
            size_increment = volume_size_increments.get(volume.region, {}).get(volume.type, 1)
        else:
            size_increment = 1
        return size_increment


class OpenStackVolumeSerializer(serializers.ModelSerializer):
    attachments = VolumeAttachmentSerializerMin(many=True)
    display_name = serializers.ReadOnlyField()
    size_increment = serializers.SerializerMethodField()
    number_of_snapshots = serializers.SerializerMethodField(read_only=True)
    related_instance_uuid = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Volume
        exclude = ('extra', 'user_id', 'consistencygroup_id', 'sync_version',)

    @staticmethod
    def get_related_instance_uuid(volume):
        volume_attachment = VolumeAttachments.objects.filter(volume_id=volume.id).first()
        return volume_attachment.server_id if volume_attachment else None

    @staticmethod
    def get_number_of_snapshots(volume):
        return VolumeSnapshot.objects.filter(volume=volume).count()

    @staticmethod
    def get_size_increment(volume):
        conf = OSConfig()
        volume_size_increments = conf.volume_size_increments
        if volume_size_increments:
            size_increment = volume_size_increments.get(volume.region, {}).get(volume.type, 1)
        else:
            size_increment = 1
        return size_increment


class VolumeSourceSerializer(serializers.Serializer):
    VOLUME_SOURCE_TYPES = (
        ('image', _('Image')),
        ('volume', _('Volume')),
        ('new', _('Empty volume'))
    )
    source_type = serializers.ChoiceField(choices=VOLUME_SOURCE_TYPES)
    source = serializers.CharField(max_length=128)

    def to_internal_value(self, data):
        if data['source_type'] == 'image':
            data['source'] = models.Image.objects.get(pk=data['source'])
        elif data['source_type'] == 'volume':
            data['source'] = models.Volume.objects.get(pk=data['source'])
        elif data['source_type'] == 'new':
            data['source'] = None
        return data

    def to_representation(self, instance):
        return super(VolumeSourceSerializer, self).to_representation(instance)


class OpenstackVolumeCreateSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    source = VolumeSourceSerializer(write_only=True, required=False)

    class Meta:
        model = models.Volume
        fields = ('name', 'size', 'region', 'type', 'id', 'source')

    def validate(self, data):
        conf = OSConfig()
        volume_type = data.get('type', None)
        region = data.get('region', None)
        size = data.get('size', 0)
        if conf.volume_size_increments:
            size_increment = conf.volume_size_increments.get(region, {}).get(volume_type, 1)
        else:
            size_increment = 1
        if size % size_increment != 0:
            raise ValidationError({'size': _('Size must be a multiple of {}').format(size_increment)})
        return data

    def to_internal_value(self, data):
        """
        Perform any data modification here.
        to_internal_value is called before .validate() and after each field is validated.
        """
        value = super(OpenstackVolumeCreateSerializer, self).to_internal_value(data)

        request = self.context.get('request', None)
        assert request, 'Serializer can only be used with http requests'

        client = request.user.clients.first()
        if not client:
            raise ValidationError({'detail': _('Unable to find a client for the current user')})
        project = client.first_project
        if not project:
            raise ValidationError({'detail': _('Cannot create volume without a project')})
        value['project_id'] = project.project_id
        if 'type' not in value:
            value['type'] = None

        return value


class VolumeAttachSerializer(serializers.Serializer):
    instance = serializers.SlugRelatedField(slug_field='id', queryset=models.Instance.objects.all())

    def validate_instance(self, instance):
        volume = self.context.get('view').get_object()
        if volume.project != instance.project:
            raise ValidationError(_('Unable to find the instance'))
        return instance


class VolumeDetachSerializer(serializers.Serializer):
    attachment = serializers.SlugRelatedField(slug_field='attachment_id',
                                              queryset=models.VolumeAttachments.objects.all())

    def validate(self, data):
        volume = self.context.get('view').get_object()
        instance = data['attachment'].instance
        attachment = data['attachment']
        if volume.project != instance.project:
            raise ValidationError({'detail': _('Unable to find the instance')})
        if attachment.instance != instance or attachment.volume != volume:
            raise ValidationError({'detail': _('Unable to find the attachment')})
        return data


class VolumeAttachmentSerializer(serializers.ModelSerializer):
    volume = OpenStackVolumeSerializerMin()

    class Meta:
        model = models.VolumeAttachments
        exclude = ('server_id', )


class VolumeNameSerializer(serializers.Serializer):
    name = serializers.CharField(write_only=True, max_length=128, required=True)


class VolumeRevertSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    snapshot_id = serializers.CharField(max_length=36)


class VolumeExtendSerializer(serializers.Serializer):
    size = serializers.IntegerField()

    def validate_size(self, size):
        volume = self.context.get('view').get_object()
        if size <= volume.size:
            raise ValidationError(_('Volumes cannot be shrinked, only extended'))
        return size

    def validate(self, data):
        volume = self.context.get('view').get_object()
        volume_type = volume.type
        region = volume.region
        size = data.get('size', 0)
        conf = OSConfig()
        if conf.volume_size_increments:
            size_increment = conf.volume_size_increments.get(region, {}).get(volume_type, 1)
        else:
            size_increment = 1
        if size % size_increment != 0:
            raise ValidationError({'size': _('Size must be a multiple of {}').format(size_increment)})
        return data


class VolumeAttachmentSyncSerializer(serializers.ModelSerializer):
    extra = serializers.JSONField(default=dict())
    sync_version = serializers.IntegerField(default=0)

    class Meta:
        model = models.VolumeAttachments
        fields = '__all__'
        # NOTE(tomo): Remove the unique validator to avoid an extra query
        # we deal with uniqueness validation in another way
        extra_kwargs = {'id': {'validators': list()}}


class VolumeSyncSerializer(serializers.ModelSerializer):
    extra = serializers.JSONField(default=dict())
    sync_version = serializers.IntegerField(default=0)
    attachments = VolumeAttachmentSyncSerializer(many=True, read_only=True)
    project_id = serializers.CharField(write_only=True)

    class Meta:
        model = models.Volume
        fields = '__all__'
        # NOTE(tomo): Remove the unique validator to avoid an extra query
        # we deal with uniqueness validation in another way
        extra_kwargs = {'id': {'validators': list()}}


class VolumeTypeSyncSerializer(serializers.ModelSerializer):
    sync_version = serializers.IntegerField(default=0)
    qos_specs_id = serializers.CharField(max_length=36, allow_null=True)

    class Meta:
        model = models.VolumeType
        fields = '__all__'
        extra_kwargs = {'id': {'validators': list()}}


class VolumeTypeExtraSpecSyncSerializer(serializers.ModelSerializer):
    sync_version = serializers.IntegerField(default=0)
    volume_type_id = serializers.CharField(max_length=36, allow_null=True)

    class Meta:
        model = models.VolumeTypeExtraSpec
        fields = '__all__'
        extra_kwargs = {'id': {'validators': list()}}


class QosSpecsSyncSerializer(serializers.ModelSerializer):
    sync_version = serializers.IntegerField(default=0)
    specs = serializers.JSONField(default=dict())

    class Meta:
        model = models.QoSSpec
        fields = '__all__'
        extra_kwargs = {'qos_specs_id': {'validators': list()}}


class VolumeTypeToProjectSyncSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VolumeTypeToProject
        fields = '__all__'
