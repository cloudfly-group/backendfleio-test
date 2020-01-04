from plugins.sms_authenticator.enduser.sms_authenticator.views import views
from plugins.sms_authenticator.common.base_views import SMSAuthenticatorAnonymousBaseViewSet

try:
    from fleio.core.loginview import FeatureRouter
    router = FeatureRouter(trailing_slash=False)
    router.register(r'api', views.SMSAuthenticatorViewSet, basename='sms_authenticator',
                    feature_name='clients&users.second_factor_auth.sms_authenticator')
    router.register(r'anonymous', SMSAuthenticatorAnonymousBaseViewSet, basename='sms_authenticator',
                    feature_name='clients&users.second_factor_auth.sms_authenticator')

    urlpatterns = router.urls
except ImportError:
    urlpatterns = []
