from django.contrib import admin

from fleio.reseller.models import ResellerResources

admin.site.register(ResellerResources, admin.ModelAdmin)
