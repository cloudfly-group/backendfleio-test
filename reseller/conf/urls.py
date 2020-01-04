from reseller.conf.views import ConfigurationsViewset

try:
    from fleio.core.loginview import ResellerFeatureRouter
    router = ResellerFeatureRouter(trailing_slash=False)
    router.register(r'configurations', ConfigurationsViewset, basename='configurations',
                    feature_name='settings.configurations')
    urlpatterns = router.urls
except ImportError:
    urlpatterns = []
