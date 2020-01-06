from rest_framework import serializers

from fleio.core.models.custom_code import CodeInsertionPoints
from fleio.core.models.custom_code import CustomCode
from fleio.core.models.custom_code import FrontendFileTypes

from fleio.utils.model import dict_to_choices


class CustomCodeSerializer(serializers.ModelSerializer):
    insertion_point = serializers.ChoiceField(
        choices=dict_to_choices(CodeInsertionPoints.code_insertion_points_name_map)
    )
    frontend_file_type = serializers.ChoiceField(choices=dict_to_choices(FrontendFileTypes.frontend_file_types_map))

    class Meta:
        model = CustomCode
        fields = '__all__'
