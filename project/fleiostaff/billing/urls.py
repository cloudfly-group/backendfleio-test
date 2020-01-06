from django.urls import path

from fleiostaff.billing.configurable_options.views import ConfigurableOptionsViewset
from fleiostaff.billing.configurable_options.views import ConfigurableOptionsCyclesViewset
from fleiostaff.billing.configurable_options.views import ConfigurableOptionsChoicesViewset
from fleiostaff.billing.orders.views import StaffOrderViewset
from fleiostaff.billing.productgroups.views import StaffProductGroupViewset
from fleiostaff.billing.products.views import StaffProductViewSet
from fleiostaff.billing.productcycles.views import StaffProductCycleViewSet
from fleiostaff.billing.services.views import StaffServiceViewSet
from fleiostaff.billing.invoicing.views import StaffInvoiceViewSet
from fleiostaff.billing.taxrules.views import StaffTaxRuleViewset
from fleiostaff.billing.transactions.views import StaffTransactionViewSet
from fleiostaff.billing.gateways.views import GatewaysViewset
from fleiostaff.billing.gateways.views import staff_action
from fleiostaff.billing.journal.views import JournalViewset

try:
    from fleio.core.loginview import StaffFeatureRouter
    router = StaffFeatureRouter(trailing_slash=False)
    router.register(r'billing/orders', StaffOrderViewset, basename='orders', feature_name='billing.orders')
    router.register(r'billing/services', StaffServiceViewSet, basename='services', feature_name='billing.services')
    router.register(r'billing/products', StaffProductViewSet, basename='products', feature_name='billing.products')
    router.register(
        r'billing/productcycles',
        StaffProductCycleViewSet,
        basename='productcycles',
        feature_name='billing.products'
    )
    router.register(
        r'billing/productgroups',
        StaffProductGroupViewset,
        basename='productgroups',
        feature_name='billing.products'
    )
    router.register(r'billing/invoices', StaffInvoiceViewSet, basename='invoices', feature_name='billing.invoices')
    router.register(
        r'billing/transactions',
        StaffTransactionViewSet,
        basename='transactions',
        feature_name='billing.transactions')
    router.register(r'billing/gateways', GatewaysViewset, basename='gateways', feature_name='billing.gateways')
    router.register(r'billing/journal', JournalViewset, basename='journal', feature_name='billing.journal')
    router.register(r'billing/taxrules', StaffTaxRuleViewset, basename='taxrules', feature_name='billing.taxrules')

    router.register(r'billing/configoptions/cycles', ConfigurableOptionsCyclesViewset,
                    basename='configurable-options-cycles', feature_name='billing')
    router.register(r'billing/configoptions/choices', ConfigurableOptionsChoicesViewset,
                    basename='configurable-options-values', feature_name='billing')
    router.register(r'billing/configoptions', ConfigurableOptionsViewset,
                    basename='configurable-options', feature_name='billing')

    urlpatterns = router.urls

    urlpatterns.append(path('billing/gateway/<slug:gateway>/<slug:action_name>', staff_action, name='gateway-action'))

except ImportError:
    urlpatterns = []
