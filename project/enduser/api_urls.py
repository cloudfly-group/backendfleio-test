from django.urls import include, path

from fleio.core import views
from fleio.core.plugins.plugin_definition import PluginConfigTypes
from fleio.core.plugins.plugin_utils import PluginUtils

from fleio.core.terms_of_service.views import tos_preview

urlpatterns = [
    path('', include('fleio.core.urls')),
    path('', include(('fleio.billing.urls', 'fleio.billing'), namespace='billing')),
    path('', include(('fleio.pkm.urls', 'fleio.pkm'), namespace='pkm')),
    path('', include(('fleio.osbackup.urls', 'fleio.osbackup'), namespace='osbackup')),
    path('', include(('fleio.notifications.urls', 'fleio.notifications'), namespace='notifications')),
    path('sfauth/', include(('fleio.core.second_factor_auth.urls', 'fleio.core.second_factor_auth'),
                            namespace='sfatypesmanager')),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('sso', views.sso, name='sso'),
    path('current-user', views.current_user, name='current-user'),
    path('reset-password/', views.password_reset, name='reset-password'),
    path('reset-password/confirm/', views.password_reset_confirm, name='reset-password-confirm'),
    path('confirm-email/', views.confirm_email_after_signup, name='email-sign-up-confirmation'),
    path('resend-confirmation-email/', views.resend_email_confirmation_email_message, name='resend-email-confirmation'),
    path('get-external-billing-url/', views.get_external_billing_url, name='get-external-billing-url'),
    path('terms-of-service', tos_preview, name='terms_of_service_preview'),
]

PluginUtils.append_plugin_urls(
    urlpatterns=urlpatterns,
    config_type=PluginConfigTypes.enduser,
)
