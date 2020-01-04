from django.contrib import admin

from .models import (OpenStackBackupLog, OpenStackBackupSchedule, )


class OpenStackBackupScheduleAdmin(admin.ModelAdmin):
    pass


admin.site.register(OpenStackBackupSchedule, OpenStackBackupScheduleAdmin)


class OpenStackBackupLogAdmin(admin.ModelAdmin):
    pass


admin.site.register(OpenStackBackupLog, OpenStackBackupLogAdmin)
