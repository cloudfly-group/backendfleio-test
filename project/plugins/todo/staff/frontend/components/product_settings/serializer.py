from rest_framework import serializers

from plugins.todo.models import TODOProductSettings


class TODOProductSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TODOProductSettings
        fields = '__all__'
