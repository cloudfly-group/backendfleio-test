from django.conf.urls import include, url
from . import views

try:
    # TODO: this should be moved to staff
    from fleio.core.loginview import StaffFeatureRouter
    router = StaffFeatureRouter(trailing_slash=False)
    router.register(r'revenue_reports', views.RevenueReportsViewset, basename='revenue_reports',
                    feature_name='billing.reporting')

    urlpatterns = [
        url(r'', include((router.urls, 'fleio.reports'), namespace='default')),
    ]
except ImportError:
    urlpatterns = []
