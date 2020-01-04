from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from fleio.core.models import Client
from fleio.core.clients.serializers import ClientMinSerializer
from fleio.openstack.settings import OSConfig
from fleio.openstack.models import Image, VolumeAttachments, VolumeSnapshot
from fleio.openstack.models import Volume


class StaffVolumeSerializer(serializers.ModelSerializer):
    client = ClientMinSerializer(source='project.service.client', read_only=True, default=None)
    display_name = serializers.ReadOnlyField()
    size_increment = serializers.SerializerMethodField()
    number_of_snapshots = serializers.SerializerMethodField(read_only=True)
    related_instance_uuid = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Volume
        exclude = ('extra', 'sync_version',)

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
            data['source'] = Image.objects.get(pk=data['source'])
        elif data['source_type'] == 'volume':
            data['source'] = Volume.objects.get(pk=data['source'])
        elif data['source_type'] == 'new':
            data['source'] = None
        return data

    def to_representation(self, instance):
        return super(VolumeSourceSerializer, self).to_representation(instance)


class StaffVolumeCreateSerializer(serializers.ModelSerializer):
    client = serializers.IntegerField(required=True, write_only=True)
    source = VolumeSourceSerializer(write_only=True, required=False)

    class Meta:
        model = Volume
        fields = ('name', 'description', 'size', 'region', 'type', 'id', 'client', 'source')
        read_only_fields = ('id',)

    def validate(self, data):
        volume_type = data.get('type', None)
        region = data.get('region', None)
        size = data.get('size', 0)
        conf = OSConfig()
        if conf.volume_size_increments:
            size_increment = conf.volume_size_increments.get(region, {}).get(volume_type, 1)
        else:
            size_increment = 1
        if size % size_increment != 0:
            raise ValidationError({'size': _('Size must be a multiple of {} GB').format(size_increment)})
        return data

    @staticmethod
    def validate_client(value):
        try:
            client = Client.objects.get(id=value)
        except (Client.DoesNotExist, Client.MultipleObjectsReturned):
            raise ValidationError(_('Client does not exist'))
        return client

    def to_internal_value(self, data):
        """
        Perform any data modification here.
        to_internal_value is called before .validate() and after each field is validated.
        """
        value = super(StaffVolumeCreateSerializer, self).to_internal_value(data)
        client = value.pop('client')
        project = client.first_project
        if not project:
            raise ValidationError({'detail': _('Unable to find a project for the specified client')})
        value['project'] = project
        if 'type' not in value:
            value['type'] = None

        return value
