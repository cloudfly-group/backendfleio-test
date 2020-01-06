from django.contrib import admin

from plugins.google_authenticator.models import GoogleAuthenticatorData

admin.site.register(GoogleAuthenticatorData, admin.ModelAdmin)
