from django.contrib.auth import get_user_model
from django.urls import resolve
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin


class ImpersonateUserMiddleware(MiddlewareMixin):
    """Impersonate a user"""

    @staticmethod
    def process_request(request):
        if request.user and 'impersonate' in request.session and request.user.can_impersonate:
            if resolve(request.path_info).view_name.startswith('staff:'):
                return
            if resolve(request.path_info).view_name.startswith('reseller:'):
                if request.user.is_reseller:
                    return
            if request.path.startswith(''.join(['/', settings.DJANGO_ADMIN_URL_PREFIX])):
                return
            user_id = request.session['impersonate']
            try:
                user = get_user_model().objects.get(pk=user_id, is_active=True, is_staff=False)
            except get_user_model().DoesNotExist:
                request.session.pop('impersonate')
                return
            else:
                request.impersonator = request.user
                request.user = user
