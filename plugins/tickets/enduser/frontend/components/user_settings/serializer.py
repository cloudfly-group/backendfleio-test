from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers

from plugins.tickets.models.tickets_user_settings import TicketsUserSettings


class TicketsUserSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketsUserSettings
        fields = '__all__'
        extra_kwargs = {
            'user': {
                'validators': [UnicodeUsernameValidator()],
            }
        }
