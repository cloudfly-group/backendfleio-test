from plugins.google_authenticator.enduser.google_authenticator.views import views

try:
    from fleio.core.loginview import FeatureRouter
    router = FeatureRouter(trailing_slash=False)
    router.register(r'api', views.GoogleAuthenticatorViewSet, basename='google_authenticator',
                    feature_name='clients&users.second_factor_auth.google_authenticator')

    urlpatterns = router.urls
except ImportError:
    urlpatterns = []
