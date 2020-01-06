from collections import OrderedDict

from django.utils.translation import ugettext_lazy as _

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from fleio.core.drf import StaffOnly
from fleio.core.exceptions import APIBadRequest
from fleio.core.exceptions import ForbiddenException
from fleio.core.features import staff_active_features
from fleio.core.models.custom_code import CodeInsertionPoints
from fleio.core.models.custom_code import CustomCode
from fleio.core.models.custom_code import FrontendFileTypes
from fleiostaff.core.frontend_customization.index_manager import IndexManager
from fleiostaff.core.frontend_customization.serializers import CustomCodeSerializer


class FrontendCustomizationView(ModelViewSet):
    permission_classes = (StaffOnly, )
    model = CustomCode
    queryset = CustomCode.objects.all()
    serializer_class = CustomCodeSerializer

    @action(detail=False, methods=['POST'])
    def save_custom_code(self, request, *args, **kwargs):
        if staff_active_features.is_enabled('demo'):
            raise ForbiddenException(detail=_('Operation not allowed in demo mode'))

        del args, kwargs  # unused

        custom_code = request.data.get('custom_code', None)
        if custom_code:
            for insertion_point in custom_code:
                custom_code_id = custom_code[insertion_point]['data'].get('id', None)
                instance = CustomCode.objects.filter(id=custom_code_id).first() if custom_code_id else None
                serializer = CustomCodeSerializer(
                    data=custom_code[insertion_point]['data'],
                    instance=instance)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()

        return Response()

    @action(detail=False, methods=['GET'])
    def get_custom_code(self, request, *args, **kwargs):
        del request, args, kwargs  # unused

        custom_code = OrderedDict()

        insertion_points = []
        for insertion_point in CodeInsertionPoints.code_insertion_points_name_map:
            db_data = {custom_code.frontend_file_type: CustomCodeSerializer(
                instance=custom_code
            ).data for custom_code in CustomCode.objects.filter(insertion_point=insertion_point)}

            self.add_insertion_point(custom_code, db_data, insertion_point, FrontendFileTypes.enduser_index)
            insertion_points.append('{}_{}'.format(insertion_point, FrontendFileTypes.enduser_index))

            self.add_insertion_point(custom_code, db_data, insertion_point, FrontendFileTypes.staff_index)
            insertion_points.append('{}_{}'.format(insertion_point, FrontendFileTypes.staff_index))

        return Response(data={
            'insertion_points': insertion_points,
            'custom_code': custom_code
        })

    @staticmethod
    def add_insertion_point(custom_code, db_data, insertion_point, frontend_file_type):
        if frontend_file_type in db_data:
            data = db_data[frontend_file_type]
        else:
            data = {
                'insertion_point': insertion_point,
                'code': '',
                'active': True,
                'frontend_file_type': frontend_file_type
            }
        custom_code['{}_{}'.format(insertion_point, frontend_file_type)] = {
            'display_name': CodeInsertionPoints.code_insertion_points_name_map[insertion_point],
            'file_display_name': FrontendFileTypes.frontend_file_types_map[frontend_file_type],
            'helptext': CodeInsertionPoints.code_insertion_points_helptext_map[insertion_point],
            'data': data
        }

    @action(detail=False, methods=['POST'])
    def update_frontend(self, request, *args, **kwargs):
        if staff_active_features.is_enabled('demo'):
            raise ForbiddenException(detail=_('Operation not allowed in demo mode'))

        del request, args, kwargs  # unused

        try:
            index_manager = IndexManager()
            index_manager.update_frontend()
        except IndexManager.IndexUpdateException as e:
            raise APIBadRequest(detail=e.detail)

        return Response()
