from __future__ import unicode_literals

import ipaddress
import json
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from fleio.openstack.models import Project, SubnetPool


class StaffSubnetPoolSerializer(serializers.ModelSerializer):
    prefixes = serializers.JSONField()
    project_name = serializers.SerializerMethodField()

    class Meta:
        model = SubnetPool
        exclude = ('sync_version',)

    def get_project_name(self, subnet):
        project = Project.objects.filter(project_id=subnet.project_id).first()
        if project:
            return project.name
        else:
            return _('n/a')


class StaffSubnetPoolCreateSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    prefixes = serializers.JSONField(default=list())
    name = serializers.CharField()

    class Meta:
        model = SubnetPool
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'extra', 'ip_version')

    def to_internal_value(self, data):
        """
        Perform any data modification here.
        to_internal_value is called before .validate() and after each field is validated.
        """
        value = super(StaffSubnetPoolCreateSerializer, self).to_internal_value(data)

        request = self.context.get('request', None)
        assert request, 'Serializer can only be used with http requests.'

        if not int(data['min_prefixlen']) <= int(data['default_prefixlen']) <= int(data['max_prefixlen']):
            raise ValidationError({'detail': _('Prefix length specifications must follow the rule: Minimum prefix '
                                               'length <= Default prefix length <= Maximum prefix length')})

        prefixes = data.get('prefixes', None)
        if prefixes:
            if isinstance(prefixes, str):
                try:
                    prefixes = json.loads(prefixes)
                except json.decoder.JSONDecodeError:
                    raise ValidationError({'detail': _('Invalid CIDR.')})
            for prefix in prefixes:
                try:
                    ip = ipaddress.ip_network(prefix, strict=False)
                    if not int(data['min_prefixlen']) <= ip.prefixlen <= int(data['max_prefixlen']):
                        raise ValidationError({'detail': _('CIDR(s) prefix length must be greater or '
                                                           'equal to minimum prefix length and smaller '
                                                           'or equal to maximum prefix length.')})
                except ValueError:
                    raise ValidationError({'detail': _('Invalid CIDR.')})
        else:
            raise ValidationError({'detail': _('You must specify at least one pool prefix in CIDR notation.')})

        return value


class StaffSubnetPoolUpdateSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    prefixes = serializers.JSONField(default=list())
    name = serializers.CharField()

    class Meta:
        model = SubnetPool
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'extra', 'project_id', 'ip_version', 'shared')

    def to_internal_value(self, data):
        """
        Perform any data modification here.
        to_internal_value is called before .validate() and after each field is validated.
        """
        value = super(StaffSubnetPoolUpdateSerializer, self).to_internal_value(data)

        request = self.context.get('request', None)
        assert request, 'Serializer can only be used with http requests.'

        if data['prefixes']:
            for prefix in data['prefixes']:
                try:
                    ipaddress.ip_network(prefix)
                except ValueError:
                    raise ValidationError({'detail': _('Invalid CIDR.')})
        else:
            raise ValidationError({'detail': _('You must specify at least one pool prefix in CIDR notation.')})

        return value
