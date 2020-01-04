from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from plugins.domains.utils.domain import DomainUtils


def validate_nameserver(value):
    if not DomainUtils.validate_domain_name(domain_name=value):
        raise serializers.ValidationError(_('Not a valid hostname'))


class SaveNameserversSerializer(serializers.Serializer):
    nameserver1 = serializers.CharField(
        max_length=255,
        required=True,
        validators=[validate_nameserver]
    )
    nameserver2 = serializers.CharField(
        max_length=255,
        required=False,
        allow_blank=True,
        validators=[validate_nameserver]
    )
    nameserver3 = serializers.CharField(
        max_length=255,
        required=False,
        allow_blank=True,
        validators=[validate_nameserver]
    )
    nameserver4 = serializers.CharField(
        max_length=255,
        required=False,
        allow_blank=True,
        validators=[validate_nameserver]
    )

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
