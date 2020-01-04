from fleiostaff.conf.views import ConfigurationsViewset

try:
    from fleio.core.loginview import StaffFeatureRouter
    router = StaffFeatureRouter(trailing_slash=False)
    router.register(r'configurations', ConfigurationsViewset, basename='configurations',
                    feature_name='settings.configurations')
    urlpatterns = router.urls
except ImportError:
    urlpatterns = []
