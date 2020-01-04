from rest_framework import serializers


class UserCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    password = serializers.CharField(required=False, write_only=True)
    description = serializers.CharField(required=False, allow_null=True, allow_blank=True)


class UserUpdateSerializer(UserCreateSerializer):
    name = serializers.CharField(max_length=100, required=False)
