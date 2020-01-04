import ipaddress
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from fleio.openstack.models import Port


class PortSerializer(serializers.ModelSerializer):
    fixed_ips = serializers.JSONField(required=False)

    class Meta:
        model = Port
        exclude = ('sync_version',)


class FixedIPSerializer(serializers.Serializer):
    ip_address = serializers.IPAddressField(required=False)
    subnet_id = serializers.CharField(required=False)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class PortCreateSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    fixed_ips = FixedIPSerializer(many=True)
    region = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    attach_to = serializers.CharField(required=True)
    project = serializers.CharField(allow_blank=True, allow_null=True, required=False)

    class Meta:
        model = Port
        exclude = ('sync_version', )
        read_only_fields = ('created_at', 'updated_at', 'extra', 'project')

    def to_internal_value(self, data):
        """
        Perform any data modification here.
        to_internal_value is called before .validate() and after each field is validated.
        """
        value = super().to_internal_value(data)
        if 'mac_address' in value and not value['mac_address']:
            value.pop('mac_address')
        return value


class PortUpdateSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    fixed_ips = serializers.JSONField(default=list())
    subnet = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    region = serializers.CharField(allow_blank=True, allow_null=True, required=False)

    class Meta:
        model = Port
        exclude = ('sync_version', 'network')
        read_only_fields = ('created_at', 'updated_at', 'extra',)

    def _validate_fixed_ips(self, fixed_ips):
        if fixed_ips:
            for fixed_ip in fixed_ips:
                if 'ip_address' in fixed_ip:
                    try:
                        ipaddress.ip_address(fixed_ip['ip_address'])
                    except ValueError:
                        raise ValidationError({'detail': _('Invalid IP specified')})

        return fixed_ips

    def to_internal_value(self, data):
        """
        Perform any data modification here.
        to_internal_value is called before .validate() and after each field is validated.
        """
        value = super().to_internal_value(data)

        request = self.context.get('request', None)
        assert request, 'Serializer can only be used with http requests.'

        if ('subnet' in value and not value['subnet']) or 'subnet' not in value:
            if ('fixed_ips' in value and not value['fixed_ips']) or 'fixed_ips' not in value:
                raise ValidationError({'detail': _('Either subnet or fixed_ips must be specified')})

        self._validate_fixed_ips(data['fixed_ips'])

        if 'mac_address' in value and not value['mac_address']:
            value.pop('mac_address')

        return value
