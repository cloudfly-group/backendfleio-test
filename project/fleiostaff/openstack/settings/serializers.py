from __future__ import unicode_literals

from django.utils.encoding import force_text
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from keystoneauth1.exceptions import (ConnectFailure, EndpointNotFound, NotFound, SSLError,
                                      Unauthorized, VersionNotAvailable)
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from fleio.openstack.models import OpenstackRegion, VolumeType
from fleio.openstack.api.keystone import keystone_client
from fleio.conf.serializer import ConfSerializer


class OpenstackSettingsSerializer(ConfSerializer):
    """All Openstack settings under one serializer."""
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        fields = ('auth_url', 'username', 'password', 'user_domain_id', 'user_project_id', 'require_valid_ssl',
                  'default_interface')

    def validate(self, attrs):
        password = attrs.get('password', None)
        # Check password is set if no other password is sent
        if not password:
            try:
                password = self.instance.password
            except Exception as e:
                raise ValidationError({'password': force_text(e)})
            if not password:
                raise ValidationError({'password': _('OpenStack user password is required')})

        ksc = keystone_client(auth_url=attrs.get('auth_url'),
                              username=attrs.get('username'),
                              password=password,
                              user_domain_id=attrs.get('user_domain_id'),
                              user_project_id=attrs.get('user_project_id'),
                              verify=attrs.get('require_valid_ssl', False),
                              interface=attrs.get('default_interface'))
        err_msg = None
        try:
            ksc.regions.list()
        except (NotFound, VersionNotAvailable, EndpointNotFound):
            err_msg = _('Could not find a suitable endpoint for Keystone')
        except ConnectFailure as e:
            err_msg = e.args[0]
        except Unauthorized as e:
            err_msg = _('{} Please check your credentials and try again').format(e)
        except SSLError:
            err_msg = _('Keystone SSL certificate is invalid. '
                        'Check certificate for region with auth url: {0}'.format(attrs.get('auth_url')))
        except Exception as e:
            err_msg = force_text(e)
        finally:
            if err_msg:
                raise ValidationError(err_msg)
        return attrs


class DefaultsSettingsSerializer(ConfSerializer):
    class Meta:
        fields = (
            'timeout',
            'default_role',
            'default_region',
            'default_project_name',
            'default_project_description',
            'project_domain_id',
            'hide_projects_and_api_users',
            'hide_project_ids',
            'auto_allocated_topology',
            'prefix_api_users_with_username',
            'force_config_drive_for_instance_creation',
        )

    def validate(self, attrs):
        current_settings = self.instance
        default_role = attrs.get('default_role')
        default_region = attrs.get('default_region')
        project_domain_id = attrs.get('project_domain_id')
        auth_url = current_settings.auth_url
        password = current_settings.password
        username = current_settings.username
        user_project_id = current_settings.user_project_id
        user_domain_id = current_settings.user_domain_id

        kc = keystone_client(auth_url=auth_url,
                             username=username,
                             password=password,
                             user_project_id=user_project_id,
                             user_domain_id=user_domain_id)
        try:
            roles = kc.roles.list()
            regions = kc.regions.list()
            domains = kc.domains.list()
        except Exception as e:
            raise ValidationError(
                detail=_('Please set a valid set of OpenStack credentials first.')
            )
        if default_role not in [r.name for r in roles]:
            raise ValidationError({'default_role': _('Role {} does not exist').format(default_role)})
        if default_region not in [r.id for r in regions]:
            raise ValidationError({'default_region': _('Region {} does not exist').format(default_region)})
        if project_domain_id not in [d.id for d in domains]:
            raise ValidationError({'project_domain_id': _('Domain with ID {} not found').format(project_domain_id)})
        return attrs


class VolumeSizeIncrementsSerializer(ConfSerializer):
    class Meta:
        fields = ('volume_size_increments', )

    def to_representation(self, instance):
        current_repr = super(VolumeSizeIncrementsSerializer, self).to_representation(instance=instance)
        size_increments = {}
        for volume_type in VolumeType.objects.all():
            try:
                current_vsi = current_repr.get('volume_size_increments')
                current_size_increment = current_vsi[volume_type.region_id][volume_type.name]
            except (TypeError, LookupError, AttributeError, ValueError):
                current_size_increment = 1
            if volume_type.region_id:
                if volume_type.region_id not in size_increments:
                    size_increments[volume_type.region_id] = {volume_type.name: current_size_increment}
                else:
                    size_increments[volume_type.region_id][volume_type.name] = current_size_increment

        return {'volume_size_increments': size_increments}

    @staticmethod
    def validate_volume_size_increments(value):
        if not isinstance(value, dict):
            raise serializers.ValidationError(detail='volume_size_increments is invalid')
        for region, vsi in iter(value.items()):
            if not isinstance(vsi, dict):
                raise serializers.ValidationError(detail='Invalid size increment')
            for vol_type_name, size_incr in iter(vsi.items()):
                if not size_incr:
                    size_incr = 1  # Empty/null or 0 defaults to 1
                try:
                    vsi[vol_type_name] = int(size_incr)
                except ValueError:
                    invalid_size_msg = 'Invalid size for {} in region {}'.format(vol_type_name, region)
                    raise serializers.ValidationError(detail=invalid_size_msg)
            if not OpenstackRegion.objects.filter(id=region).exists():
                raise serializers.ValidationError(detail='region {} does not exist'.format(region))
            if value[region] == {}:
                del value[region]  # NOTE(tomo): Delete
        return value


class NotificationsSettingsSerializer(ConfSerializer):
    notifications_settings_version = serializers.HiddenField(default=now)

    class Meta:
        fields = ('notifications_url', 'notifications_topic', 'notifications_exchange', 'notifications_pool',
                  'notifications_settings_version')

    def validate(self, attrs):
        notifications_url = attrs.get('notifications_url', None)
        if not notifications_url:
            try:
                notifications_url = self.instance.notifications_url
            except Exception as e:
                raise ValidationError({'notifications_url': force_text(e)})
            if not notifications_url:
                raise ValidationError({'notifications_url': _('Notification url is required')})

        return attrs
