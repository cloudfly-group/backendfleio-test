from django.contrib import admin
from fleio.notifications import models


class NotificationsAdmin(admin.ModelAdmin):
    search_fields = ['client', 'name']
    list_display = ('client', 'name', 'generated', 'priority', 'status', 'is_current', )


class DispatcherLogAdmin(admin.ModelAdmin):
    list_display = ('notification', 'name', 'generated', 'status')


class NotificationTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'title', 'dispatcher')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


class NotificationSettingsAdmin(admin.ModelAdmin):
    list_display = ('name', 'enabled')


class UserNotificationsSettingsAdmin(admin.ModelAdmin):
    list_display = ('user', )


admin.site.register(models.Notification, NotificationsAdmin)
admin.site.register(models.DispatcherLog, DispatcherLogAdmin)
admin.site.register(models.NotificationTemplate, NotificationTemplateAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.NotificationSettings, NotificationSettingsAdmin)
admin.site.register(models.UserNotificationsSettings, UserNotificationsSettingsAdmin)
