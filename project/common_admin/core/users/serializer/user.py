from rest_framework import serializers
from fleio.core.models import AppUser


class AdminUserMinSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = AppUser
        fields = ('id', 'full_name', 'email')
