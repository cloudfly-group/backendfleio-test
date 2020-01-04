from plugins.cpanelserver.staff.frontend.views import FrontendView


try:
    from fleio.core.loginview import StaffFeatureRouter
    router = StaffFeatureRouter(trailing_slash=False)
    router.register(r'frontend', FrontendView, basename='frontend', feature_name='plugins.cpanelserver')

    urlpatterns = router.urls
except ImportError:
    urlpatterns = []
