from rest_framework import serializers

from fleio.core.models import TermsOfServiceAgreement


class TermsOfServiceAgreementSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermsOfServiceAgreement
        fields = '__all__'
