import datetime

from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from fleio.conf.serializer import ConfSerializer
from fleio.core.exceptions import APIBadRequest
from fleio.core.models import TermsOfService


class StaffTOSSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermsOfService
        fields = '__all__'


class TermsOfServiceSettingsSerializer(ConfSerializer):

    class Meta:
        fields = (
            'require_end_users_to_agree_with_latest_tos',
            'forbid_access_after',
            'ask_again_after',
        )

    def update(self, instance, validated_data):
        forbid_access_after = validated_data.get('forbid_access_after', '')
        if forbid_access_after:
            try:
                datetime.datetime.strptime(
                    forbid_access_after,
                    '%Y-%m-%d %H:%M:%S'
                )
            except Exception:
                raise APIBadRequest(
                    _('Specify date in the following format: YYYY-MM-DD h:m:s, e.g.: 2019-10-01 12:00:00')
                )
        return super().update(instance=instance, validated_data=validated_data)
