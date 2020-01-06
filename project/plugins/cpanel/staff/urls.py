from plugins.cpanel.staff.frontend.views import FrontendView
from plugins.cpanel.staff.licenses.views import CPanelLicenseViews


try:
    from fleio.core.loginview import StaffFeatureRouter
    router = StaffFeatureRouter(trailing_slash=False)
    router.register(r'frontend', FrontendView, basename='frontend', feature_name='plugins.cpanel')

    router.register(r'cpanel', CPanelLicenseViews, basename='cpanel', feature_name='plugins.cpanel')

    urlpatterns = router.urls
except ImportError:
    urlpatterns = []
