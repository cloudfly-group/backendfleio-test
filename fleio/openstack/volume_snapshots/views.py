from django.utils.translation import ugettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from fleio.activitylog.utils.activity_helper import activity_helper
from fleio.activitylog.utils.decorators import log_enduser_activity
from fleio.core.drf import CustomPermissions, EndUserOnly
from fleio.core.exceptions import APIBadRequest
from fleio.core.filters import CustomFilter
from fleio.core.permissions.permissions_cache import permissions_cache
from fleio.core.validation_utils import validate_cloud_objects_limit
from fleio.openstack.exceptions import handle
from fleio.openstack.models import Volume, VolumeSnapshot
from fleio.openstack.models.volume_snapshot import VolumeSnapshotStatus
from fleio.openstack.osapi import OSApi
from fleio.openstack.volume_snapshots.serializers import VolumeSnapshotCreateSerializer
from fleio.openstack.volume_snapshots.serializers import VolumeSnapshotSerializer
from fleio.openstack.volume_snapshots.serializers import VolumeSnapshotUpdateSerializer
from fleio.utils.model import statuses_dict_to_statuses_choices


@log_enduser_activity(
    category_name='openstack', object_name='volume snapshot'
)
class VolumeSnapshotViewSet(viewsets.ModelViewSet):
    serializer_class = VolumeSnapshotSerializer
    serializer_map = {
        'create': VolumeSnapshotCreateSerializer,
        'update': VolumeSnapshotUpdateSerializer,
    }
    permission_classes = (CustomPermissions, EndUserOnly,)
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend, CustomFilter, filters.SearchFilter)
    search_fields = ('name', 'status', 'size', 'id')
    filter_fields = ('project_id', 'volume', 'volume__id')

    def get_queryset(self):
        volume_snapshots = VolumeSnapshot.objects.filter(project__service__client__in=self.request.user.clients.all())
        return volume_snapshots

    def get_serializer_class(self):
        return self.serializer_map.get(self.action, self.serializer_class)

    def list(self, request, *args, **kwargs):
        response = super().list(request=request, *args, **kwargs)
        response.data['permissions'] = permissions_cache.get_view_permissions(request.user, self.basename)
        return response

    def perform_create(self, serializer: VolumeSnapshotCreateSerializer):
        if not validate_cloud_objects_limit():
            raise APIBadRequest(_('Licence cloud objects limit reached. Please check your license.'))
        volume_id = serializer.validated_data.get('volume_id')
        volume = Volume.objects.filter(id=volume_id).first()
        if volume:
            os_api = OSApi.from_request(request=self.request)
            try:
                volume_snapshot = os_api.volume_snapshots.create(
                    region_name=volume.region,
                    **serializer.validated_data,
                )
                activity_helper.add_current_activity_params(object_id=volume_snapshot.id)
            except Exception as e:
                handle(self.request, message=str(e))
            return Response({'detail': _('Volume snapshot creation in progress')})
        else:
            raise APIBadRequest(_('Cannot create volume snapshot as related volume does not exist'))

    @action(detail=False, methods=['get'])
    def filter_options(self, request, *args, **kwargs):
        del args, kwargs, request  # unused
        filter_options = {
            'statuses': statuses_dict_to_statuses_choices(VolumeSnapshotStatus.status_map.items()),
        }
        return Response(filter_options)

    @action(detail=False, methods=['get'])
    def permissions(self, request):
        view_permissions = permissions_cache.get_view_permissions(request.user, self.basename)
        return Response(data=view_permissions)

    @action(detail=True, methods=['post'])
    def reset_state(self, request, pk):
        del pk  # unused
        os_volume_snapshot = self.get_openstack_volume_snapshot()
        state = request.data.get('state')
        if not state:
            raise APIBadRequest(_('Cannot reset state because new state was not provided.'))
        try:
            os_volume_snapshot.reset_state(state=state)
        except Exception as e:
            raise APIBadRequest(_(str(e)))
        return Response({'detail': _('State reset scheduled.')})

    def perform_update(self, serializer):
        db_volume_snapshot = serializer.instance
        os_volume_snapshot = self.get_openstack_volume_snapshot(volume_snapshot=db_volume_snapshot)
        try:
            os_volume_snapshot.update(
                name=serializer.validated_data.get('name', None),
                description=serializer.validated_data.get('description', None)
            )
        except Exception as e:
            handle(self.request, message=_('Unable to update volume snapshot: {}').format(str(e)))

    def get_openstack_volume_snapshot(self, volume_snapshot=None):
        volume_snapshot = volume_snapshot or self.get_object()
        os_api = OSApi.from_request(request=self.request)
        return os_api.volume_snapshots.get(volume_snapshot=volume_snapshot)

    def perform_destroy(self, volume_snapshot):
        os_volume_snapshot = self.get_openstack_volume_snapshot(volume_snapshot=volume_snapshot)
        try:
            os_volume_snapshot.delete()
        except Exception as e:
            handle(self.request, message=_('Unable to delete volume snapshot: {}').format(str(e)))
