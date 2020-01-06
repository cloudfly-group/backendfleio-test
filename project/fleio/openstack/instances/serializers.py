import copy
import ipaddress
import json
import logging
from collections import OrderedDict

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from novaclient.api_versions import APIVersion
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import empty

from fleio.core.drf import FieldsModelSerializer
from fleio.core.features import active_features, staff_active_features
from fleio.core.models import Client, ClientGroup
from fleio.core.utils import check_password_complexity
from fleio.openstack import models
from fleio.openstack.images.serializers import ImageSerializer
from fleio.openstack.instances.instance_status import InstanceStatus
from fleio.openstack.models import Instance
from fleio.openstack.models import OpenstackInstanceFlavor
from fleio.openstack.serializers.regions import RegionSerializer
from fleio.openstack.settings import plugin_settings
from fleio.openstack.utils import newlines_substract
from fleio.pkm.models import PublicKey

LOG = logging.getLogger(__name__)

INSTANCE_ALLOWED_ACTIONS = {
    InstanceStatus.ACTIVE: [
        'reboot', 'shutoff', 'resize', 'rescue', 'rebuild', 'console', 'rename',
        'create_snapshot', 'attach_volume', 'boot_from_iso'
    ],
    InstanceStatus.STOPPED: [
        'start', 'resize', 'rescue', 'rebuild', 'rename', 'create_snapshot', 'attach_volume',
        'boot_from_iso',
    ],
    InstanceStatus.RESCUED: ['unrescue', 'console'],
    InstanceStatus.BOOTED_FROM_ISO: ['unmount_and_reboot', 'console'],
    InstanceStatus.RESIZED: ['cfresize', 'console', 'attach_volume'],
    InstanceStatus.ERROR: ['reset_state', 'delete']
}


def validate_password(password):
    validation_result = check_password_complexity(password)
    if not validation_result['password_ok']:
        error_list = [key for key, value in validation_result.items() if value is True]
        raise ValidationError(error_list)
    return password


class InstanceSyncSerializer(serializers.ModelSerializer):
    volumes_attached = serializers.JSONField(default=list())
    addresses = serializers.JSONField(default=dict())
    security_groups = serializers.JSONField(default=list())
    fault = serializers.JSONField(default=None)
    extra = serializers.JSONField(default=None)
    config_drive = serializers.BooleanField(default=False)
    project_id = serializers.CharField(write_only=True)
    locked = serializers.BooleanField(default=False)

    class Meta:
        model = models.Instance
        fields = '__all__'
        extra_kwargs = {'id': {'validators': list()}}

    def run_validation(self, data=empty):
        if data and isinstance(data, dict):
            # save instances host names
            if 'OS-EXT-SRV-ATTR:host' in data:
                data['host_name'] = data['OS-EXT-SRV-ATTR:host']
                if data['hostId'] == data['host_name']:
                    del data['hostId']

            # allow syncing instances that do not have anymore the related flavor in fleio
            if 'flavor' in data:
                flavor = data['flavor']
                if flavor:
                    try:
                        OpenstackInstanceFlavor.objects.get(id=flavor)
                    except OpenstackInstanceFlavor.DoesNotExist:
                        data['flavor'] = None
        return super().run_validation(data=data)


class InstancePortSerializer(serializers.ModelSerializer):
    ip_addresses = serializers.ReadOnlyField()
    network_name = serializers.ReadOnlyField()
    floating_ips = serializers.SerializerMethodField()

    class Meta:
        model = models.Port
        fields = ('network_id', 'name', 'description', 'ip_addresses', 'network_name', 'floating_ips')

    def get_floating_ips(self, port):
        floating_ips = models.FloatingIp.objects.filter(port_id=port.id)
        return FloatingIpMinSerializer(instance=floating_ips, many=True).data


class FlavorGroupBriefSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    id = serializers.IntegerField()
    name = serializers.CharField()
    priority = serializers.IntegerField()


class FlavorSerializer(serializers.ModelSerializer):
    memory_gb = serializers.ReadOnlyField()
    flavor_group = FlavorGroupBriefSerializer(read_only=True)

    class Meta:
        # TODO(tomo): Set read_only_fields or write_only...
        model = models.OpenstackInstanceFlavor
        exclude = ('is_public', 'disabled', 'deleted', 'show_in_fleio', 'rxtx_factor', 'vcpu_weight', 'show_to_groups')


class FloatingIpMinSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FloatingIp
        fields = ('id', 'floating_ip_address')


class InstanceSerializer(FieldsModelSerializer):
    allowed_actions = serializers.SerializerMethodField()
    access_ip = serializers.CharField(read_only=True)
    os_distro = serializers.SerializerMethodField()
    # TODO(tomo): Remove the below fields once replacement of models is over
    uuid = serializers.CharField(source='id')
    display_status = serializers.CharField()
    display_task = serializers.CharField()
    region_obj = serializers.SerializerMethodField()
    flavor = FlavorSerializer(read_only=True)

    class Meta:
        model = models.Instance
        fields = (
            'id', 'name', 'allowed_actions', 'access_ip', 'os_distro', 'uuid', 'created',
            'display_status', 'display_task', 'description', 'image', 'region', 'region_obj',
            'flavor', 'status', 'booted_from_iso', 'locked', 'current_cycle_traffic',
            'current_month_traffic', 'hostId', 'host_name',
        )
        read_only_fields = (
            'id', 'allowed_actions', 'access_ip', 'os_distro', 'uuid', 'created',
            'display_status', 'display_task', 'image', 'region', 'region_obj',
            'flavor', 'status', 'booted_from_iso', 'locked', 'current_cycle_traffic',
            'current_month_traffic',
        )

    def allowed(self):
        allowed = copy.deepcopy(INSTANCE_ALLOWED_ACTIONS)
        if active_features.is_enabled('openstack.floatingips'):
            allowed[InstanceStatus.ACTIVE] += ['associate_ip', 'dissociate_ip']
            allowed[InstanceStatus.STOPPED] += ['associate_ip', 'dissociate_ip']
        if active_features.is_enabled('openstack.instances.allow_changing_password'):
            allowed[InstanceStatus.ACTIVE] += ['change_password', ]
        return allowed

    def get_allowed_actions(self, obj):
        return self.allowed().get(obj.status, [])

    def get_os_distro(self, obj):
        try:
            related_image = obj.image
            return related_image.os_distro if related_image and related_image.os_distro else None
        except models.Image.DoesNotExist:
            pass
        # FIXME(tomo): Try to get the actual bootable volume
        if obj.volumes_attached and len(obj.volumes_attached):
            volumes_attached = models.VolumeAttachments.objects.filter(server_id=obj.id)
            volume = models.Volume.objects.filter(id__in=volumes_attached.values_list('volume_id'),
                                                  bootable=True).first()
            if volume and 'volume_image_metadata' in volume.extra:
                if 'os_distro' in volume.extra['volume_image_metadata']:
                    return volume.extra['volume_image_metadata'].get('os_distro', None)

    @staticmethod
    def get_region_obj(model: Instance):
        return RegionSerializer().to_representation(model.region_obj) if model.region_obj is not None else None


class InstanceDetailSerializer(serializers.ModelSerializer):
    net_details = serializers.SerializerMethodField()
    # TODO(tomo): Replace the below fields after module change
    image = ImageSerializer(read_only=True)
    flavor = FlavorSerializer(read_only=True)
    uuid = serializers.CharField(source='id', read_only=True)
    project = serializers.CharField(read_only=True, source='project_id')
    display_status = serializers.CharField()
    display_task = serializers.CharField()

    os_distro = serializers.SerializerMethodField()
    allowed_actions = serializers.SerializerMethodField()
    region_obj = serializers.SerializerMethodField()
    traffic_type = serializers.SerializerMethodField()

    class Meta:
        model = models.Instance
        fields = (
            'id', 'name', 'allowed_actions', 'access_ip', 'os_distro', 'uuid', 'created',
            'display_status', 'display_task', 'description', 'image', 'region', 'region_obj',
            'flavor', 'net_details', 'project', 'status', 'booted_from_iso', 'locked',
            'current_cycle_traffic', 'current_month_traffic', 'traffic_type', 'hostId', 'host_name',
        )
        read_only_fields = (
            'id', 'name', 'allowed_actions', 'access_ip', 'os_distro', 'uuid', 'created',
            'display_status', 'display_task', 'image', 'region', 'region_obj',
            'flavor', 'net_details', 'project', 'booted_from_iso', 'locked',
            'current_cycle_traffic', 'current_month_traffic', 'traffic_type',
        )

    def allowed(self):
        allowed = copy.deepcopy(INSTANCE_ALLOWED_ACTIONS)
        if active_features.is_enabled('openstack.floatingips'):
            allowed[InstanceStatus.ACTIVE] += ['associate_ip', 'dissociate_ip']
            allowed[InstanceStatus.STOPPED] += ['associate_ip', 'dissociate_ip']
        if active_features.is_enabled('openstack.instances.allow_changing_password'):
            allowed[InstanceStatus.ACTIVE] += ['change_password', ]
        return allowed

    def get_traffic_type(self, value):
        return getattr(settings, 'INSTANCE_TRAFFIC_DISPLAY', 'all')

    def get_net_details(self, obj):
        # FIXME(tomo): refactor this. Ports have FKs to Networks and Projects now
        ports_objects = models.Port.objects.filter(device_id=obj.id)
        floating_ips = models.FloatingIp.objects.filter(port__in=ports_objects)
        grouped_ips = list()
        ports = list()
        for port in ports_objects:
            ipv4s = list()
            ipv6s = list()
            for fixed_ip in port.fixed_ips:
                try:
                    ipaddress.IPv4Address(fixed_ip['ip_address'])
                    ipv4s.append({'ip_address': fixed_ip['ip_address'], 'subnet_id': fixed_ip['subnet_id']})
                except (ValueError, KeyError):
                    pass
                try:
                    ipaddress.IPv6Address(fixed_ip['ip_address'])
                    ipv6s.append({'ip_address': fixed_ip['ip_address'], 'subnet_id': fixed_ip['subnet_id']})
                except (ValueError, KeyError):
                    pass
            grouped_ips.append({'network_name': port.network_name(), 'ipv4s': ipv4s, 'ipv6s': ipv6s})
            ports.append({
                'id': port.id,
                'name': port.name or port.id,
                'ipv4s': ipv4s,
                'ipv6s': ipv6s,
                'floating_ips': FloatingIpMinSerializer(instance=floating_ips, many=True).data,
            })
        return {
            'grouped_ips': grouped_ips,
            'ports': ports,
        }

    def get_allowed_actions(self, obj):
        return self.allowed().get(obj.status, [])

    def get_os_distro(self, obj):
        try:
            related_image = obj.image
            return related_image.os_distro if related_image and related_image.os_distro else None
        except models.Image.DoesNotExist:
            pass
        # FIXME(tomo): Try to get the actual bootable volume
        if obj.volumes_attached and len(obj.volumes_attached):
            volumes_attached = models.VolumeAttachments.objects.filter(server_id=obj.id)
            volume = models.Volume.objects.filter(id__in=volumes_attached.values_list('volume_id'),
                                                  bootable=True).first()
            if volume and 'volume_image_metadata' in volume.extra:
                if 'os_distro' in volume.extra['volume_image_metadata']:
                    return volume.extra['volume_image_metadata'].get('os_distro', None)

    @staticmethod
    def get_region_obj(model: Instance):
        return RegionSerializer().to_representation(model.region_obj) if model.region_obj is not None else None


class InstanceBootSourceSerializer(serializers.Serializer):
    BOOT_SOURCE = (('image', _('Image')),
                   ('owned_image', _('Owned Image')),
                   ('shared_image', _('Shared Image')),
                   ('community_image', _('Community Image')),
                   ('volume', _('Volume')),
                   ('volume_snapshot', _('Volume Snapshot')),
                   ('requested_image', _('Requested Image')),
                   ('requested_volume', _('Requested Volume')))
    source_id = serializers.CharField(max_length=64, required=True)
    source_type = serializers.ChoiceField(BOOT_SOURCE, required=True)
    delete_on_termination = serializers.BooleanField(write_only=True, required=False)
    create_new_volume = serializers.BooleanField(write_only=True, required=False)
    volume_size = serializers.IntegerField(write_only=True, required=False)
    volume_type = serializers.CharField(write_only=True, allow_null=True, default=None, required=False,
                                        allow_blank=True)
    image = serializers.HiddenField(default=None)
    boot_device = serializers.HiddenField(default=None)

    def to_internal_value(self, data):
        value = super(InstanceBootSourceSerializer, self).to_internal_value(data)

        # Check if volume booting is enabled, otherwise raise
        is_staff = self.context['request'].user.is_staff
        if is_staff:
            volume_boot_feature = (
                staff_active_features.is_enabled('openstack.volumes') and
                staff_active_features.is_enabled('openstack.volumes.boot')
            )
        else:
            volume_boot_feature = (
                active_features.is_enabled('openstack.volumes') and
                active_features.is_enabled('openstack.volumes.boot')
            )
        source_type = value.get('source_type')
        if not volume_boot_feature and (value.get('create_new_volume', False) or
                                        source_type in ('volume', 'volume_snapshot')):
            raise serializers.ValidationError(detail=_('Booting from a volume is disabled'))
        # End of volume boot check

        if value.get('volume_type') == 'default':
            value['volume_type'] = None
        source_id = value['source_id']
        dev_mapping_v1 = None
        dev_mapping_v2 = None
        delete_on_termination = value.get('delete_on_termination', False)
        create_new_volume = value.get('create_new_volume', False)
        volume_size = value.get('volume_size')

        if source_type in ('image', 'owned_image', 'shared_image', 'requested_image', 'community_image'):
            try:
                db_image = models.Image.objects.get(id=source_id)
            except models.Image.DoesNotExist:
                raise ValidationError(dict(image=[_('Image not found')]))
            if create_new_volume:
                volume_size = volume_size if volume_size and volume_size >= db_image.min_disk else db_image.min_disk
                if not volume_size:
                    raise ValidationError({'detail': _('Volume size is not valid')})
                dev_mapping_v2 = [{"boot_index": "0",
                                   "uuid": source_id,
                                   "source_type": "image",
                                   "destination_type": "volume",
                                   "volume_size": volume_size,
                                   "delete_on_termination": delete_on_termination,
                                   }]
            else:
                value['image'] = db_image  # NOTE(tomo): Used for instance FK set
        elif source_type in ('volume', 'volume_snapshot', 'requested_volume'):
            try:
                if source_type == 'volume':
                    db_volume = models.Volume.objects.get(id=source_id)
                elif source_type == 'volume_snapshot':
                    db_volume = models.VolumeSnapshot.objects.get(id=source_id)
                else:
                    db_volume = models.Volume.objects.get(id=source_id)
            except models.Volume.DoesNotExist:
                raise ValidationError({'detail': _('Volume not found')})
            except models.VolumeSnapshot.DoesNotExist:
                raise ValidationError({'detail': _('Volume snapshot not found')})

            volume_size = volume_size if volume_size else db_volume.size
            if not volume_size:
                raise ValidationError({'detail': _('Volume size is not valid')})

            if source_type == 'volume':
                dev_mapping_v2 = [{"boot_index": "0",
                                   "uuid": source_id,
                                   "source_type": "volume",
                                   "volume_size": volume_size,
                                   "destination_type": "volume",
                                   "delete_on_termination": delete_on_termination,
                                   }]
            elif source_type == 'volume_snapshot':
                dev_mapping_v2 = [{"boot_index": "0",
                                   "uuid": source_id,
                                   "source_type": "snapshot",
                                   "destination_type": "volume",
                                   "delete_on_termination": delete_on_termination,
                                   }]
            else:
                dev_mapping_v1 = {'vda': '{}:snap:{}:{}'.format(source_id, volume_size, int(delete_on_termination))}

        boot_device = None
        if dev_mapping_v2:
            for block_device in dev_mapping_v2:
                if block_device.get('boot_index') == '0':
                    boot_device = block_device
        value['boot_device'] = boot_device

        # NOTE(tomo): If a volume is involved (bootable or just created from image) these should be defined else None
        value['dev_mapping_v1'] = dev_mapping_v1
        value['dev_mapping_v2'] = dev_mapping_v2
        return value

    def to_representation(self, instance):
        return {}

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class InstanceCreateSerializer(serializers.Serializer):
    client = serializers.CharField(required=False, write_only=True)
    name = serializers.CharField(max_length=128, required=True)
    boot_source = InstanceBootSourceSerializer(write_only=True, required=True)
    flavor = serializers.PrimaryKeyRelatedField(queryset=models.OpenstackInstanceFlavor.objects)
    region = serializers.PrimaryKeyRelatedField(queryset=models.OpenstackRegion.objects.enabled())
    root_password = serializers.CharField(write_only=True, required=False)
    ssh_keys = serializers.CharField(write_only=True, required=False)
    nics = serializers.ListField(required=False, write_only=True, allow_null=True)
    user_data = serializers.CharField(
        default=None, write_only=True, allow_null=True, allow_blank=True, max_length=21844
    )

    class Meta:
        fields = ('client', 'name', 'boot_source', 'flavor', 'region', 'root_password', 'ssh_keys', 'nics',
                  'user_data',)

    def get_fields(self):
        fields = super().get_fields()
        if 'view' in self.context:
            request = self.context['view'].request
            clients = request.user.clients.all()
            client_groups = ClientGroup.objects.none()
            for client in clients:
                client_groups = (client_groups | client.groups.all()).distinct()
            new_queryset = models.OpenstackInstanceFlavor.objects.filter(
                Q(show_to_groups__in=client_groups) | Q(show_to_groups__isnull=True)
            )
            new_queryset = new_queryset.filter(show_in_fleio=True)
            fields['flavor'].queryset = new_queryset
        return fields

    @staticmethod
    def validate_root_password(password):
        if password:
            validate_password(password)
        return password

    def validate_client(self, client_id):
        request = self.context.get('request', None)
        assert request, 'Serializer can only be used with http requests'

        try:
            client = request.user.clients.filter(id=client_id, services__openstack_project__isnull=False).first()
        except ObjectDoesNotExist:
            raise ValidationError(_('A client with id {} does not exist').format(client_id))
        except (TypeError, ValueError):
            raise ValidationError(_('Invalid client id provided: {}').format(client_id))
        except Exception as e:
            LOG.exception(e)
            raise ValidationError(_('Unable retrieve the client associated with your account'))
        if not client:
            raise ValidationError(_('Unable to find a client account'))
        return client

    def to_internal_value(self, data):
        """
        Perform any data modification here.
        to_internal_value is called before .validate() and after each field is validated.
        """
        value = super(InstanceCreateSerializer, self).to_internal_value(data)

        errors = OrderedDict()
        db_region = value['region']

        client = value['client']
        flavor = value['flavor']
        boot_source = value['boot_source']

        request = self.context.get('request', None)
        assert request, 'Serializer can only be used with http requests'

        # Try to get a project by client
        project = client.first_project
        if project is None:
            raise ValidationError({'detail': _('Unable to find a client with an OpenStack project associated')})
        value['project'] = project

        # Validate boot source
        if boot_source['source_type'] in ('image', 'owned_image', 'shared_image', 'community_image'):
            try:
                models.Image.objects.get_images_for_project(
                    project_id=project.project_id).get(id=boot_source['source_id'])
            except models.Image.DoesNotExist:
                raise ValidationError({'detail': _('Boot source image not found')})
        else:
            try:
                if boot_source['source_type'] == 'volume':
                    models.Volume.objects.get(id=boot_source['source_id'], project__project_id=project.project_id)
                elif boot_source['source_type'] == 'volume_snapshot':
                    models.VolumeSnapshot.objects.get(
                        id=boot_source['source_id'], project__project_id=project.project_id
                    )
                else:
                    models.Volume.objects.get(id=boot_source['source_id'],
                                              project__project_id=project.project_id)
            except models.Volume.DoesNotExist:
                raise ValidationError({'detail': _('Boot source volume not found')})
            except models.VolumeSnapshot.DoesNotExist:
                raise ValidationError({'detail': _('Boot source volume snapshot not found')})

        # Nics
        compute_api_version = APIVersion(plugin_settings.COMPUTE_API_VERSION)
        nics = value.get('nics')
        if nics:
            value['nics'] = [{'net-id': n} for n in nics]
        elif compute_api_version > APIVersion('2.37'):
            if plugin_settings.AUTO_ALLOCATED_TOPOLOGY:
                value['nics'] = 'auto'
            else:
                value['nics'] = 'none'  # neutron expects it as none string rather than bool

        # SSH Key
        ssh_keys = value.get('ssh_keys', None)
        if ssh_keys:
            ssh_keys = json.loads(ssh_keys)
            pkm_keys_dict = {}
            for ssh_key in ssh_keys:
                try:
                    pkm_key = PublicKey.objects.get(id=ssh_key, user__in=client.users.all())
                    pkm_keys_dict[ssh_key] = newlines_substract(pkm_key.public_key)
                except PublicKey.DoesNotExist:
                    errors['ssh_keys'] = [_('SSH Key not found')]
            value['ssh_keys'] = pkm_keys_dict

        if flavor.region != db_region:
            errors['flavor'] = [_('Flavor not in {}').format(db_region.id)]

        if errors:
            raise ValidationError(errors)

        return value


class InstanceChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, max_length=128)

    def validate_password(self, password):
        return validate_password(password)


class InstanceRebuildSerializer(serializers.Serializer):
    image = serializers.CharField(write_only=True, max_length=36)
    root_password = serializers.CharField(write_only=True, max_length=128, required=False, allow_blank=True)
    name = serializers.CharField(write_only=True, max_length=128, required=False)
    ssh_keys = serializers.CharField(write_only=True, required=False)
    client_id = serializers.CharField(required=False)
    user_data = serializers.CharField(
        default=None, write_only=True, allow_null=True, allow_blank=True, max_length=21844
    )

    def validate_root_password(self, password):
        if password:
            validate_password(password)
        return password

    def to_internal_value(self, data):
        value = super(InstanceRebuildSerializer, self).to_internal_value(data)
        errors = OrderedDict()
        client_id = value.get('client_id', None)
        if client_id:
            client = Client.objects.filter(id=client_id).first()
            ssh_keys = value.get('ssh_keys', None)
            if ssh_keys:
                ssh_keys = json.loads(ssh_keys)
                pkm_keys_dict = {}
                for ssh_key in ssh_keys:
                    try:
                        pkm_key = PublicKey.objects.get(id=ssh_key, user__in=client.users.all())
                        pkm_keys_dict[ssh_key] = newlines_substract(pkm_key.public_key)
                    except PublicKey.DoesNotExist:
                        errors['ssh_keys'] = [_('SSH Key not found')]
                value['ssh_keys'] = pkm_keys_dict
        else:
            ssh_keys = value.get('ssh_keys', None)
            if ssh_keys:
                ssh_keys = json.loads(ssh_keys)
                pkm_keys_dict = {}
                for ssh_key in ssh_keys:
                    try:
                        pkm_key = PublicKey.objects.get(id=ssh_key)
                        pkm_keys_dict[ssh_key] = newlines_substract(pkm_key.public_key)
                    except PublicKey.DoesNotExist:
                        errors['ssh_keys'] = [_('SSH Key not found')]
                value['ssh_keys'] = pkm_keys_dict
        if errors:
            raise ValidationError(errors)
        return value


class InstanceRescueSerializer(serializers.Serializer):
    image = serializers.CharField(write_only=True, max_length=36)
    root_password = serializers.CharField(write_only=True, max_length=128, required=False, allow_blank=True)

    def validate_root_password(self, password):
        if password:
            validate_password(password)
        return password


class InstanceBootFromIsoSerializer(serializers.Serializer):
    image = serializers.CharField(write_only=True, max_length=36)


class InstanceResizeSerializer(serializers.Serializer):
    flavor = serializers.CharField(write_only=True, max_length=36)


class InstanceNameSerializer(serializers.Serializer):
    name = serializers.CharField(write_only=True, max_length=128, required=True)


class SysLogLengthSerializer(serializers.Serializer):
    length = serializers.IntegerField(min_value=0, max_value=1000)


class InstanceActionsSerializer(serializers.Serializer):
    """
    Serialize the instance history log (instance actions in OpenStack)
    """
    start_time = serializers.DateTimeField(read_only=True)
    action = serializers.CharField(read_only=True)
    message = serializers.CharField(read_only=True)
    request_id = serializers.CharField(read_only=True)


class InstanceActionDetailsEventSerializer(serializers.Serializer):
    start_time = serializers.DateTimeField(read_only=True)
    result = serializers.CharField(read_only=True)
    finish_time = serializers.DateTimeField(read_only=True)
    event = serializers.CharField(read_only=True)
    traceback = serializers.CharField(read_only=True)


class InstanceActionDetailsSerializer(serializers.Serializer):
    start_time = serializers.DateTimeField(read_only=True)
    user_id = serializers.CharField(read_only=True)
    message = serializers.CharField(read_only=True)
    instance_uuid = serializers.CharField(read_only=True)
    request_id = serializers.CharField(read_only=True)
    project_id = serializers.CharField(read_only=True)
    action = serializers.CharField(read_only=True)
    events = InstanceActionDetailsEventSerializer(many=True)


class VolumeIdSerializer(serializers.Serializer):
    volume_id = serializers.CharField(write_only=True, max_length=36)


class IpSerializer(serializers.Serializer):
    ip = serializers.IPAddressField(required=True)


class AddFloatingIpSerializer(serializers.Serializer):
    floating_ip = serializers.IPAddressField(required=True)
    fixed_ip = serializers.IPAddressField(required=False)


class FloatingIpListFilterSerializer(serializers.Serializer):
    # status 'DOWN' means unused, 'ACTIVE' means used
    status = serializers.CharField(required=False)

    def validate_status(self, status):
        if status not in ['ACTIVE', 'DOWN']:
            raise ValidationError(_('Not a valid status'))
        return status


class MigrateSerializer(serializers.Serializer):
    hypervisor = serializers.CharField(required=False)
    block_migration = serializers.BooleanField(default=False)
    live_migrate = serializers.BooleanField(default=True)
    over_commit = serializers.BooleanField(default=False)

    def to_internal_value(self, data):
        value = super(MigrateSerializer, self).to_internal_value(data)
        if data['live_migrate'] and not data.get('hypervisor', None):
            raise ValidationError(_('Must select hypervisor with live migration'))

        return value
