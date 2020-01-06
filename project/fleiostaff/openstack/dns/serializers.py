from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from rest_framework import exceptions, serializers
from rest_framework.exceptions import ValidationError

from fleio.core.models import Client
from fleio.openstack.dns.serializers import RECORD_TYPES, ZONE_TYPES

from fleio.openstack.settings import plugin_settings


OPENSTACK_DESIGNATE_RECORDSET_LIMIT = getattr(settings, 'OPENSTACK_DESIGNATE_RECORDSET_LIMIT', 100000)


class RecordSetCreateSerializer(serializers.Serializer):
    region_name = serializers.CharField(required=False)
    name = serializers.CharField(max_length=255)
    type_ = serializers.ChoiceField(choices=RECORD_TYPES)
    records = serializers.ListField(min_length=1)
    ttl = serializers.IntegerField(required=False)
    description = serializers.CharField(max_length=255, required=False)
    sudo_project_id = serializers.UUIDField(required=False)

    def validate(self, attrs):
        if 'sudo_project_id' in attrs:
            attrs['sudo_project_id'] = attrs['sudo_project_id'].hex
        return attrs


class RecordSetListSerializer(serializers.Serializer):
    STATUS = (
        ('PENDING', _('Pending')),
        ('ACTIVE', _('Active')),
        ('ERROR', _('Error'))
    )

    region_name = serializers.CharField(required=False)
    name = serializers.CharField(max_length=255, required=False)
    type_ = serializers.ChoiceField(choices=RECORD_TYPES, required=False)
    ttl = serializers.IntegerField(required=False)
    description = serializers.CharField(max_length=255, required=False)
    status = serializers.ChoiceField(choices=STATUS, required=False)
    all_projects = serializers.BooleanField(default=True)
    limit = serializers.IntegerField(default=OPENSTACK_DESIGNATE_RECORDSET_LIMIT)

    def validate(self, attrs):
        if 'type_' in attrs:
            attrs['type'] = attrs.pop('type_')
        return attrs


class RecordSetUpdateSerializer(serializers.Serializer):
    region_name = serializers.CharField(required=False)
    records = serializers.ListField(required=False)
    ttl = serializers.IntegerField(required=False)
    description = serializers.CharField(max_length=255, required=False)
    all_projects = serializers.BooleanField(default=False)


class DnsUpdateSerializer(serializers.Serializer):
    """Base DNS serializer"""
    all_projects = serializers.BooleanField(default=True)
    sudo_project_id = serializers.UUIDField(format='hex', required=False)
    email = serializers.EmailField(required=False)
    ttl = serializers.IntegerField(required=False)
    description = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    region_name = serializers.CharField(required=False)
    masters = serializers.ListField(required=False, allow_null=True)
    type = serializers.ChoiceField(choices=ZONE_TYPES)

    def validate(self, attrs):
        sudo_project_id = attrs.get('sudo_project_id')
        all_projects = attrs.get('all_projects')

        if sudo_project_id and all_projects:
            raise exceptions.ValidationError({'detail': _('Cannot retrieve zones for all projects and '
                                                          'particular project at the same time')})
        elif sudo_project_id:
            attrs['sudo_project_id'] = sudo_project_id.hex

        return attrs


class DnsCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField(required=True)
    all_projects = serializers.BooleanField(default=False)
    sudo_project_id = serializers.UUIDField(format='hex', required=False)
    ttl = serializers.IntegerField(required=False)
    description = serializers.CharField(required=False)
    region_name = serializers.CharField(required=False)
    masters = serializers.ListField(required=False, allow_null=True)
    type_ = serializers.ChoiceField(choices=ZONE_TYPES)
    client = serializers.IntegerField(required=False, allow_null=True)

    def to_internal_value(self, data):
        values = super().to_internal_value(data)
        if not values['name'].endswith('.'):
            values['name'] += '.'
        if data.get('client', None):
            client_id = data['client']
            client = Client.objects.filter(id=client_id).first()
            if not client:
                raise ValidationError({'detail': _('No client found.')})
            project = client.first_project
            if not project:
                raise ValidationError({'detail': _('Client has no project.')})
            values['sudo_project_id'] = project.project_id
        else:
            try:
                values['sudo_project_id'] = plugin_settings.user_project_id
            except Exception as e:
                del e
                raise ValidationError({'detail': _('No project was chosen.')})
        return values


class DnsFilterSerializer(serializers.Serializer):
    ZONE_TYPE = (
        ('PRIMARY', _('Primary')),
        ('SECONDARY', _('Secondary'))
    )

    STATUS = (
        ('PENDING', _('Pending')),
        ('ACTIVE', _('Active')),
        ('ERROR', _('Error'))
    )

    all_projects = serializers.BooleanField(default=True)
    sudo_project_id = serializers.UUIDField(format='hex', required=False)
    email = serializers.EmailField(required=False)
    ttl = serializers.IntegerField(required=False)
    description = serializers.CharField(required=False)
    region_name = serializers.CharField(required=False)
    name = serializers.CharField(max_length=255, required=False)
    zone_type = serializers.ChoiceField(choices=ZONE_TYPE, required=False)
    status = serializers.ChoiceField(choices=STATUS, required=False)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        sudo_project_id = attrs.get('sudo_project_id')
        all_projects = attrs.get('all_projects')
        zone_type = attrs.pop('zone_type', None)

        if sudo_project_id and all_projects:
            raise exceptions.ValidationError({'detail': _('Cannot retrieve zones for all projects and '
                                                          'particular project at the same time')})
        elif sudo_project_id:
            attrs['sudo_project_id'] = sudo_project_id.hex

        if zone_type:
            attrs['type'] = zone_type

        return attrs


class DnsSerializer(serializers.Serializer):
    attributes = serializers.DictField()
    created_at = serializers.DateTimeField()
    description = serializers.CharField(required=False)
    email = serializers.EmailField(required=True)
    id = serializers.CharField(max_length=36)
    masters = serializers.ListField()
    name = serializers.CharField(max_length=255)
    project_id = serializers.CharField(max_length=36)
    serial = serializers.IntegerField()
    status = serializers.CharField(required=False)
    ttl = serializers.IntegerField(required=False, min_value=0, default=3600)
    type = serializers.ChoiceField(choices=ZONE_TYPES)
    updated_at = serializers.DateTimeField()
    version = serializers.IntegerField()

    def to_representation(self, instance):
        current_rep = super().to_representation(instance=instance)
        if current_rep['name'].endswith('.'):
            current_rep['name'] = current_rep['name'][:-1]
        return current_rep


class SyncRecordSetsSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=36, required=False, default=-1)
    records = serializers.ListField(min_length=1)
    zone_id = serializers.CharField(max_length=36)
    name = serializers.CharField(max_length=255)
    type = serializers.ChoiceField(choices=RECORD_TYPES)
    ttl = serializers.IntegerField(allow_null=True)
    deleted = serializers.BooleanField(default=False, required=False)
    created = serializers.BooleanField(default=False, required=False)
