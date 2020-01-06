from django.urls import include, path

from .views import StaffNotificationViewset

try:
    from fleio.core.loginview import StaffFeatureRouter
    router = StaffFeatureRouter(trailing_slash=False)
    router.register(r'notifications', StaffNotificationViewset, basename='notifications', feature_name='notifications')

    urlpatterns = [
        path('', include((router.urls, 'fleiostaff.notifications'), namespace='default')),
    ]
except ImportError:
    urlpatterns = []
