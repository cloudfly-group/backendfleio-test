from plugins.tickets.models.department import Department

from rest_framework import serializers


class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = (
            'id',
            'name',
            'email',
        )
