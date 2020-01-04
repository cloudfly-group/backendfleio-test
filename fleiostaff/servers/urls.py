from fleiostaff.servers.views import StaffServerViewSet
from fleiostaff.servers.views import StaffServerGroupViewSet

try:
    from fleio.core.loginview import StaffFeatureRouter
except ImportError:
    urlpatterns = []
else:
    router = StaffFeatureRouter(trailing_slash=False)
    router.register(r'server', StaffServerViewSet, basename='servers', feature_name='servers')
    router.register(r'servergroup', StaffServerGroupViewSet, basename='servergroups', feature_name='servers')

    urlpatterns = router.urls
