from rest_framework import serializers

from fleio.core.models import UserGroup
from reseller.core.users.serializers.reseller_user_serializer import ResellerUserSerializer


class ResellerUserUpdateSerializer(ResellerUserSerializer):
    user_groups = serializers.PrimaryKeyRelatedField(many=True, read_only=False, queryset=UserGroup.objects.all(),
                                                     required=False)

    class Meta(ResellerUserSerializer.Meta):
        extra_kwargs = {'password': {'write_only': True, 'required': False}}

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user
