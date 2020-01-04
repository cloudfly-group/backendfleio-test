from .views import TaskLogViewSet

try:
    from fleio.core.loginview import StaffFeatureRouter
    router = StaffFeatureRouter(trailing_slash=False)
    router.register(r'tasklog', TaskLogViewSet, basename='tasklog', feature_name='utils.tasklog')

    urlpatterns = router.urls

except ImportError:
    urlpatterns = []
