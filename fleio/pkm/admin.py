from django.contrib import admin

from .models import PublicKey


class PublicKeyAdmin(admin.ModelAdmin):
    pass


admin.site.register(PublicKey, PublicKeyAdmin)
