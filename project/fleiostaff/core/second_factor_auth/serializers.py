from rest_framework import serializers

from fleio.conf.serializer import ConfSerializer
from fleio.core.models import SecondFactorAuthMethod, SecondFactorAuthType


class StaffSecondFactorAuthTypeSerializer(serializers.ModelSerializer):
    related_method = serializers.SerializerMethodField(read_only=True)
    name = serializers.CharField(read_only=True)

    class Meta:
        model = SecondFactorAuthType
        fields = '__all__'

    def get_related_method(self, model):
        request = self.context.get('request')
        sfa_method = SecondFactorAuthMethod.objects.filter(type=model, user=request.user).first()
        if not sfa_method:
            return dict(enabled=False, default=False,)
        return dict(enabled=sfa_method.enabled, default=sfa_method.default,)


class SFASettingsSerializer(ConfSerializer):

    class Meta:
        fields = ('require_end_users_to_use_sfa', 'require_staff_users_to_use_sfa',)
