from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    id = serializers.UUIDField(format='hex', required=False)
    default_project_id = serializers.UUIDField(required=False, format='hex')
    domain_id = serializers.CharField(required=False)
    description = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False, allow_null=True, allow_blank=True)
    enabled = serializers.BooleanField(required=False)
    password_expires_at = serializers.DateTimeField(allow_null=True, required=False)
    project_name = serializers.CharField(required=False, allow_null=True, allow_blank=True)


class UserCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    password = serializers.CharField(required=False, write_only=True)
    description = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    domain = serializers.CharField(required=False)
    default_project = serializers.UUIDField(required=False, format='hex')
    email = serializers.EmailField(required=False, allow_null=True, allow_blank=True)
    enabled = serializers.BooleanField(default=True)

    def validate_default_project(self, obj):
        """Uses the hex format of uuid (without hyphens) to be OpenStack friendly"""
        return obj.hex
