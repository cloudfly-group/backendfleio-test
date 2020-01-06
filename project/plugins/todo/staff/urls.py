from plugins.todo.staff.frontend.views import FrontendView
from plugins.todo.staff.todos.views.todo import TODOView


try:
    from fleio.core.loginview import StaffFeatureRouter
    router = StaffFeatureRouter(trailing_slash=False)
    router.register(r'frontend', FrontendView, basename='frontend', feature_name='plugins.todo')

    router.register(r'todo', TODOView, basename='todo', feature_name='plugins.todo')

    urlpatterns = router.urls
except ImportError:
    urlpatterns = []
