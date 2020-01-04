from reseller.billing.invoices.views.invoice import ResellerInvoiceViewSet
from reseller.billing.journal.views.journal import JournalViewset
from reseller.billing.services.views.service import ResellerServiceViewSet
from reseller.billing.transactions.views.transaction import ResellerTransactionViewSet

try:
    from fleio.core.loginview import ResellerFeatureRouter

    router = ResellerFeatureRouter(trailing_slash=False)
    # router.register(r'billing/orders', ResellerOrderViewSet, basename='orders', feature_name='billing.orders')
    router.register(r'billing/services', ResellerServiceViewSet, basename='services', feature_name='billing.services')
    # router.register(r'billing/products', ResellerProductViewSet, basename='products', feature_name='billing.products')
    # router.register(
    #     r'billing/productcycles',
    #     ResellerProductCycleViewSet,
    #     basename='productcycles',
    #     feature_name='billing.products'
    # )
    # router.register(
    #     r'billing/productgroups',
    #     StaffProductGroupViewset,
    #     basename='productgroups',
    #     feature_name='billing.products'
    # )
    router.register(r'billing/invoices', ResellerInvoiceViewSet, basename='invoices', feature_name='billing.invoices')
    router.register(r'billing/journal', JournalViewset, basename='journal', feature_name='billing.journal')
    router.register(
        r'billing/transactions',
        ResellerTransactionViewSet,
        basename='transactions',
        feature_name='billing.transactions'
    )

    # router.register(r'billing/configoptions/cycles', ResellerConfigurableOptionsCyclesViewSet,
    #                 basename='configurable-options-cycles', feature_name='billing')
    # router.register(r'billing/configoptions/choices', ResellerConfigurableOptionsChoicesViewSet,
    #                 basename='configurable-options-values', feature_name='billing')
    # router.register(r'billing/configoptions', ResellerConfigurableOptionsViewSet,
    #                 basename='configurable-options', feature_name='billing')

    urlpatterns = router.urls

except ImportError:
    urlpatterns = []
