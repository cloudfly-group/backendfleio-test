from django.contrib import admin

from fleio.servers.models import Server
from fleio.servers.models import ServerGroup


class ServerAdmin(admin.ModelAdmin):
    readonly_fields = ('id', )


admin.site.register(ServerGroup)
admin.site.register(Server, ServerAdmin)
