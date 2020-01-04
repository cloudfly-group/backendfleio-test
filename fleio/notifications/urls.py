from django.urls import include, path

from .views import NotificationViewset

try:
    from fleio.core.loginview import FeatureRouter
    router = FeatureRouter(trailing_slash=False)
    router.register(r'notifications', NotificationViewset, basename='notifications', feature_name='notifications')

    urlpatterns = [
        path('', include((router.urls, 'fleio.notifications'), namespace='default')),
    ]
except ImportError:
    urlpatterns = []
