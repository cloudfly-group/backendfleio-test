from django.conf.urls import include, url

from . import views

try:
    from fleio.core.loginview import StaffFeatureRouter
    router = StaffFeatureRouter(trailing_slash=False)
    router.register(r'sfa-types-manager', views.SecondFactorAuthTypeViewSet, basename='sfatypesmanager',
                    feature_name='clients&users.second_factor_auth')

    urlpatterns = [
        url(r'', include((router.urls, 'fleiostaff.core.second_factor_auth'), namespace='default'))
    ]
except ImportError:
    urlpatterns = []
