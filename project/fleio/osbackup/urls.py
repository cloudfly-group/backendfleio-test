from django.conf.urls import include, url
from .views import BackupSchedulesViewSet

try:
    from fleio.core.loginview import FeatureRouter
    router = FeatureRouter(trailing_slash=False)
    router.register(r'osbackup', BackupSchedulesViewSet, basename='osbackup',
                    feature_name='openstack.osbackup.schedules')

    urlpatterns = [
        url(r'', include((router.urls, 'fleio.osbackup'), namespace='default'))
    ]
except ImportError:
    urlpatterns = []
