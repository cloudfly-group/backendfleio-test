import logging

from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from fleio.activitylog.utils.decorators import log_enduser_activity
from fleio.billing.credit_checker import check_if_enough_credit
from fleio.core.drf import CustomPermissions, EndUserOnly
from fleio.core.permissions.permissions_cache import permissions_cache
from fleio.core.validation_utils import validate_cloud_objects_limit
from fleio.openstack.signals.signals import user_delete_volume
from fleio.openstack.views.regions import get_regions
from fleio.openstack.settings import OSConfig
from fleio.openstack.volumes.volume_status import VolumeStatus
from fleio.utils.model import statuses_dict_to_statuses_choices
from .filters import OpenStackVolumeFilter
from .serializers import (OpenstackVolumeCreateSerializer, OpenStackVolumeSerializer, OpenStackVolumeSerializerMin,
                          VolumeAttachmentSerializer, VolumeAttachSerializer, VolumeDetachSerializer,
                          VolumeExtendSerializer, VolumeNameSerializer, VolumeRevertSerializer)
from ..exceptions import APIBadRequest, APIConflict, handle, UnavailableException
from ..models import Image, Volume, VolumeAttachments, VolumeType
from ..models.image import OpenStackImageVisibility
from ..osapi import OSApi
from fleio.core.filters import CustomFilter

LOG = logging.getLogger(__name__)


@log_enduser_activity(
    category_name='openstack', object_name='volume',
)
class VolumesViewSet(viewsets.ModelViewSet):
    serializer_class = OpenStackVolumeSerializerMin
    serializer_map = {
        'create': OpenstackVolumeCreateSerializer,
        'retrieve': OpenStackVolumeSerializer,
        'attach': VolumeAttachSerializer,
        'detach': VolumeDetachSerializer,
        'rename': VolumeNameSerializer,
        'extend': VolumeExtendSerializer,
        'revert_to_snapshot': VolumeRevertSerializer,
    }
    lookup_field = 'id'
    http_method_names = ['get', 'post', 'options', 'delete', 'head']
    ordering_fields = ('name', 'size', 'status', 'created_at')
    permission_classes = (EndUserOnly, CustomPermissions)
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend, CustomFilter, filters.SearchFilter)
    search_fields = ('name', 'status', 'size', 'region', 'id')
    filter_class = OpenStackVolumeFilter

    def get_serializer_class(self):
        return self.serializer_map.get(self.action, self.serializer_class)

    def get_volume(self, volume=None):
        """Return a Volume class instance using a Volume model
        :param volume: fleio.openstack.models.Volume, overwrite the volume in request.
        :rtype: .volume.Volume
        """
        volume = volume or self.get_object()
        os_api = OSApi.from_request(request=self.request)
        return os_api.volumes.get(volume)

    def get_queryset(self):
        volumes = Volume.objects.filter(project__service__client__in=self.request.user.clients.all())
        return volumes

    def list(self, request, *args, **kwargs):
        response = super().list(request=request, *args, **kwargs)
        response.data['permissions'] = permissions_cache.get_view_permissions(request.user, self.basename)
        return response

    @staticmethod
    def get_size_increment(size_increments, volume_type, region):
        if type(size_increments) is dict:
            volume_size_increments_in_region = size_increments.get(region, [])
        else:
            volume_size_increments_in_region = {}
        size_increment = volume_size_increments_in_region.get(volume_type, 1)
        try:
            size_increment = int(size_increment)
        except (ValueError, TypeError):
            size_increment = 1
        return size_increment

    @action(detail=False, methods=['get'])
    def create_options(self, request, *args, **kwargs):
        client = self.request.user.clients.filter(services__openstack_project__isnull=False).first()
        if client is None:
            raise APIConflict(detail=_('No client with an OpenStack project associated found'))
        db_project = client.first_project
        conf = OSConfig()
        volume_size_increments = conf.volume_size_increments
        selected_region, regions = get_regions(request, filter_for='volumes', for_end_user=True)

        # get volume types
        volume_types = []
        for volume_type in VolumeType.objects.public().filter(region=selected_region):
            type_display = volume_type.description if volume_type.description else volume_type.name
            volume_types.append({'name': volume_type.name,
                                 'type_display': type_display,
                                 'sizeIncrement': self.get_size_increment(volume_size_increments,
                                                                          volume_type.name,
                                                                          selected_region)})

        available_images = Image.objects.get_images_for_project(project_id=db_project.project_id)
        available_images = available_images.filter(region=selected_region).distinct()

        # filter for reseller
        available_images = available_images.exclude(
            Q(visibility__in=[OpenStackImageVisibility.PUBLIC, OpenStackImageVisibility.COMMUNITY]) &
            ~Q(reseller_resources=client.reseller_resources)
        )

        available_volumes = Volume.objects.filter(project__service__client=client, region=selected_region)
        available_volumes = available_volumes.values('id', 'name', 'region')

        volume_sources = {'image': available_images.values('id', 'name', 'type', 'region', 'min_disk'),
                          'volume': available_volumes}

        return Response({
            'types': volume_types,
            'regions': regions,
            'sources': volume_sources,
            'selected_region': selected_region,
            'can_create_resource': check_if_enough_credit(
                client=self.request.user.clients.all().first(), update_uptodate_credit=False,
            ),
        })

    @action(detail=False, methods=['get'])
    def filter_options(self, request, *args, **kwargs):
        del args, kwargs  # unused
        selected_region, regions = get_regions(request, filter_for='volumes', for_end_user=True)
        filter_options = {
            'regions': regions,
            'statuses': statuses_dict_to_statuses_choices(VolumeStatus.status_map.items()),
        }
        return Response(filter_options)

    def perform_create(self, serializer):
        if not validate_cloud_objects_limit():
            raise APIBadRequest(_('Failed to create volume, please contact support'))
        os_api = OSApi.from_request(request=self.request)
        volume_source = serializer.validated_data.pop('source', {})
        source_type = volume_source.get('source_type')
        source = volume_source.get('source')
        source_id = source.pk if source else None
        try:
            os_api.volumes.create(name=serializer.validated_data['name'],
                                  size=serializer.validated_data['size'],
                                  region_name=serializer.validated_data['region'],
                                  type=serializer.validated_data.get('type', None),
                                  source_type=source_type,
                                  source_id=source_id)
        except Exception as e:
            LOG.error(e)
            handle(self.request, message=e)

    def perform_destroy(self, volume):
        volume = self.get_volume(volume=volume)
        if volume.status not in [
            'available', 'error', 'error_restoring', 'error_extending', 'error_deleting', 'deleting', 'creating',
        ]:
            raise UnavailableException(detail=_('Volume cannot be deleted now'))
        try:
            volume.delete()
        except Exception as e:
            LOG.debug(str(e))
            handle(self.request, message=_('Unable to delete volume'))
        else:
            user = self.request.user
            user_delete_volume.send(sender=__name__, user=user, user_id=user.id,
                                    volume_name=volume.volume.name, volume_id=volume.volume.id,
                                    username=user.username, request=self.request)

    @action(detail=True, methods=['POST'])
    def rename(self, request, id):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        volume = self.get_volume()
        try:
            volume.rename(name=serializer.validated_data['name'])
        except Exception as e:
            LOG.exception(e)
            handle(self.request, message=_('Unable to rename volume'))
        return Response({'detail': _('Renaming volume in progress')})

    @action(detail=True, methods=['POST'])
    def change_bootable_status(self, request, id):
        del id  # unused
        db_volume = self.get_object()
        volume = self.get_volume(db_volume)
        new_status = request.data.get('new_status')
        if not isinstance(new_status, bool):
            raise APIBadRequest(_('Invalid new status flag for volume bootable flag.'))
        try:
            volume.change_bootable_status(new_status=new_status)
        except Exception as e:
            LOG.debug(str(e))
            handle(self.request, message=_('Unable to update volume bootable flag.'))
        else:
            db_volume.bootable = new_status
            db_volume.save()
        return Response({'detail': _('Successfully changed volume bootable status flag.')})

    @action(detail=True, methods=['POST'])
    def extend(self, request, id):
        volume = self.get_volume()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            volume.extend(size=serializer.validated_data['size'])
        except Exception as e:
            LOG.error(e)
            handle(self.request, message=_('Unable to extend volume'))
        return Response({'detail': _('Extending volume in progress')})

    @action(detail=True, methods=['POST'])
    def revert_to_snapshot(self, request, id):
        volume = self.get_volume()
        if volume.volume.status != VolumeStatus.AVAILABLE:
            raise APIBadRequest(_('Cannot revert volume to snapshot only when it\'s status is available.'))
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            volume.revert_to_snapshot(snapshot_id=serializer.validated_data['snapshot_id'])
        except Exception as e:
            LOG.error(e)
            handle(self.request, message=_('Unable to revert volume to snapshot'))
        return Response({'detail': _('Volume revert to snapshot scheduled')})

    @action(detail=False, methods=['GET'])
    def get_attachments(self, request):
        instance_uuid = request.GET.get('instance_uuid', None)
        volume_attachments = VolumeAttachments.objects.filter(server_id=instance_uuid)
        serializer = VolumeAttachmentSerializer(volume_attachments, many=True)
        return Response({'objects': serializer.data})

    @action(detail=False, methods=['get'])
    def permissions(self, request):
        view_permissions = permissions_cache.get_view_permissions(request.user, self.basename)
        return Response(data=view_permissions)
