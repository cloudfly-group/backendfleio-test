import logging
import phonenumbers
from decimal import Decimal

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from fleio.core.clients.serializers import ClientMinSerializer
from fleio.core.models import AppUser, Currency
from fleio.core.plugins.plugin_config_types import PluginConfigTypes
from fleio.core.plugins.serialization import ComponentDataSerializer
from fleio.core.plugins.serialization import ComponentDataModelSerializer
from fleio.core.utils import check_password_complexity

LOG = logging.getLogger(__name__)


class UserSerializer(ComponentDataModelSerializer):
    clients = ClientMinSerializer(many=True, required=False)

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'last_login', 'is_active',
                  'language', 'clients', 'email_verified', 'mobile_phone_number', )
        component_name = 'UserSettings'
        plugin_config_type = PluginConfigTypes.enduser


class UserMinSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    @staticmethod
    def get_full_name(user):
        return user.get_full_name()

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'full_name')


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=255)
    remember_me = serializers.BooleanField(default=False, required=False)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class UpdateUserSerializer(ComponentDataSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, max_length=30, required=False, allow_null=True, allow_blank=True)
    old_password = serializers.CharField(write_only=True, required=False, allow_blank=True, allow_null=True)
    first_name = serializers.CharField(max_length=64)
    last_name = serializers.CharField(max_length=64)
    language = serializers.ChoiceField(choices=settings.LANGUAGES, required=False)
    mobile_phone_number = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        component_name = 'UserSettings'
        plugin_config_type = PluginConfigTypes.enduser

    @staticmethod
    def validate_mobile_phone_number(mobile_phone_number):
        if mobile_phone_number:
            try:
                numobj = phonenumbers.parse(number=mobile_phone_number)
            except Exception as e:
                raise serializers.ValidationError(_('Mobile phone number is invalid'))
            if not phonenumbers.is_valid_number(numobj=numobj):
                raise serializers.ValidationError(_('Mobile phone number is invalid'))
        return mobile_phone_number

    def validate_password(self, password):
        if password:
            validation_result = check_password_complexity(password)
            if not validation_result['password_ok']:
                error_list = [key for key, value in validation_result.items() if value is True]
                raise ValidationError(error_list)
            return password
        return None

    def validate_email(self, email):
        """Email and username are both unique."""
        if 'request' in self.context and self.context['request'].user.email != email:
            user_model = get_user_model()
            try:
                user_model.objects.get(email=email)
                raise serializers.ValidationError(_('Email not available'))
            except user_model.DoesNotExist:
                try:
                    user_model.objects.get(username=email)
                    raise serializers.ValidationError(_('Email not available'))
                except user_model.DoesNotExist:
                    return email
        return email


class PasswordResetSerializer(serializers.Serializer):
    username_or_email = serializers.CharField(max_length=255, validators=[UnicodeUsernameValidator()])

    def validate(self, attrs):
        """
        Given an email or a username, return matching user(s) who should receive a reset.
        """

        username_or_email = attrs.get('username_or_email', None)
        active_user = AppUser.objects.filter(Q(username__iexact=username_or_email, is_active=True) |
                                             Q(email__iexact=username_or_email, is_active=True))
        if len(active_user) > 1:
            raise ValidationError(detail=_('Reset password failed.'))

        if active_user:
            attrs['username_or_email'] = active_user.first()  # we can pick the first because of object uniqueness
        else:
            attrs['username_or_email'] = None

        return attrs


class CurrencySerializer(serializers.ModelSerializer):
    rate = serializers.DecimalField(min_value=Decimal('0.000001'), max_digits=12, decimal_places=6)

    class Meta:
        model = Currency
        fields = '__all__'
