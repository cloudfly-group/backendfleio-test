import datetime
import pytz

from django.urls import resolve
from django.utils.timezone import now as utcnow
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from django.utils.translation import ugettext_lazy as _
from rest_framework import status

from fleio.core.models import TermsOfService, TermsOfServiceAgreement
from fleio.core.terms_of_service.tos_settings import tos_settings


class CheckTOSMiddleware(MiddlewareMixin):
    """Make sure the current user uses second factor authentication if settings make it required"""
    whitelisted_url_names = ('current-user', 'login', 'dynamic-ui-custom-menu-links', 'resend-email-confirmation',
                             'userprofile-create-options', 'userprofile-detail', 'userprofile-list',
                             'plugins-plugins-with-component', 'plugins-plugins-with-notifications',
                             'client-list', 'client-create-options', 'logout', 'reset-password',
                             'reset-password-confirm', 'email-sign-up-confirmation', 'dynamic-ui-plugin-data',
                             'tickets-get-current-user-tickets-count', 'get-external-billing-url',
                             'todo-get-current-user-todo-count', 'termsofserviceagreements-agree',
                             'termsofserviceagreements-list', 'termsofserviceagreements-detail',
                             'termsofserviceagreements-get-active-tos')

    @staticmethod
    def _forbid_response(request, mandatory_response: bool = False):
        new_tos_message = None
        if TermsOfServiceAgreement.objects.filter(user=request.user, agreed=True).count():
            new_tos_message = _('We have updated our terms and conditions.')
        if mandatory_response:
            message = _('You must agree with terms of service.')
        else:
            message = _('Please agree with terms of service.')
        response_message = '{} {}'.format(new_tos_message, message) if new_tos_message else message
        request.session['tos_notify'] = {
            'notified_at': utcnow().strftime('%B %d %Y - %H:%M:%S')
        }
        return JsonResponse({
            'detail': response_message,
            'checkTOS': True
        }, status=status.HTTP_428_PRECONDITION_REQUIRED)

    def process_request(self, request):
        if request.user.is_anonymous:
            return None
        elif request.user.is_staff:
            # tos for staff not implemented
            return None
        else:
            path_resolved = resolve(request.path_info)
            if tos_settings.require_end_users_to_agree_with_latest_tos:
                if path_resolved.url_name in self.whitelisted_url_names:
                    # allow whitelisted url names
                    return None
                latest_tos = TermsOfService.objects.filter(
                    draft=False
                ).order_by('-version').first()  # take the latest version
                try:
                    prepare_user_tos = TermsOfServiceAgreement.objects.get_or_create(
                        user=request.user,
                        terms_of_service=latest_tos
                    )
                    user_tos_agreement = prepare_user_tos[0]  # type: TermsOfServiceAgreement
                except Exception as e:
                    del e  # unused
                    # should have no reason to get here
                    return None
                if not user_tos_agreement.agreed:
                    now = utcnow()
                    if tos_settings.forbid_access_after:
                        forbid_after_datetime = datetime.datetime.strptime(
                            tos_settings.forbid_access_after,
                            '%Y-%m-%d %H:%M:%S'
                        )
                        forbid_after_datetime = forbid_after_datetime.replace(tzinfo=pytz.utc)
                        if now > forbid_after_datetime:
                            # if now is later than forbid_after setting, do not allow user to do any action
                            return self._forbid_response(request=request, mandatory_response=True)
                    # if he didn't agree and agreement is not mandatory (i.e. now is earlier or equal to forbid_after),
                    # notify him that he has to agree (page redirect in frontend) every x minutes (defined in settings)
                    # or after login
                    if 'tos_notify' in request.session:
                        notified_at = datetime.datetime.strptime(
                            request.session['tos_notify']['notified_at'],
                            '%B %d %Y - %H:%M:%S'
                        )
                        notified_at = notified_at.replace(tzinfo=pytz.utc)
                        elapsed_time_since_last_notified = now - notified_at
                        if elapsed_time_since_last_notified > datetime.timedelta(
                                minutes=tos_settings.ask_again_after
                        ):
                            # more than defined time passed since last notify
                            return self._forbid_response(request=request)
                        else:
                            # allow access as user was notified before the minutes limit
                            return None
                    else:
                        return self._forbid_response(request=request)
                return None
            return None
