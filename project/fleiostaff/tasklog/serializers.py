from typing import Optional

from rest_framework import serializers

from fleio.tasklog.models import Task
from fleio.tasklog.models import TaskState


class TaskSerializer(serializers.ModelSerializer):
    description = serializers.SerializerMethodField()
    state = serializers.SerializerMethodField()
    has_subtasks = serializers.SerializerMethodField()
    parent_id = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ('id', 'parent_id', 'name', 'args', 'kwargs', 'user', 'state', 'created_at', 'resource_id',
                  'resource_type', 'description', 'has_subtasks')
        read_only_fields = ('id', 'parent_id', 'has_subtasks')

    @staticmethod
    def get_parent_id(instance: Task) -> Optional[str]:
        try:
            return instance.parent_task.id
        except AttributeError:
            return None

    @staticmethod
    def get_has_subtasks(instance: Task):
        return instance.children.count() > 0

    @staticmethod
    def get_description(obj):
        return obj.name

    @staticmethod
    def get_state(obj):
        return TaskState.states_map.get(obj.state, None)
