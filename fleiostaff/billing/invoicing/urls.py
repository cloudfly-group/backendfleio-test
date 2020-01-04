from .views import StaffInvoiceViewSet

try:
    from fleio.core.loginview import StaffFeatureRouter
    router = StaffFeatureRouter(trailing_slash=False)
    router.register(r'invoices', StaffInvoiceViewSet, basename='invoices')

    urlpatterns = router.urls
except ImportError:
    urlpatterns = []
