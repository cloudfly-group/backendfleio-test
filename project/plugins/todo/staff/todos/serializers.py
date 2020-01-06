from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from plugins.todo.models import TODO
from plugins.todo.models import TODOComment
from plugins.todo.models import TODOStatus


class TODOCommentSerializer(serializers.ModelSerializer):
    new_assignee_display = serializers.SerializerMethodField(required=False, read_only=True)
    created_by_display = serializers.SerializerMethodField(required=False, read_only=True)
    new_status_display = serializers.SerializerMethodField(required=False, read_only=True)
    new_status = serializers.CharField(required=False, read_only=True, allow_null=True, allow_blank=True)

    class Meta:
        model = TODOComment
        fields = (
            'created_at',
            'created_by',
            'created_by_display',
            'comment_text',
            'new_assignee',
            'new_assignee_display',
            'new_status',
            'new_status_display',
            'description_changed',
            'title_changed'
        )

    @staticmethod
    def get_new_assignee_display(model: TODOComment):
        return model.new_assignee.get_full_name() if model.new_assignee else _('N/A')

    @staticmethod
    def get_created_by_display(model: TODOComment):
        return model.created_by.get_full_name() if model.created_by else _('N/A')

    @staticmethod
    def get_new_status_display(model: TODOComment):
        return TODOStatus.status_map.get(model.new_status, _('N/A'))


class TODOSerializer(serializers.ModelSerializer):
    comments = TODOCommentSerializer(many=True, required=False, read_only=True)
    assigned_to_display = serializers.SerializerMethodField(required=False, read_only=True)
    status_display = serializers.SerializerMethodField(required=False, read_only=True)
    created_by_display = serializers.SerializerMethodField(required=False, read_only=True)
    description = serializers.CharField(max_length=10240, allow_null=True, allow_blank=True, required=False)

    class Meta:
        model = TODO
        fields = (
            'id',
            'created_at',
            'created_by',
            'created_by_display',
            'assigned_to',
            'assigned_to_display',
            'title',
            'description',
            'status',
            'status_display',
            'comments',
        )

    @staticmethod
    def validate_status(status):
        if not status:
            return status
        if not TODOStatus.status_map.get(status, None):
            raise ValidationError(_('Invalid status.'))
        return status

    @staticmethod
    def get_status_display(model: TODO):
        return TODOStatus.status_map.get(model.status, _('N/A'))

    @staticmethod
    def get_assigned_to_display(model: TODO):
        return model.assigned_to.get_full_name() if model.assigned_to else _('N/A')

    @staticmethod
    def get_created_by_display(model: TODO):
        return model.created_by.get_full_name() if model.created_by else _('N/A')
