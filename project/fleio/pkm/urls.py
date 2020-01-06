from django.conf.urls import include, url

from . import views

try:
    from fleio.core.loginview import FeatureRouter
    router = FeatureRouter(trailing_slash=False)
    router.register(r'pkm', views.PublicKeyViewSet, basename='publickeys', feature_name='openstack.sshkeys')

    urlpatterns = [
        url(r'', include((router.urls, 'fleio.pkm'), namespace='default'))
    ]
except ImportError:
    urlpatterns = []
