from django.conf.urls import include
from django.conf.urls import url

# from fleio.core.plugins.plugin_definition import PluginConfigTypes
# from fleio.core.plugins.plugin_utils import PluginUtils
from fleio.core.views import password_reset
from fleio.core.views import password_reset_confirm
from reseller.core.auth import views

urlpatterns = [
    url(r'', include(('reseller.core.urls', 'reseller.core'), namespace='core')),
    url(r'', include(('reseller.billing.urls', 'reseller.billing'), namespace='billing')),
    url(r'', include(('reseller.conf.urls', 'reseller.conf'), namespace='conf')),
    url(r'', include(('reseller.openstack.urls', 'reseller.openstack'), namespace='openstack')),
    url(r'', include(('reseller.pkm.urls', 'reseller.pkm'), namespace='pkm')),

    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^current-user$', views.current_user, name='current-user'),
    url(r'^reset-password/$', password_reset, name='reset-password'),
    url(r'^reset-password/confirm/$', password_reset_confirm, name='reset-password-confirm'),
]

# TODO: make this work for reseller
# PluginUtils.append_plugin_urls(
#     urlpatterns=urlpatterns,
#     config_type=PluginConfigTypes.staff
# )
