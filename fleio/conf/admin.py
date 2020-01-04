from django.contrib import admin

from fleio.conf import models


class ConfigurationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'is_default')


class OptionAdmin(admin.ModelAdmin):
    search_fields = ['section', 'field', 'value']
    list_display = ('configuration', 'section', 'field', 'value')
    list_filter = ('configuration', 'section')
    readonly_fields = ('section', 'field', 'configuration')


admin.site.register(models.Configuration, ConfigurationAdmin)
admin.site.register(models.Option, OptionAdmin)
