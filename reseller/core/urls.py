from django.conf.urls import url
from django.urls import include
from django.urls import path

from fleiostaff.core.dynamic_ui.view import DynamicUIViewSet
from fleiostaff.core.frontend_customization.views import FrontendCustomizationView
from fleiostaff.core.plugins.views import StaffPluginsViewSet
from fleiostaff.core.second_factor_auth.views import sfa_settings_view
from fleiostaff.core.signup_settings.views import sign_up_settings_view
from fleiostaff.core.terms_of_service.views import tos_settings_view
from fleiostaff.core.views import CurrencyViewSet
from reseller.core.clients.views.client import ResellerClientViewSet
from reseller.core.users.views.user import ResellerUserViewSet
from reseller.core.views import ResellerUserProfileViewSet

try:
    from fleio.core.loginview import ResellerFeatureRouter
    router = ResellerFeatureRouter(trailing_slash=False)

    router.register(r'clients', ResellerClientViewSet, basename='clients', feature_name='clients&users.clients')
    router.register(r'users', ResellerUserViewSet, basename='users', feature_name='clients&users.users')

    # router.register(
    #     r'clientgroups',
    #     ResellerClientGroupViewSet,
    #     basename='clientgroups',
    #     feature_name='clients&users.clientgroups'
    # )
    router.register(r'currency', CurrencyViewSet, basename='currency', feature_name='core')

    router.register(r'dynamic-ui', DynamicUIViewSet, basename='dynamic-ui', feature_name='core')

    router.register(
        'frontend-customization',
        FrontendCustomizationView,
        basename='frontend-customization',
        feature_name='core'
    )

    router.register(r'userprofile', ResellerUserProfileViewSet, basename='userprofile',
                    feature_name='clients&users.userprofile')

    router.register(r'plugins', StaffPluginsViewSet, basename='plugins', feature_name='core')

    # router.register(r'usergroups', UserGroupViewset, basename='usergroups', feature_name='clients&users.usergroups')
    # router.register(r'userprofile', StaffUserProfileViewSet, basename='userprofile',
    #                 feature_name='clients&users.userprofile')

    urlpatterns = router.urls

    urlpatterns.extend([
        path('sfauth/', include(('fleiostaff.core.second_factor_auth.urls', 'fleiostaff.core.second_factor_auth'),
                                namespace='sfatypesmanager')),
        path('settings/', include((
            'fleiostaff.core.terms_of_service.urls', 'fleiostaff.core.terms_of_service'
        ), namespace='termsofservice')),
        path('settings/tos-settings', tos_settings_view, name='terms_of_service_settings'),
        path('settings/sign-up-settings', sign_up_settings_view, name='signup_settings'),
        path('settings/sfa-settings', sfa_settings_view, name='sfa_settings'),
    ])

except ImportError:
    urlpatterns = [
        url(
            r'^plugins/plugins_menu$',
            StaffPluginsViewSet.as_view({'get': 'plugins_menu'}),
            name='plugins-plugins-menu',
        ),
    ]
