from django.conf.urls import include, url

from . import views

try:
    from fleio.core.loginview import StaffFeatureRouter
    router = StaffFeatureRouter(trailing_slash=False)
    router.register(r'tos', views.TermsOfServiceViewSet, basename='termsofservice',
                    feature_name='core')

    urlpatterns = [
        url(r'', include((router.urls, 'fleiostaff.core.terms_of_service'), namespace='default'))
    ]
except ImportError:
    urlpatterns = []
