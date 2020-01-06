import logging
import string

from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.fields import CreateOnlyDefault
from rest_framework.validators import UniqueTogetherValidator

from fleio.core.serializers import UserMinSerializer
from fleio.pkm.models import PublicKey
from fleio.pkm.utils import get_fingerprint
from fleio.pkm.utils import is_valid_ssh_public_key

LOG = logging.getLogger(__name__)


class ResellerPublicKeySerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True, default=CreateOnlyDefault(timezone.now))
    user = UserMinSerializer(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = PublicKey
        fields = ('id', 'name', 'public_key', 'created_at', 'fingerprint', 'user')
        read_only_fields = ('id', 'fingerprint', 'user',)
        validators = [UniqueTogetherValidator(queryset=PublicKey.objects.all(),
                                              fields=('name', 'user'),
                                              message=_('A key already exists with the same name'))]

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        data['fingerprint'] = get_fingerprint(data['public_key'])
        return data

    @staticmethod
    def validate_public_key(value):
        if not is_valid_ssh_public_key(value):
            raise serializers.ValidationError(_('Invalid SSH public key'))
        return value

    @staticmethod
    def validate_name(value):
        # NOTE(tomo): OpenStack only allows "_- " digits and numbers
        safechars = "_- " + string.digits + string.ascii_letters
        clean_value = "".join(x for x in value if x in safechars)
        if clean_value != value:
            raise serializers.ValidationError(_("Name contains unsafe characters"))
        return value
