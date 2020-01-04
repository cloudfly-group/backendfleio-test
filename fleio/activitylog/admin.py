# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.utils.encoding import smart_text

from fleio.activitylog import models


class LogCategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')
    ordering = ('name', )


class LogClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    ordering = ('name', )


class LogAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'user', 'ip', 'get_log_entry', 'parameters')
    ordering = ('-created_at',)

    def get_log_entry(self, obj):
        return smart_text(obj)

    get_log_entry.short_description = 'Log'


admin.site.register(models.LogCategory, LogCategoryAdmin)
admin.site.register(models.LogClass, LogClassAdmin)
admin.site.register(models.Log, LogAdmin)
