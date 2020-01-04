from django.conf import settings
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from fleio.activitylog.utils.decorators import log_staff_activity
from fleio.core.drf import SuperUserOnly
from fleio.core.models import Permission, PermissionSet

from fleiostaff.core.permissions.serializers import PermissionSerializer, PermissionUpdateSerializer
from fleiostaff.core.permissions.serializers import PermissionSetSerializer


class PermissionViewSet(mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.ListModelMixin,
                        GenericViewSet):
    permission_classes = (SuperUserOnly,)
    serializer_class = PermissionSerializer
    queryset = Permission.objects.all()
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend, filters.SearchFilter)
    ordering_fields = ('name', 'id',)
    filter_fields = ('name', 'permission_set')
    search_fields = ('name',)
    model = Permission

    serializer_map = {'retrieve': PermissionSerializer}

    def get_serializer_class(self):
        return self.serializer_map.get(self.action, self.serializer_class)


@log_staff_activity(category_name='core', object_name='permission set')
class PermissionSetViewSet(mixins.RetrieveModelMixin,
                           mixins.DestroyModelMixin,
                           mixins.ListModelMixin,
                           GenericViewSet):
    permission_classes = (SuperUserOnly,)
    serializer_class = PermissionSetSerializer
    queryset = PermissionSet.objects.all()
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend, filters.SearchFilter)
    ordering_fields = ('name', 'id',)
    filter_fields = ('name',)
    search_fields = ('name',)
    model = PermissionSet

    @action(detail=True, methods=['post'])
    def update_objects(self, request, pk):
        del pk  # unused
        """Updates permissions for a permission set"""
        permission_set = self.get_object()  # type: PermissionSet
        to_be_updated = Permission.objects.filter(permission_set=permission_set)
        serializer = PermissionUpdateSerializer(
            to_be_updated,
            data=request.data['objects'],
            many=True,
            context={
                # get the permission set that needs to be updated
                "permissions_set": permission_set.id
            }
        )
        if serializer.is_valid():
            serializer.save()
            implicitly_granted = getattr(settings, 'GRANT_ALL_PERMISSIONS_IMPLICITLY', False)
            permission_set.implicitly_granted = request.data.get('implicitly_granted', implicitly_granted)
            permission_set.save()
            return Response({'detail': 'Permissions updated'})
        else:
            return Response({'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
