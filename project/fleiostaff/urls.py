from django.conf.urls import include, url

from fleio.core.plugins.plugin_definition import PluginConfigTypes
from fleio.core.plugins.plugin_utils import PluginUtils
from fleio.core.views import password_reset, password_reset_confirm
from fleiostaff.core import views

urlpatterns = [
    url(r'', include(('fleiostaff.core.urls', 'fleiostaff.core'), namespace='core')),
    url(r'', include(('fleiostaff.notifications.urls', 'fleiostaff.notifications'), namespace='notifications')),
    url(r'', include(('fleiostaff.pkm.urls', 'fleiostaff.pkm'), namespace='pkm')),
    url(r'', include(('fleiostaff.osbackup.urls', 'fleiostaff.osbackup'), namespace='staff.osbackup')),
    url(r'', include(('fleiostaff.billing.urls', 'fleiostaff.billing'), namespace='billing')),
    url(r'', include(('fleiostaff.conf.urls', 'fleiostaff.conf'), namespace='conf')),
    url(r'', include(('fleiostaff.tasklog.urls', 'fleiostaff.tasklog'), namespace='tasklog')),
    url(r'', include(('fleiostaff.activitylog.urls', 'fleiostaff.activitylog'), namespace='activitylog')),
    url(r'', include(('fleiostaff.servers.urls', 'fleiostaff.servers'), namespace='server')),
    url(r'', include(('fleio.osbackup.urls', 'fleio.osbackup'), namespace='osbackup')),
    url(r'^get-sso-session$', views.get_sso_session, name='get-sso-session'),
    url(r'^set-license$', views.set_license, name='set-license'),
    url(r'^refresh-license$', views.refresh_license, name='refresh-license'),
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^current-user$', views.current_user, name='current-user'),
    url(r'^services-statuses$', views.get_services_statuses, name='services-statuses'),
    url(r'^app-status', views.get_app_status, name='app-status'),
    url(r'^get-license-info$', views.get_license_info, name='get-license-info'),
    url(r'^reset-password/$', password_reset, name='reset-password'),
    url(r'^reset-password/confirm/$', password_reset_confirm, name='reset-password-confirm'),
    url('', include(('fleio.reports.urls', 'fleio.reports'), namespace='reports'))
]

PluginUtils.append_plugin_urls(
    urlpatterns=urlpatterns,
    config_type=PluginConfigTypes.staff
)
