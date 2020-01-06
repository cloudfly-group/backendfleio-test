from rest_framework import serializers

from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import ValidationError

from plugins.domains.configuration import DomainsSettings
from plugins.domains.utils.domain import DomainUtils


def validate_nameserver(value):
    if not DomainUtils.validate_domain_name(domain_name=value):
        raise serializers.ValidationError(_('Not a valid hostname'))


class RegisterDomainSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=256)
    use_default_nameservers = serializers.BooleanField(default=True, required=False)
    years = serializers.IntegerField(required=True)
    contact_id = serializers.IntegerField(required=False, default=None, allow_null=True)
    dns_management = serializers.BooleanField(default=False, required=False, allow_null=True)
    email_forwarding = serializers.BooleanField(default=False, required=False, allow_null=True)
    id_protection = serializers.BooleanField(default=False, required=False, allow_null=True)
    operation = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    client = serializers.IntegerField(required=True)

    nameserver1 = serializers.CharField(max_length=256, required=False, validators=[validate_nameserver])
    nameserver2 = serializers.CharField(
        max_length=256,
        required=False,
        allow_blank=True,
        allow_null=True,
        validators=[validate_nameserver],
    )
    nameserver3 = serializers.CharField(
        max_length=256,
        required=False,
        allow_blank=True,
        allow_null=True,
        validators=[validate_nameserver],
    )
    nameserver4 = serializers.CharField(
        max_length=256,
        required=False,
        allow_blank=True,
        allow_null=True,
        validators=[validate_nameserver],
    )

    def validate(self, attrs):
        validated_data = super().validate(attrs=attrs)
        domain_settings = DomainsSettings.for_client(client=self.context['request'].user.clients.first())
        # validate domain name
        if attrs['operation'] == 'register':
            available, error, adjusted_name = DomainUtils.check_if_domains_is_available_for_registration(
                domain_name=attrs['name'],
                domains_settings=domain_settings,
                skip_whois_check=True,
            )

            if not available:
                raise ValidationError({
                    'non_field_errors': error
                })
            else:
                validated_data['name'] = adjusted_name

        if attrs['operation'] == 'transfer':
            available, error, adjusted_name = DomainUtils.check_if_domains_is_available_for_transfer(
                domain_name=attrs['non_field_errors'],
                domains_settings=domain_settings,
                skip_whois_check=True,
            )

            if not available:
                raise ValidationError({
                    'name': error
                })
            else:
                validated_data['name'] = adjusted_name

        return validated_data

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
