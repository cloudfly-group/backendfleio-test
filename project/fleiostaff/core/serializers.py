import logging
import phonenumbers

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from fleio.core.clients.serializers import ClientMinSerializer
from fleio.core.utils import check_password_complexity

LOG = logging.getLogger(__name__)


class StaffUserProfileSerializer(serializers.ModelSerializer):
    clients = ClientMinSerializer(many=True, required=False)

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'last_login', 'is_active',
                  'is_staff', 'language', 'clients', 'mobile_phone_number',)


class StaffUserProfileMinSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    @staticmethod
    def get_full_name(user):
        return user.get_full_name()

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'full_name')


class StaffUpdateUserProfileSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, max_length=30, required=False, allow_null=True, allow_blank=True)
    old_password = serializers.CharField(write_only=True, required=False, allow_blank=True, allow_null=True)
    first_name = serializers.CharField(max_length=64)
    last_name = serializers.CharField(max_length=64)
    language = serializers.ChoiceField(choices=settings.LANGUAGES, required=False)
    mobile_phone_number = serializers.CharField(required=False, allow_blank=True, allow_null=True)

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
