from django.utils.translation import ugettext_lazy as _

from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from fleio.core.clients.serializers import ClientMinSerializer
from fleio.reseller.utils import user_reseller_resources
from fleiostaff.core.usergroups.serializers import UserGroupBriefSerializer


class ResellerUserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    clients = ClientMinSerializer(many=True, required=False, read_only=True)
    user_groups = UserGroupBriefSerializer(many=True, required=False)

    class Meta:
        model = get_user_model()
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'last_login', 'is_active',
            'clients', 'external_billing_id', 'full_name', 'password',
            'permissions', 'user_groups', 'language', 'email_verified'
        )
        read_only_fields = ('id', 'date_joined', 'last_login', 'full_name', 'permissions')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        validated_data = super().validate(attrs)

        request = self.context.get('request', None)
        if not request:
            raise ValidationError({'detail': _('Internal error when creating user.')})
        else:
            # user created by reseller should be assigned to creating reseller
            validated_data['reseller_resources'] = user_reseller_resources(user=request.user)
            validated_data['is_reseller'] = False

        validated_data['is_staff'] = False
        validated_data['is_superuser'] = False

        return validated_data

    def create(self, validated_data):
        # user is not associated in any group by default
        if 'user_groups' in validated_data:
            validated_data.pop('user_groups', None)
        if 'language' not in validated_data:
            validated_data['language'] = getattr(settings, 'DEFAULT_USER_LANGUAGE', 'en')

        return self.Meta.model.objects.create_user(**validated_data)
