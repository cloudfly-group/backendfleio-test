from plugins.google_authenticator.staff.google_authenticator.views import views

try:
    from fleio.core.loginview import StaffFeatureRouter
    router = StaffFeatureRouter(trailing_slash=False)
    router.register(r'api', views.StaffGoogleAuthenticatorViewSet, basename='google_authenticator',
                    feature_name='clients&users.second_factor_auth.google_authenticator')

    urlpatterns = router.urls
except ImportError:
    urlpatterns = []
