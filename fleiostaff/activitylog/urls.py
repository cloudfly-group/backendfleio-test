# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from .views import ActivityLogViewSet

try:
    from fleio.core.loginview import StaffFeatureRouter
    router = StaffFeatureRouter(trailing_slash=False)
    router.register(r'activitylog', ActivityLogViewSet, basename='activitylog', feature_name='utils.activitylog')

    urlpatterns = router.urls

except ImportError:
    urlpatterns = []
