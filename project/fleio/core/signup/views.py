from rest_framework import viewsets
from rest_framework import throttling
from rest_framework import permissions
from rest_framework.response import Response

from fleio.core.signup.serializers import SignUpSerializer
from fleio.core.signup.settings import signup_settings
from fleio.core.signup.utils import generate_verification_token_and_send

from fleio.core import utils
from fleio.core.views import get_current_user_info


class SignUpRateThrottle(throttling.AnonRateThrottle):
    scope = 'signup'


class SignUpViewSet(viewsets.ViewSet):
    """New user account sign up API end-point."""

    permission_classes = (permissions.AllowAny,)
    throttle_classes = (SignUpRateThrottle,)

    @staticmethod
    def create(request):
        """Create a new user account."""
        serializer = SignUpSerializer(data=request.data.copy(), context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        utils.login_without_password(request, user)

        response_obj = dict(
            user=get_current_user_info(request.user)
        )

        if signup_settings.require_confirmation:
            # send confirmation email
            generate_verification_token_and_send(user=user)
            response_obj['needs_email_confirmation'] = signup_settings.require_confirmation

        return Response(response_obj)
