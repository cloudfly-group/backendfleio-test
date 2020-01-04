from django.conf.urls import url
from django.urls import include, path

from fleiostaff.core.clientgroups.views import ClientGroupViewSet
from fleiostaff.core.terms_of_service.views import tos_settings_view
from fleiostaff.core.dynamic_ui.view import DynamicUIViewSet
from fleiostaff.core.plugins.views import StaffPluginsViewSet
from fleiostaff.core.second_factor_auth.views import sfa_settings_view
from fleiostaff.core.signup_settings.views import sign_up_settings_view
from .clients.views import StaffClientViewSet
from .frontend_customization.views import FrontendCustomizationView
from .notifications.views import NotificationsCategoriesViewSet, NotificationTemplateViewSet
from .permissions.views import PermissionSetViewSet, PermissionViewSet
from .usergroups.views import UserGroupViewset
from .users.views import UserViewSet
from .views import CurrencyViewSet, StaffUserProfileViewSet

try:
    from fleio.core.loginview import StaffFeatureRouter
    router = StaffFeatureRouter(trailing_slash=False)

    router.register(r'clients', StaffClientViewSet, basename='clients', feature_name='clients&users.clients')
    router.register(
        r'clientgroups',
        ClientGroupViewSet,
        basename='clientgroups',
        feature_name='clients&users.clientgroups'
    )
    router.register(r'currency', CurrencyViewSet, basename='currency', feature_name='core')

    router.register(r'dynamic-ui', DynamicUIViewSet, basename='dynamic-ui', feature_name='core')

    router.register(
        'frontend-customization',
        FrontendCustomizationView,
        basename='frontend-customization',
        feature_name='core'
    )
    router.register(r'notification_templates', NotificationTemplateViewSet, basename='notificationtemplates',
                    feature_name='settings.notifications.templates')
    router.register(r'notifications_categories', NotificationsCategoriesViewSet, basename='notifications_categories',
                    feature_name='settings.notifications.templates')

    router.register(r'permissions', PermissionViewSet, basename='permissions', feature_name='settings.authorization')
    router.register(r'permissionsset', PermissionSetViewSet, basename='permissionsset',
                    feature_name='settings.authorization')

    router.register(r'plugins', StaffPluginsViewSet, basename='plugins', feature_name='core')

    router.register(r'users', UserViewSet, basename='users', feature_name='clients&users.users')
    router.register(r'usergroups', UserGroupViewset, basename='usergroups', feature_name='clients&users.usergroups')
    router.register(r'userprofile', StaffUserProfileViewSet, basename='userprofile',
                    feature_name='clients&users.userprofile')

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
