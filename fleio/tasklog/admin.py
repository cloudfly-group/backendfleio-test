from django.contrib import admin

from fleio.tasklog import models


class TaskRunInline(admin.StackedInline):
    model = models.TaskRun
    readonly_fields = ('retry', 'started_at', 'ended_at', 'traceback')
    ordering = ('retry',)
    can_delete = False

    def has_add_permission(self, request, *args, **kwargs):
        return False


class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'state', 'name', 'parent_task', 'activity_log')
    ordering = ('-created_at', )
    inlines = [
        TaskRunInline,
    ]


admin.site.register(models.Task, TaskAdmin)
admin.site.register(models.TaskRun, admin.ModelAdmin)
