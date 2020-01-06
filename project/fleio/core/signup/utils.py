from django.conf import settings

from fleio.core.signup.signup_token import signup_token_generator
from fleio.core.utils import fleio_parse_url
from fleio.core.models import AppUser
from fleio.notifications import notifier


def send_email_confirmation_notification(email: str, variables: dict, user: AppUser):
    notifier.send(
        name='account.signup.confirm',
        variables=variables,
        to_emails=[email],
        user=user,
    )


def generate_verification_token_and_send(user):
    if user.reseller_resources:
        frontend_url = fleio_parse_url(user.reseller_resources.frontend_url)
    else:
        frontend_url = fleio_parse_url(settings.FRONTEND_URL)
    confirmation_token = signup_token_generator.make_token(user=user)
    confirmation_template_variables = dict(
        first_name=user.first_name if user.first_name else user.username,
        frontend_url=frontend_url,
        confirmation_token=confirmation_token,
    )
    send_email_confirmation_notification(email=user.email, variables=confirmation_template_variables, user=user)
