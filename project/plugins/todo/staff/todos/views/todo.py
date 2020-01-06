from django.db import transaction
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from fleio.core.drf import StaffOnly
from fleio.core.filters import CustomFilter

from fleio.utils.collections import get_new_or_none
from fleio.utils.model import statuses_dict_to_statuses_choices

from plugins.todo.models import TODO
from plugins.todo.models import TODOComment
from plugins.todo.models import TODOStatus
from fleio.core.models import AppUser
from plugins.todo.staff.todos.serializers import TODOSerializer
from plugins.todo.utils import send_view_notification


class TODOView(viewsets.ModelViewSet):
    serializer_class = TODOSerializer
    permission_classes = (StaffOnly, )
    queryset = TODO.objects.all()
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend, CustomFilter, filters.SearchFilter)
    search_fields = (
        'assigned_to__first_name',
        'assigned_to__last_name',
        'created_by__first_name',
        'created_by__last_name',
        'description',
        'status',
        'title',
    )
    ordering_fields = ('assigned_to', 'created_at', 'created_by', 'status', 'title', )
    filter_fields = ('assigned_to', 'created_by', 'status', )

    @action(detail=True, methods=['POST'])
    def add_comment(self, request, pk):
        del pk  # unused
        todo = self.get_object()
        comment_text = request.data.get('comment_text', None)
        close_todo = request.data.get('close_todo', False)

        with transaction.atomic():
            if comment_text or close_todo:
                TODOComment.objects.create(
                    todo=todo,
                    created_by=request.user,
                    comment_text=comment_text,
                    new_status=TODOStatus.done if close_todo and todo.status is not TODOStatus.done else None
                )

            if close_todo and todo.status is not TODOStatus.done:
                todo.status = TODOStatus.done
                todo.save()

        return Response()

    @action(detail=False, methods=['get'])
    def create_options(self, request):
        del request  # unused
        return Response(data={
            'statuses': TODOStatus.status_map,
        })

    @action(detail=False, methods=['get'])
    def get_current_user_todo_count(self, request):
        user = AppUser.objects.get(id=request.user.id)
        params = Q(assigned_to=user) | Q(assigned_to=None)
        todo_count = TODO.objects.filter(params).exclude(status='done').count()
        return Response({'count': todo_count})

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
        send_view_notification(user=self.request.user, todo=serializer.instance, signal_type='created')

    def perform_update(self, serializer):
        prev_todo = serializer.instance  # type: TODO
        new_assignee = get_new_or_none(serializer.validated_data, 'assigned_to', prev_todo.assigned_to)
        new_status = get_new_or_none(serializer.validated_data, 'status', prev_todo.status)
        description_changed = get_new_or_none(
            serializer.validated_data, 'description', prev_todo.description
        ) is not None
        title_changed = get_new_or_none(serializer.validated_data, 'title', prev_todo.title) is not None

        with transaction.atomic():
            if new_assignee or new_status or description_changed or title_changed:
                TODOComment.objects.create(
                    todo=prev_todo,
                    created_by=self.request.user,
                    new_status=new_status,
                    new_assignee=new_assignee,
                    description_changed=description_changed,
                    title_changed=title_changed,
                )

            serializer.save()

        send_view_notification(user=self.request.user, todo=serializer.instance, signal_type='updated')

    def perform_destroy(self, instance):
        super().perform_destroy(instance=instance)
        send_view_notification(user=self.request.user, todo=instance, signal_type='deleted')

    @action(detail=False, methods=['get'])
    def filter_options(self, request):
        return Response({
            'statuses': statuses_dict_to_statuses_choices(dictionary=TODOStatus.status_map.items()),
        })
