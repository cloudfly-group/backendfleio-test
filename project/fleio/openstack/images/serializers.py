from datetime import timedelta

from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from fleio.core.clients.serializers import ClientMinSerializer
from fleio.core.features import active_features
from fleio.openstack.configuration import OpenstackSettings
from fleio.openstack.images.utils import validate_ascii_properties
from fleio.openstack.models import Image, ImageMembers, Project
from fleio.openstack.models.image import OpenStackImageVisibility
from fleio.openstack.settings import OS_HYPERVISOR_TYPES


class ImageSyncSerializer(serializers.ModelSerializer):
    properties = serializers.JSONField(default=dict())
    tags = serializers.JSONField(default=list())
    region_id = serializers.CharField(allow_null=True, allow_blank=True)
    project_id = serializers.CharField(allow_null=True, allow_blank=True, default=None)

    class Meta:
        model = Image
        fields = '__all__'
        extra_kwargs = {'id': {'validators': list()}}


class ImageMemberSyncSerializer(serializers.ModelSerializer):
    member_id = serializers.CharField(allow_null=True, allow_blank=True, default=None)
    image_id = serializers.CharField(allow_null=True, allow_blank=True, default=None)

    class Meta:
        model = ImageMembers
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    tags = serializers.JSONField(default=list())
    client = ClientMinSerializer(source='project.service.client', read_only=True, default=None)
    properties = serializers.JSONField(default=dict())
    is_iso = serializers.SerializerMethodField()
    display_name = serializers.SerializerMethodField()
    cleanup_date = serializers.SerializerMethodField()
    assigned_to_flavor = serializers.BooleanField(default=True, read_only=True)

    class Meta:
        model = Image
        exclude = ('project', 'owner', 'sync_version', 'virtual_size', 'flavors', 'flavor_groups')
        read_only_fields = ('id', 'type', 'region', 'status', 'size', 'os_distro', 'os_version', 'architecture',
                            'instance_uuid', 'is_iso', 'display_name', 'cleanup_date', 'assigned_to_flavor',
                            'properties', )

    def to_representation(self, instance):
        if isinstance(instance.properties, dict):
            # we treat these items as field not as properties
            instance.properties.pop('os_distro', None)
            instance.properties.pop('hypervisor_type', None)
            instance.properties.pop('os_version', None)
            instance.properties.pop('architecture', None)
        else:
            instance.properties = {}
        return super(ImageSerializer, self).to_representation(instance=instance)

    @staticmethod
    def get_is_iso(image: Image) -> bool:
        return image.disk_format == 'iso'

    @staticmethod
    def get_display_name(image: Image) -> str:
        if image.disk_format == 'iso':
            return '[ISO] {}'.format(image.name)

        return image.name

    @staticmethod
    def get_cleanup_date(image: Image):
        cleanup_date = None
        try:
            project = image.project
        except Project.DoesNotExist:
            return cleanup_date

        if project and project.service and project.service.client:
            openstack_settings = OpenstackSettings.for_client(project.service.client)

            if openstack_settings.auto_cleanup_image_types:
                if image.disk_format in openstack_settings.auto_cleanup_image_types:
                    cleanup_date = image.created_at + timedelta(days=openstack_settings.auto_cleanup_number_of_days)

        return cleanup_date


class ImageBriefSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    name = serializers.ReadOnlyField()
    id = serializers.ReadOnlyField()


class ImageCreateSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=False, write_only=True)
    url = serializers.URLField(required=False, write_only=True)
    source = serializers.ChoiceField(choices=['file', 'url', 'later'], required=True)
    hypervisor_type = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = Image
        fields = ('name', 'min_disk', 'min_ram', 'region', 'container_format', 'disk_format', 'visibility',
                  'protected', 'architecture', 'os_distro', 'os_version', 'file', 'url', 'source', 'hypervisor_type',)
        extra_kwargs = {'container_format': {'default': 'bare'}}

    @staticmethod
    def validate_visibility(value):
        if value not in OpenStackImageVisibility.get_user_choices():
            raise serializers.ValidationError({'visibility': 'Invalid visibility selected'})
        return value

    @staticmethod
    def validate_hypervisor_type(value: str):
        if value == 'null':
            value = None
        if value and value not in OS_HYPERVISOR_TYPES:
            raise serializers.ValidationError(_('Invalid hypervisor type selected'))
        return value

    def validate(self, attrs):
        attrs = super(ImageCreateSerializer, self).validate(attrs)
        if attrs.get('source') == 'file' and not active_features.is_enabled('openstack.images.file_uploads'):
            raise serializers.ValidationError(detail={'source': 'File uploads are not allowed.'})
        if attrs.get('source') == 'file' and not attrs.get('file'):
            raise serializers.ValidationError(detail={'source': 'A File is required'})
        elif attrs.get('source') == 'url' and not attrs.get('url'):
            raise serializers.ValidationError(detail={'url': 'A valid URL is required'})
        return attrs


class ImageUpdateSerializer(serializers.ModelSerializer):
    properties = serializers.JSONField(default=dict())
    hypervisor_type = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = Image
        fields = ('name', 'min_disk', 'min_ram', 'visibility', 'protected', 'architecture',
                  'os_distro', 'hypervisor_type', 'os_version', 'properties',)

    @staticmethod
    def validate_visibility(value):
        if value not in OpenStackImageVisibility.get_user_choices():
            raise serializers.ValidationError({'visibility': 'Invalid visibility selected'})
        return value

    @staticmethod
    def validate_hypervisor_type(value: str):
        if value == 'null':
            value = None
        if value and value not in OS_HYPERVISOR_TYPES:
            raise serializers.ValidationError(_('Invalid hypervisor type selected'))
        return value

    @staticmethod
    def validate_properties(value: str or dict):
        return validate_ascii_properties(value)
