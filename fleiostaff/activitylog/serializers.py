from django.utils.encoding import smart_text
from rest_framework import serializers

from fleio.activitylog.models import Log
from fleio.core.serializers import UserMinSerializer


class ActivityLogSerializer(serializers.ModelSerializer):
    log = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    user = UserMinSerializer()
    tasks_count = serializers.SerializerMethodField()

    class Meta:
        model = Log
        fields = ('id', 'created_at', 'user', 'ip', 'type', 'parameters', 'log', 'tasks_count')
        read_only_fields = ('id', 'created_at', 'tasks_count')

    @staticmethod
    def get_tasks_count(instance: Log) -> bool:
        return instance.tasks.count()

    @staticmethod
    def get_log(instance):
        return smart_text(instance)

    @staticmethod
    def get_type(instance):
        return instance.log_class.type
