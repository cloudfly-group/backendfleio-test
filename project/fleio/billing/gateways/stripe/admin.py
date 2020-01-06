from django.contrib import admin

from .models import RecurringPayments

admin.site.register(RecurringPayments, admin.ModelAdmin)
