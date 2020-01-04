from django.conf.urls import include, url

from . import views

try:
    from fleio.core.loginview import StaffFeatureRouter
    router = StaffFeatureRouter(trailing_slash=False)
    router.register(r'osbackup', views.StaffBackupSchedulesViewSet, basename='osbackup',
                    feature_name='openstack.osbackup.schedules')

    urlpatterns = [
        url(r'', include((router.urls, 'fleiostaff.osbackup'), namespace='default')),
    ]
except ImportError:
    urlpatterns = []
