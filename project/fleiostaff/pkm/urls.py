from django.conf.urls import include, url

from . import views

try:
    from fleio.core.loginview import StaffFeatureRouter
    router = StaffFeatureRouter(trailing_slash=False)
    router.register(r'pkm', views.StaffPublicKeyViewSet, basename='publickeys', feature_name='openstack.sshkeys')

    urlpatterns = [
        url(r'', include((router.urls, 'fleiostaff.pkm'), namespace='default')),
    ]
except ImportError:
    urlpatterns = []
