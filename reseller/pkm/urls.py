from django.conf.urls import include, url

from reseller.pkm.views.public_key import ResellerPublicKeyViewSet

try:
    from fleio.core.loginview import ResellerFeatureRouter
    router = ResellerFeatureRouter(trailing_slash=False)
    router.register(r'pkm', ResellerPublicKeyViewSet, basename='publickeys', feature_name='openstack.sshkeys')

    urlpatterns = [
        url(r'', include((router.urls, 'reseller.pkm'), namespace='default')),
    ]
except ImportError:
    urlpatterns = []
