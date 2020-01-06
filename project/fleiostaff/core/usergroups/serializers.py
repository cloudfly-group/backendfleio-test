from rest_framework import serializers

from fleio.core.models import AppUser, UserGroup
from fleio.core.serializers import UserMinSerializer


class UserGroupSerializer(serializers.ModelSerializer):
    users_count = serializers.SerializerMethodField()

    @staticmethod
    def get_users_count(user_group):
        return AppUser.objects.filter(user_groups=user_group).count()

    class Meta:
        model = UserGroup
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'permissions',)


class UserGroupBriefSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserGroup
        fields = ('id', 'name')
        read_only_field = ('id',)


class UserGroupDetailSerializer(UserGroupSerializer):
    users_count = serializers.SerializerMethodField()
    users = serializers.SerializerMethodField()

    @staticmethod
    def get_users_count(user_group):
        return AppUser.objects.filter(user_groups=user_group).count()

    @staticmethod
    def get_users(user_group):
        qs = AppUser.objects.filter(user_groups=user_group)
        return UserMinSerializer(instance=qs, many=True).data
