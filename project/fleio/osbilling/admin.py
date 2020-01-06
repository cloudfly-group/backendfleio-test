from django.contrib import admin
from fleio.osbilling import models


class ResourcePriceAdmin(admin.ModelAdmin):
    list_display = ('pricing_plan', 'price', 'unit', 'resource_type', 'sub_type', 'region')


class TrafficPriceAdmin(admin.ModelAdmin):
    list_display = ('pricing_plan', 'instance_flavor', 'included_traffic_mb', 'exceed_traffic_price', 'region')


class ServiceDynamicUsageAdmin(admin.ModelAdmin):
    search_fields = ('service__client__first_name', 'service__client__last_name')
    list_display = ('active_service', 'plan', 'start_date', 'end_date', 'price')


class ServiceDynamicUsageHistoryAdmin(admin.ModelAdmin):
    search_fields = ('service_dynamic_usage__service__client__first_name',
                     'service_dynamic_usage__service__client__last_name')
    list_display = ('__str__', 'price', 'start_date', 'end_date')


class ResourceUsageLogAdmin(admin.ModelAdmin):
    search_fields = ('resource_uuid', 'project_id',)
    list_display = ('resource_type', 'resource_uuid', 'project_id', 'start', 'end')


class BillingResourceAdmin(admin.ModelAdmin):
    search_fields = ('display_name', 'type', 'name')
    list_display = ('display_name', 'type', 'name')


admin.site.register(models.ServiceDynamicUsage, ServiceDynamicUsageAdmin)
admin.site.register(models.ServiceDynamicUsageHistory, ServiceDynamicUsageHistoryAdmin)
admin.site.register(models.PricingPlan)
admin.site.register(models.BillingResource, BillingResourceAdmin)
admin.site.register(models.PricingRule, admin.ModelAdmin)
admin.site.register(models.PricingRuleCondition, admin.ModelAdmin)
admin.site.register(models.PricingRuleModifier, admin.ModelAdmin)
admin.site.register(models.ResourceUsageLog, ResourceUsageLogAdmin)
