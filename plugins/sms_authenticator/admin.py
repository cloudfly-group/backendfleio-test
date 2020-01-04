from django.contrib import admin

from plugins.sms_authenticator.models import SMSAuthenticatorData

admin.site.register(SMSAuthenticatorData, admin.ModelAdmin)
