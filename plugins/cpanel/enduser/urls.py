from plugins.cpanel.enduser.frontend.views import UserFrontendView


try:
    from fleio.core.loginview import StaffFeatureRouter
    router = StaffFeatureRouter(trailing_slash=False)
    router.register(r'frontend', UserFrontendView, basename='frontend', feature_name='plugins.cpanel')
    urlpatterns = router.urls
except ImportError:
    urlpatterns = []
