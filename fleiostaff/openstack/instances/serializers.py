import copy
import ipaddress
import json
import logging
from collections import OrderedDict

from cinderclient.api_versions import APIVersion
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from fleio.core.clients.serializers import ClientMinSerializer
from fleio.core.features import staff_active_features
from fleio.core.models import Client
from fleio.openstack import models as openstack_models
from fleio.openstack.api.identity import IdentityAdminApi
from fleio.openstack.images.api import Image
from fleio.openstack.instances.instance_status import InstanceStatus
from fleio.openstack.instances.serializers import InstanceBootSourceSerializer
from fleio.openstack.instances.serializers import InstanceDetailSerializer
from fleio.openstack.instances.serializers import InstanceSerializer
from fleio.openstack.instances.serializers import validate_password
from fleio.openstack.models.image import OpenStackImageVisibility
from fleio.openstack.settings import plugin_settings
from fleio.openstack.utils import newlines_substract
from fleio.pkm.models import PublicKey

LOG = logging.getLogger(__name__)

INSTANCE_ALLOWED_ACTIONS = {
    InstanceStatus.ACTIVE: [
        'reboot', 'shutoff', 'resize', 'rescue', 'rebuild', 'console', 'rename', 'create_snapshot', 'suspend',
        'add_port', 'remove_port', 'add_ip', 'remove_ip', 'migrate', 'abort_migrate', 'attach_volume', 'move',
        'boot_from_iso', 'lock', 'unlock',
    ],
    InstanceStatus.STOPPED: [
        'start', 'resize', 'rescue', 'rebuild', 'rename', 'create_snapshot', 'lock', 'unlock', 'add_port',
        'remove_port', 'add_ip', 'remove_ip', 'migrate', 'abort_migrate', 'attach_volume', 'move', 'boot_from_iso',
    ],
    InstanceStatus.RESCUED: ['unrescue', 'console', 'add_port', 'remove_port', 'add_ip', 'remove_ip'],
    InstanceStatus.BOOTED_FROM_ISO: ['unmount_and_reboot', 'console', 'add_port', 'remove_port', 'add_ip', 'remove_ip'],
    InstanceStatus.RESIZED: ['cfresize', 'console', 'add_port', 'remove_port', 'add_ip', 'remove_ip', 'attach_volume'],
    InstanceStatus.ERROR: ['reset_state', 'delete'],
    InstanceStatus.SUSPENDED: ['resume', 'lock', 'unlock', 'add_port', 'remove_port', 'add_ip', 'remove_ip', 'migrate']
}


class MoveSerializer(serializers.Serializer):
    client = serializers.IntegerField(allow_null=False)

    @staticmethod
    def validate_client(client_id: int) -> int:
        try:
            client = Client.objects.get(id=client_id)
            if not client.first_project:
                raise ValidationError(
                    _('Client {}({}) does not have an openstack project.').format(client, client.id)
                )

            if client.first_project.disabled:
                raise ValidationError(
                    _('The openstack project associated with client {}({}) is disabled.').format(client, client.id)
                )
        except Client.DoesNotExist:
            raise ValidationError(_('Client {} does not exist').format(client_id))
        else:
            return client_id

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class AdminInstanceSerializer(InstanceSerializer):
    client = ClientMinSerializer(source='project.service.client', read_only=True, default=None)
    host_name = serializers.CharField()

    class Meta(InstanceSerializer.Meta):
        fields = InstanceSerializer.Meta.fields + ('client', 'host_name')

    def allowed(self):
        allowed = copy.deepcopy(INSTANCE_ALLOWED_ACTIONS)
        if staff_active_features.is_enabled('openstack.floatingips'):
            allowed[InstanceStatus.ACTIVE] += ['associate_ip', 'dissociate_ip']
            allowed[InstanceStatus.STOPPED] += ['associate_ip', 'dissociate_ip']
        if staff_active_features.is_enabled('openstack.instances.allow_changing_password'):
            allowed[InstanceStatus.ACTIVE] += ['change_password', ]
        return allowed


class AdminInstanceDetailSerializer(InstanceDetailSerializer):
    client = ClientMinSerializer(source='project.service.client', read_only=True, default=None)

    class Meta(InstanceDetailSerializer.Meta):
        fields = InstanceDetailSerializer.Meta.fields + ('client', 'hostId', 'host_name',)

    def allowed(self):
        allowed = copy.deepcopy(INSTANCE_ALLOWED_ACTIONS)
        if staff_active_features.is_enabled('openstack.floatingips'):
            allowed[InstanceStatus.ACTIVE] += ['associate_ip', 'dissociate_ip']
            allowed[InstanceStatus.STOPPED] += ['associate_ip', 'dissociate_ip']
        if staff_active_features.is_enabled('openstack.instances.allow_changing_password'):
            allowed[InstanceStatus.ACTIVE] += ['change_password', ]
        return allowed

    def get_net_details(self, obj):
        ports_objects = openstack_models.Port.objects.filter(device_id=obj.id)
        floating_ips = openstack_models.FloatingIp.objects.filter(port__in=ports_objects).values('id',
                                                                                                 'floating_ip_address')
        ports = list()
        for port in ports_objects:
            ipv4s = list()
            ipv6s = list()
            for fixed_ip in port.fixed_ips:
                try:
                    ip_obj = ipaddress.ip_address(fixed_ip['ip_address'])
                except ValueError:
                    continue
                if isinstance(ip_obj, ipaddress.IPv4Address):
                    ipv4s.append({'ip_address': fixed_ip['ip_address'], 'subnet_id': fixed_ip['subnet_id']})
                elif isinstance(ip_obj, ipaddress.IPv6Address):
                    ipv6s.append({'ip_address': fixed_ip['ip_address'], 'subnet_id': fixed_ip['subnet_id']})
                else:
                    continue
            ports.append({
                'id': port.id,
                'name': port.name or port.id,
                'ipv4s': ipv4s,
                'ipv6s': ipv6s,
                'floating_ips': floating_ips,
            })
        return {'ports': ports}


class AdminInstanceCreateSerializer(serializers.Serializer):
    client = serializers.CharField(required=True, write_only=True)
    name = serializers.CharField(max_length=128, required=True)
    boot_source = InstanceBootSourceSerializer(write_only=True, required=True)
    flavor = serializers.PrimaryKeyRelatedField(queryset=openstack_models.OpenstackInstanceFlavor.objects)
    region = serializers.PrimaryKeyRelatedField(queryset=openstack_models.OpenstackRegion.objects.enabled())
    root_password = serializers.CharField(write_only=True, required=False)
    ssh_keys = serializers.CharField(write_only=True, required=False)
    nics = serializers.ListField(required=False, write_only=True, allow_null=True)
    share_image = serializers.BooleanField(
        default=False, write_only=True, allow_null=True,
        help_text='Whether to actually allow a private image to be shared'
    )
    user_data = serializers.CharField(
        default=None, write_only=True, allow_null=True, allow_blank=True, max_length=21844
    )

    class Meta:
        fields = ('client', 'name', 'boot_source', 'flavor', 'region', 'root_password', 'ssh_keys', 'nics',
                  'share_image', 'user_data',)

    @staticmethod
    def validate_root_password(password):
        if password:
            validate_password(password)
        return password

    @staticmethod
    def validate_client(client_id):
        try:
            client = Client.objects.get(id=client_id)
        except Client.DoesNotExist:
            raise ValidationError(_('A client with id {} does not exist').format(client_id))
        except (TypeError, ValueError):
            raise ValidationError(_('Invalid client id provided: {}').format(client_id))
        return client

    def to_internal_value(self, data):
        """
        Perform any data modification here.
        to_internal_value is called before .validate() and after each field is validated.
        """
        request = self.context.get('request', None)
        assert request, 'Serializer can only be used with http requests'

        value = super(AdminInstanceCreateSerializer, self).to_internal_value(data)

        errors = OrderedDict()
        db_region = value['region']

        client = value['client']
        flavor = value['flavor']
        boot_source = value['boot_source']
        share_image = value['share_image']

        # Try to get a project by client
        project = client.first_project
        if project is None:
            raise ValidationError({'detail': _('Unable to find a client with an OpenStack project associated')})
        value['project'] = project

        # Validate boot source
        if boot_source['source_type'] in ('image', 'owned_image', 'shared_image', 'requested_image',
                                          'community_image'):
            try:
                openstack_models.Image.objects.get_images_for_project(
                    project_id=project.project_id).get(id=boot_source['source_id'])
            except openstack_models.Image.DoesNotExist:
                # Share the image with the client's project if it exists
                if share_image:
                    try:
                        db_image = openstack_models.Image.objects.get(id=boot_source['source_id'])
                    except openstack_models.Image.DoesNotExist:
                        raise ValidationError({'boot_source': _('Image not found')})
                    else:
                        try:
                            request_session = getattr(self.context.get('request'), 'session', None)
                            admapi = IdentityAdminApi(request_session=request_session)
                            if db_image.visibility == OpenStackImageVisibility.PRIVATE:
                                api_image = Image(db_image=db_image, api_session=admapi.session)
                                api_image.set_visibility(visibility=OpenStackImageVisibility.SHARED)
                                api_image.create_member(member_project_id=client.first_project.project_id)
                            elif db_image.visibility == OpenStackImageVisibility.SHARED:
                                api_image = Image(db_image=db_image, api_session=admapi.session)
                                api_image.create_member(member_project_id=client.first_project.project_id)
                        except Exception as e:
                            LOG.exception(e)
                            raise ValidationError({'boot_source': _('Unable to boot: {}').format(e)})
                else:
                    raise ValidationError({'boot_source': _('Image not found')})
        else:
            try:
                if boot_source['source_type'] in ('volume', 'requested_volume'):
                    openstack_models.Volume.objects.get(id=boot_source['source_id'],
                                                        project__project_id=project.project_id)
                elif boot_source['source_type'] == 'volume_snapshot':
                    openstack_models.VolumeSnapshot.objects.get(id=boot_source['source_id'],
                                                                project__project_id=project.project_id)
                else:
                    openstack_models.Volume.objects.get(id=boot_source['source_id'],
                                                        project__project_id=project.project_id)
            except openstack_models.Volume.DoesNotExist:
                raise ValidationError({'boot_source': _('Volume not available')})
            except openstack_models.VolumeSnapshot.DoesNotExist:
                raise ValidationError({'boot_source': _('Volume snapshot not available')})

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

        # SSH Keys
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

        # Set the actual flavor. Note that flavor names are unique per region.
        if flavor.region != db_region:
            errors['flavor'] = [_('Flavor not in {}'.format(db_region.id))]

        if errors:
            raise ValidationError(errors)

        return value
