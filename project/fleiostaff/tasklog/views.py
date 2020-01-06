from typing import List

from django.utils.translation import ugettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response

from .serializers import TaskSerializer

from fleio.celery import app as celery_app
from fleio.core.drf import StaffOnly
from fleio.core.filters import CustomFilter
from fleio.tasklog.models import Task


class TaskLogViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = (StaffOnly,)
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend, filters.SearchFilter, CustomFilter)
    search_fields = ('name', 'args', 'kwargs', 'id')
    ordering_fields = ('name', 'created_at', 'user', 'client', 'state')

    def get_queryset(self):
        return Task.objects.all()

    @action(detail=True, methods=['post'])
    def recreate(self, request, pk):
        del request  # unused
        task = get_object_or_404(queryset=self.get_queryset(), pk=pk)
        # send_task always executes tasks async
        celery_app.send_task(task.name, task.args, task.kwargs)
        return Response({'detail': _('Task recreated')})

    @action(detail=False, methods=['get'])
    def get_tasks_for_activity(self, request: Request):
        def tree_to_list(task_tree, depth: int) -> List:
            task_list = []
            for task in task_tree:
                task['depth'] = depth
                task_list.append(task)
                if task['has_subtasks']:
                    task_list = task_list + tree_to_list(task['subtasks'], depth + 1)

            return task_list

        activity_id = request.query_params.get('activity_id', None)

        queryset = Task.objects.filter(activity_log__id=activity_id)
        serializer = TaskSerializer(queryset, many=True)
        tasks = serializer.data
        tasks_dict = {task['id']: task for task in tasks}
        top_level_tasks = []

        for task in tasks:
            parent_id = task.get('parent_id', None)
            if parent_id:
                parent_task = tasks_dict[parent_id]
                if parent_task.get('subtasks'):
                    parent_task['subtasks'].append(task)
                else:
                    parent_task['subtasks'] = [task]
            else:
                top_level_tasks.append(task)

        sorted_tasks = tree_to_list(top_level_tasks, 1)

        return Response({
            'objects': {index: sorted_tasks[index] for index in range(0, len(sorted_tasks))}
        })

    @action(detail=True, methods=['GET'])
    def get_task_log(self, request, pk):
        del pk, request  # unused
        task = self.get_object()  # type: Task
        task_log = task.get_log()
        return Response({
            'task_log': task_log
        })
