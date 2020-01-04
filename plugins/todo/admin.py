from django import forms
from django.contrib import admin

from plugins.todo.models import TODO
from plugins.todo.models import TODOComment
from plugins.todo.models import TODOProductSettings


class TODOForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = TODO
        fields = '__all__'


class TODOAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'created_at')
    ordering = ('-created_at', )
    form = TODOForm


class TODOCommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'created_at')
    ordering = ('-created_at', )


admin.site.register(TODO, TODOAdmin)
admin.site.register(TODOComment, TODOCommentAdmin)
admin.site.register(TODOProductSettings, admin.ModelAdmin)
