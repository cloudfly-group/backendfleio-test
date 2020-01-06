from ipware.ip import get_ip

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now as utcnow

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from fleio.core.exceptions import APIBadRequest
from fleio.core.models import AppUser, TermsOfService, TermsOfServiceAgreement
from fleio.core.models import Client
from fleio.core.models import UserGroup
from fleio.core.terms_of_service.tos_settings import tos_settings
from fleio.core.utils import check_password_complexity

from isfreemail import is_free_mail

from fleio.core.signup.settings import signup_settings
from fleio.reseller.utils import client_reseller_resources


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, max_length=128)
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    tos_agreement = serializers.BooleanField(required=False, default=False)
    reseller_client_id = serializers.IntegerField(required=False, default=None, allow_null=True)

    class Meta:
        model = get_user_model()
        fields = (
            'email', 'password', 'first_name', 'last_name', 'language', 'tos_agreement',
            'reseller_client_id',
        )

    @staticmethod
    def validate_password(password):
        validation_result = check_password_complexity(password)
        if not validation_result['password_ok']:
            error_list = [key for key, value in validation_result.items() if value is True]
            raise ValidationError(detail=error_list)
        return password

    @staticmethod
    def _validate_email_from_signup_settings(email: str):
        email_parts = email.split('@')
        mail_server = email_parts[1]
        whitelist = list()
        if signup_settings.domains_for_email_signup_whitelist:
            whitelist = [x.strip() for x in signup_settings.domains_for_email_signup_whitelist.split(',')]
        blacklist = list()
        if signup_settings.forbidden_domains_for_email_signup:
            blacklist = [y.strip() for y in signup_settings.forbidden_domains_for_email_signup.split(',')]
        if mail_server in whitelist:
            # always allow whitelisted domain names for emails
            pass
        else:
            if not signup_settings.allow_free_email_addresses:
                if is_free_mail(email=email):
                    raise serializers.ValidationError(
                        _('You cannot register using an email address from free email services')
                    )
            if mail_server in blacklist:
                raise serializers.ValidationError(
                    _('You cannot register using this kind of email address')
                )
        return True

    def validate_email(self, email):
        """Email and username are both unique."""
        # validate email using sign up settings
        try:
            self._validate_email_from_signup_settings(email=email)
        except Exception as e:
            raise e
        try:
            self.Meta.model.objects.get(email=email)
            raise serializers.ValidationError(_('Email address already in use'))
        except self.Meta.model.DoesNotExist:
            try:
                self.Meta.model.objects.get(username=email)
                raise serializers.ValidationError(_('Somebody chose this email as their username'))
            except self.Meta.model.DoesNotExist:
                return email

    def create(self, validated_data):
        tos_agreement = validated_data.pop('tos_agreement', False)
        latest_tos = TermsOfService.objects.filter(
            draft=False
        ).order_by('-version').first()
        if tos_settings.require_end_users_to_agree_with_latest_tos and tos_agreement is False and latest_tos:
            raise APIBadRequest(_('You need to agree with terms of service before creating an account.'))
        valid_fields = {}
        for field_name, field_value in validated_data.items():
            if field_name in self.Meta.fields:
                valid_fields[field_name] = field_value
        valid_fields['username'] = validated_data.get('email')
        valid_fields['password'] = make_password(validated_data['password'])

        # set language on signup
        language = valid_fields.pop('language', None)
        if not language:
            language = getattr(settings, 'DEFAULT_USER_LANGUAGE', 'en')
        valid_fields['language'] = language

        reseller_client_id = valid_fields.pop('reseller_client_id', None)
        if reseller_client_id:
            reseller_client = Client.objects.get(id=reseller_client_id)
            reseller_resources = client_reseller_resources(client=reseller_client)
            valid_fields['reseller_resources'] = reseller_resources

        user = super(SignUpSerializer, self).create(valid_fields)
        # TODO: investigate why we cannot add group to user returned by serializer
        db_user = AppUser.objects.get(id=user.id)
        default_group = UserGroup.objects.filter(is_default=True).first()
        if default_group:
            db_user.user_groups.add(default_group)
        if tos_settings.require_end_users_to_agree_with_latest_tos and tos_agreement and latest_tos:
            TermsOfServiceAgreement.objects.get_or_create(
                user=db_user,
                terms_of_service=latest_tos,
                agreed=True,
                agreed_at=utcnow(),
                ip=get_ip(self.context['request'])
            )
        return db_user
