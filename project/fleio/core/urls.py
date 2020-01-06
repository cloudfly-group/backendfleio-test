from django.conf.urls import url

from fleio.core.dynamic_ui.view import DynamicUIViewSet
from .views import UserProfileViewSet
from .signup.views import SignUpViewSet
from fleio.core.clients.views import ClientViewSet
from fleio.core.terms_of_service.views import TermsOfServiceAgreementsViewSet

from fleio.core.plugins.views import EnduserPluginsViewSet

try:
    from fleio.core.loginview import FeatureRouter
    router = FeatureRouter(trailing_slash=False)
    router.register(r'clients', ClientViewSet, basename='client', feature_name='clients&users.clients')
    router.register(r'dynamic-ui', DynamicUIViewSet, basename='dynamic-ui', feature_name='core')
    router.register(r'plugins', EnduserPluginsViewSet, basename='plugins', feature_name='core')
    router.register(r'signup', SignUpViewSet, basename='signup', feature_name='clients&users.signup')
    router.register(
        r'userprofile',
        UserProfileViewSet,
        basename='userprofile',
        feature_name='clients&users.userprofile'
    )
    router.register(r'tos-agreements', TermsOfServiceAgreementsViewSet, basename='termsofserviceagreements',
                    feature_name='core')

    urlpatterns = router.urls
except ImportError:
    urlpatterns = [
        url(
            r'^plugins/plugins_menu$',
            EnduserPluginsViewSet.as_view({'get': 'plugins_menu'}),
            name='plugins-plugins-menu',
        ),
    ]
