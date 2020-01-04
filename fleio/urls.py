import sys

from django.urls import path
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.conf.urls import include, url
from fleio.billing.modules.factory import module_factory
from fleio.core.features import staff_active_features

from fleio.core.plugins.plugin_loader import plugin_loader

from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.admin.sites import AdminSite
from django.contrib.admin.forms import AdminAuthenticationForm
from django.shortcuts import render

from rest_framework import permissions, throttling
from rest_framework.decorators import api_view, permission_classes, throttle_classes

from fleio.core.second_factor_auth.utils import update_second_factor_auth_type_table

UNWANTED_ARGS = [
    'migrate',
    'reset_db',
    'makemigrations',
    'style',
    'update_frontend',
    'testdbconn',
]


class LoginRateThrottle(throttling.AnonRateThrottle):
    scope = 'django_admin'


has_unwanted_args = len([argument for argument in UNWANTED_ARGS if argument in sys.argv]) > 0

if not has_unwanted_args:
    # refresh plugins and modules only if not working with migrations
    plugin_loader.refresh_plugins()
    module_factory.refresh_modules()
    if getattr(settings, 'UPDATE_SFA_TYPE_TABLE', True):
        update_second_factor_auth_type_table()

admin.autodiscover()

admin_docs_path = '{}{}doc/'.format(settings.URL_PREFIX, settings.DJANGO_ADMIN_URL_PREFIX)
admin_base_path = '{}{}'.format(settings.URL_PREFIX, settings.DJANGO_ADMIN_URL_PREFIX)


@api_view(['GET', 'POST'])
@permission_classes([permissions.AllowAny])
@throttle_classes([LoginRateThrottle])
def login(request):
    """
    Display the login form for the given HttpRequest.
    """
    self = AdminSite()
    if request.method == 'GET' and request.user.is_active and request.user.is_staff:
        # Already logged-in, redirect to admin index
        index_path = reverse('admin:index', current_app=self.name)
        return HttpResponseRedirect(index_path)

    request.current_app = self.name

    user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
    form_instance = AdminAuthenticationForm()
    if user is not None and user.is_staff:
        django_login(request, user)
        index_path = reverse('admin:index', current_app=self.name)
        return HttpResponseRedirect(index_path)
    elif (user is not None) or (user is None and request.method == 'POST'):
        error = form_instance.get_invalid_login_error()
        form_instance.cleaned_data = []
        form_instance.add_error(field=None, error=error)

    return render(request, 'admin/login.html', {'form': form_instance, 'title': 'Log in'})


urlpatterns = [
    # API URLs
    path('{}api/'.format(settings.URL_PREFIX), include('enduser.api_urls')),
    path('{}staffapi/'.format(settings.URL_PREFIX), include(('fleiostaff.urls', 'fleiostaff'), namespace='staff')),
]

if staff_active_features.is_enabled('billing.reseller'):
    urlpatterns.append(
        path(
            '{}resellerapi/'.format(settings.URL_PREFIX),
            include(('reseller.urls', 'reseller'), namespace='reseller'),
        ),
    )


if getattr(settings, 'ENABLE_DJANGO_ADMIN', False):
    urlpatterns.extend([
        # Django Admin URLs
        path(admin_docs_path, include('django.contrib.admindocs.urls')),
        # path(admin_base_path, admin.site.urls),
        url(r'^' + admin_base_path + 'login/', login, name='login'),
        url(r'^' + admin_base_path, admin.site.urls, name='admin'),
    ])
