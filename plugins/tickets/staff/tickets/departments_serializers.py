from plugins.tickets.models.department import Department
from plugins.tickets.models.utils.ticket_id import validate_ticket_id

from rest_framework import serializers


class DepartmentSerializer(serializers.ModelSerializer):
    created_at = serializers.ReadOnlyField()

    class Meta:
        model = Department
        fields = '__all__'

    @staticmethod
    def validate_ticket_id_format(id_format):
        result, message = validate_ticket_id(id_format=id_format)
        if result is True:
            return id_format
        else:
            raise serializers.ValidationError(detail=message)
