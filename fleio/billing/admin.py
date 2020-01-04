from django.contrib import admin

from fleio.billing.models import FleioCart
from fleio.billing.models import OrderItemConfigurableOption
from fleio.billing.models import InvoiceItemConfigurableOption
from fleio.billing.models import ConfigurableOptionChoice
from fleio.billing.models import ConfigurableOptionCycle
from fleio.billing.models import ConfigurableOption
from fleio.billing.models import OrderItem
from fleio.billing.models import Product
from fleio.billing.models import ProductGroup
from fleio.billing.models import ProductCycle
from fleio.billing.models import ProductModule
from fleio.billing.models import Gateway
from fleio.billing.models import GatewayLog
from fleio.billing.models import Order
from fleio.billing.models import CancellationRequest
from fleio.billing.models import Service
from fleio.billing.models import Journal
from fleio.billing.models import Invoice
from fleio.billing.models import InvoiceItem
from fleio.billing.models import InvoiceItemTax
from fleio.billing.models import Transaction
from fleio.billing.models import ClientCredit
from fleio.billing.models import TaxRule
from fleio.billing.models import ServiceConfigurableOption
from fleio.billing.models import RecurringPaymentsOrder


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'date_initiated', 'gateway', 'amount', 'currency', 'fee')


class ProductCycleInline(admin.TabularInline):
    model = ProductCycle


class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('id', )
    list_display = ('name', 'description', 'status', 'code', 'group', 'module',
                    'price_model', 'taxable', 'has_quantity', 'available_quantity')
    inlines = [ProductCycleInline]


class ProductGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')


class ProductCycleAdmin(admin.ModelAdmin):
    list_display = ('product', 'status', 'cycle', 'cycle_multiplier', 'fixed_price', 'currency',
                    'setup_fee_entire_quantity', 'is_relative_price')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_date', 'status', 'user', 'client')


class ServiceConfigOptionsInline(admin.TabularInline):
    model = ServiceConfigurableOption
    extra = 0


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'product', 'client', 'status', 'override_price', 'created_at', 'updated_at',
                    'next_due_date', 'next_invoice_date', 'override_suspend_until', 'suspend_reason')
    inlines = (ServiceConfigOptionsInline, )


class JournalAdmin(admin.ModelAdmin):
    list_display = ('client_credit', 'invoice', 'transaction', 'source', 'destination',
                    'source_amount', 'destination_amount', 'source_currency', 'destination_currency',
                    'is_refund', 'exchange_rate', 'partial')


class GatewayLogAdmin(admin.ModelAdmin):
    list_display = ('gateway', 'external_id', 'status')


class InvoiceItemsInline(admin.TabularInline):
    model = InvoiceItem


class InvoiceAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'first_name', 'last_name', 'company', 'address1', 'address2', 'city', 'country',
                       'state', 'zip_code', 'phone', 'fax', 'email')
    list_display = ('id', 'client', 'status', 'total', 'balance', 'currency', 'issue_date', 'due_date', 'processed_at')
    inlines = (InvoiceItemsInline, )


class ClientCreditAdmin(admin.ModelAdmin):
    search_fields = ('client__first_name', 'client__last_name')
    list_display = ('client', 'amount', 'currency')


class ConfigurableOptionCycleInlineAdmin(admin.TabularInline):
    model = ConfigurableOptionCycle


class ConfigurableOptionChoiceInlineAdmin(admin.TabularInline):
    model = ConfigurableOptionChoice


class ConfigurableOptionAdmin(admin.ModelAdmin):
    search_fields = ('name', )
    list_display = ('name', )

    inlines = (ConfigurableOptionChoiceInlineAdmin,)


class ConfigurableOptionChoiceAdmin(admin.ModelAdmin):
    list_display = ('option', 'choice')
    inlines = (ConfigurableOptionCycleInlineAdmin,)


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'order', 'item_type', 'quantity', 'cycle_display')


class OrderItemConfigurableOptionAdmin(admin.ModelAdmin):
    list_display = ('option', 'option_value', 'quantity', 'price', 'setup_fee', 'order_item')


class InvoiceItemConfigurableOptionAdmin(admin.ModelAdmin):
    list_display = ('option', 'option_value', 'quantity', 'price', 'setup_fee', 'invoice_item')


class InvoiceItemConfigurableOptionInline(admin.TabularInline):
    model = InvoiceItemConfigurableOption


class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'item_type', 'service', 'amount', 'taxed', 'description')
    inlines = (InvoiceItemConfigurableOptionInline,)


class FleioCartAdmin(admin.ModelAdmin):
    list_display = ('client', 'user', 'currency', 'created_at')


class RecurringPaymentsOrderAdmin(admin.ModelAdmin):
    list_display = ('client', 'gateway_name', 'order')


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductGroup, ProductGroupAdmin)
admin.site.register(ProductCycle, ProductCycleAdmin)
admin.site.register(ProductModule)
admin.site.register(Gateway)
admin.site.register(GatewayLog, GatewayLogAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(CancellationRequest)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Journal, JournalAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(InvoiceItem, InvoiceItemAdmin)
admin.site.register(InvoiceItemTax)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(ClientCredit, ClientCreditAdmin)
admin.site.register(TaxRule)
admin.site.register(FleioCart, FleioCartAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(ConfigurableOption, ConfigurableOptionAdmin)
admin.site.register(ConfigurableOptionCycle)
admin.site.register(ConfigurableOptionChoice, ConfigurableOptionChoiceAdmin)
admin.site.register(OrderItemConfigurableOption, OrderItemConfigurableOptionAdmin)
admin.site.register(InvoiceItemConfigurableOption, InvoiceItemConfigurableOptionAdmin)
admin.site.register(RecurringPaymentsOrder, RecurringPaymentsOrderAdmin)
