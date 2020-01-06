from rest_framework import serializers

from fleio.core.models import SecondFactorAuthType
from fleio.core.models.second_factor_auth import SecondFactorAuthMethod


class SecondFactorAuthTypeSerializer(serializers.ModelSerializer):
    related_method = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = SecondFactorAuthType
        exclude = ('enabled_to_staff', 'enabled_to_enduser',)

    def get_related_method(self, model):
        request = self.context.get('request')
        sfa_method = SecondFactorAuthMethod.objects.filter(type=model, user=request.user).first()
        if not sfa_method:
            return dict(enabled=False, default=False,)
        return dict(enabled=sfa_method.enabled, default=sfa_method.default,)
