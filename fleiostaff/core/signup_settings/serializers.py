from django.utils.translation import ugettext_lazy as _

from django.core.validators import EmailValidator

from rest_framework.exceptions import ValidationError

from fleio.conf.serializer import ConfSerializer
from fleio.notifications.models import NotificationTemplate


class SignUpSettingsSerializer(ConfSerializer):

    class Meta:
        fields = ('require_confirmation', 'email_confirmation_template', 'allow_free_email_addresses',
                  'forbidden_domains_for_email_signup', 'domains_for_email_signup_whitelist',)

    @staticmethod
    def _validate_list_of_domains(domains: str, field: str):
        default_error = ValidationError({field: _('Invalid list of domains')})
        if not domains:
            return
        if domains[-1] == ',':
            raise ValidationError({field: _('No domain after the last comma')})
        try:
            domains_list = domains.split(',')
        except ValueError:
            raise default_error
        validator = EmailValidator()
        for domain in domains_list:
            if not validator.validate_domain_part(domain_part=domain.strip()):
                raise default_error

    def validate(self, attrs):
        # validate email confirmation template
        try:
            self._validate_list_of_domains(
                domains=attrs.get('forbidden_domains_for_email_signup', None),
                field='forbidden_domains_for_email_signup'
            )
            self._validate_list_of_domains(
                domains=attrs.get('domains_for_email_signup_whitelist', None),
                field='domains_for_email_signup_whitelist'
            )
        except Exception as e:
            raise e
        email_confirmation_template = attrs.get('email_confirmation_template', None)
        if not email_confirmation_template:
            raise ValidationError({'email_confirmation_template': _('No email confirmation template set')})
        nt = NotificationTemplate.objects.filter(name=email_confirmation_template).first()
        if not nt:
            raise ValidationError({
                'email_confirmation_template': _('No notification template with the specified name found')
            })
        return attrs
