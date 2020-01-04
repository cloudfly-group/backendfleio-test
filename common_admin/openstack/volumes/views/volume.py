import logging

from cinderclient.exceptions import EndpointNotFound
from django.utils.translation import ugettext_lazy as _
from keystoneauth1.exceptions import Unauthorized
from rest_framework.decorators import action
from rest_framework.response import Response

from fleio.core.drf import SuperUserOnly
from fleio.core.models import Client
from fleio.core.permissions.permissions_cache import permissions_cache
from fleio.core.validation_utils import validate_cloud_objects_limit
from fleio.openstack.exceptions import APIBadRequest
from fleio.openstack.exceptions import OpenstackAuthError
from fleio.openstack.exceptions import UnavailableException
from fleio.openstack.exceptions import handle
from fleio.openstack.models import Image
from fleio.openstack.models import Volume
from fleio.openstack.models import VolumeType
from fleio.openstack.osapi import OSApi
from fleio.openstack.settings import OSConfig
from fleio.openstack.views.regions import get_regions
from fleio.openstack.volumes.serializers import VolumeAttachSerializer
from fleio.openstack.volumes.serializers import VolumeDetachSerializer
from fleio.openstack.volumes.serializers import VolumeExtendSerializer
from fleio.openstack.volumes.serializers import VolumeNameSerializer
from fleio.openstack.volumes.serializers import VolumeRevertSerializer
from fleio.openstack.volumes.views import VolumesViewSet
from fleiostaff.openstack.osadminapi import OSAdminApi
from fleiostaff.openstack.signals import staff_delete_volume
from fleiostaff.openstack.volumes.serializers import StaffVolumeCreateSerializer
from fleiostaff.openstack.volumes.serializers import StaffVolumeSerializer

LOG = logging.getLogger(__name__)


class AdminVolumeViewSet(VolumesViewSet):
    permission_classes = (SuperUserOnly,)
    serializer_class = StaffVolumeSerializer
    serializer_map = {
        'create': StaffVolumeCreateSerializer,
        'retrieve': StaffVolumeSerializer,
        'attach': VolumeAttachSerializer,
        'detach': VolumeDetachSerializer,
        'rename': VolumeNameSerializer,
        'extend': VolumeExtendSerializer,
        'revert_to_snapshot': VolumeRevertSerializer,
    }
    filter_fields = ('name', 'status', 'project', 'region', 'size', 'id')
    filter_class = None

    def get_volume(self, volume=None):
        volume = volume or self.get_object()
        os_api = OSAdminApi()
        return os_api.volumes.get(volume)

    def get_queryset(self):
        volumes = Volume.objects.all()
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
        selected_region, regions = get_regions(request, filter_for='volumes')
        # get volume size increments
        conf = OSConfig()
        volume_size_increments = conf.volume_size_increments
        # get volume types
        volume_types = []
        for volume_type in VolumeType.objects.public().filter(region=selected_region):
            type_display = volume_type.description if volume_type.description else volume_type.name
            volume_types.append({'name': volume_type.name,
                                 'type_display': type_display,
                                 'sizeIncrement': self.get_size_increment(volume_size_increments,
                                                                          volume_type.name,
                                                                          selected_region)})
        selected_client = request.query_params.get('client', None)
        db_project = None
        if selected_client:
            try:
                db_project = Client.objects.get(pk=selected_client).first_project
            except Client.DoesNotExist as e:
                LOG.error(e)

        available_images = Image.objects.filter(region=selected_region)
        if db_project:
            available_images = available_images.get_images_for_project(project_id=db_project.project_id)
        else:
            available_images = available_images.public()
        if selected_client:
            available_volumes = Volume.objects.filter(project__service__client__id=selected_client,
                                                      region=selected_region)
            available_volumes = available_volumes.values('id', 'name', 'region')
        else:
            available_volumes = []

        volume_sources = {'image': available_images.values('id', 'name', 'type', 'region', 'min_disk'),
                          'volume': available_volumes}

        return Response({
            'types': volume_types,
            'regions': regions,
            'sources': volume_sources,
            'selected_region': selected_region
        })

    def perform_create(self, serializer: StaffVolumeCreateSerializer):
        if not validate_cloud_objects_limit():
            raise APIBadRequest(_('Licence cloud objects limit reached. Please check your license.'))
        os_api = OSApi.from_project_id(project_id=serializer.validated_data['project'].project_id)
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
        except EndpointNotFound as e:
            LOG.error(e)
            raise APIBadRequest(detail=_('Cinder endpoint not found for region {}').format(
                serializer.validated_data['region'],
            ))
        except Unauthorized as e:
            LOG.error(e)
            raise OpenstackAuthError(_('Operation not allowed'))
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
            user = self.request.user
            staff_delete_volume.send(sender=__name__, user=user, user_id=user.id,
                                     volume_name=volume.volume.name, volume_id=volume.volume.id,
                                     username=user.username, request=self.request)
        except Exception as e:
            LOG.debug(str(e))
            handle(self.request, message=_('Unable to delete volume'))

    @action(detail=False, methods=['get'])
    def permissions(self, request):
        view_permissions = permissions_cache.get_view_permissions(request.user, self.basename)
        return Response(data=view_permissions)
