from django import forms
from django.contrib import admin

from plugins.tickets.models import EmailMessage
from plugins.tickets.models import Attachment
from plugins.tickets.models import Ticket
from plugins.tickets.models.ticket_update import TicketUpdate
from plugins.tickets.models import TicketNote
from plugins.tickets.models.tickets_user_settings import TicketsUserSettings
from plugins.tickets.models.department import Department
from plugins.tickets.models.ticket import TicketLink


class TicketAdmin(admin.ModelAdmin):
    pass


class TicketUpdateAdmin(admin.ModelAdmin):
    pass


class TicketNoteAdmin(admin.ModelAdmin):
    pass


class EmailMessageForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = EmailMessage
        fields = '__all__'


class EmailMessageAdmin(admin.ModelAdmin):
    list_display = ('pk', 'sender_address', 'subject')
    form = EmailMessageForm


class DepartmentAdmin(admin.ModelAdmin):
    pass


admin.site.register(Attachment, admin.ModelAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(EmailMessage, EmailMessageAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(TicketNote, TicketNoteAdmin)
admin.site.register(TicketsUserSettings)
admin.site.register(TicketUpdate, TicketUpdateAdmin)
admin.site.register(TicketLink, admin.ModelAdmin)
