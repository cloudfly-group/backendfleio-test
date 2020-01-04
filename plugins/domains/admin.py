from django.contrib import admin

from plugins.domains.models import Contact
from plugins.domains.models import Domain
from plugins.domains.models import Nameserver
from plugins.domains.models import Registrar
from plugins.domains.models import RegistrarConnector
from plugins.domains.models import TLD
from plugins.domains.models import RegistrarPrices


class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'id', 'email', )


class DomainAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'id', )


class NameserverAdmin(admin.ModelAdmin):
    list_display = ('host_name', 'id',)


class RegistrarAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', )


class RegistrarConnectorAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', )


class TLDAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', )


class RegistrarPricesAdmin(admin.ModelAdmin):
    list_display = ('tld_name', 'connector', 'register_price', 'transfer_price', 'renew_price', 'promo_price',
                    'currency')


admin.site.register(Contact, ContactAdmin)
admin.site.register(Domain, DomainAdmin)
admin.site.register(Nameserver, NameserverAdmin)
admin.site.register(Registrar, RegistrarAdmin)
admin.site.register(RegistrarConnector, RegistrarConnectorAdmin)
admin.site.register(TLD, TLDAdmin)
admin.site.register(RegistrarPrices, RegistrarPricesAdmin)
