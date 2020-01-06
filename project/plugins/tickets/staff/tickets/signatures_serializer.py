from plugins.tickets.models.signature import StaffSignature
from fleio.core.models import AppUser

from rest_framework import serializers


class StaffSignatureSerializer(serializers.ModelSerializer):
    content = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    user = serializers.PrimaryKeyRelatedField(queryset=AppUser.objects.filter(is_staff=True))
    department_display = serializers.SerializerMethodField(required=False, read_only=True)

    class Meta:
        model = StaffSignature
        fields = '__all__'

    @staticmethod
    def get_department_display(model: StaffSignature):
        if model.department:
            return model.department.name
        else:
            return 'N/A'
