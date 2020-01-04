import logging

from django.db.models import Q
from django.http import StreamingHttpResponse
from django.utils.translation import ugettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from django.conf import settings as django_settings
from glanceclient.exc import HTTPNotFound
from rest_framework import filters
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from fleio.core.drf import SuperUserOnly
from fleio.core.exceptions import APIBadRequest
from fleio.core.exceptions import ForbiddenException
from fleio.core.exceptions import ObjectNotFound
from fleio.core.features import staff_active_features
from fleio.core.filters import CustomFilter
from fleio.core.models import Client
from fleio.core.permissions.permissions_cache import permissions_cache
from fleio.core.validation_utils import validate_cloud_objects_limit
from fleio.openstack import settings
from fleio.openstack.api.identity import IdentityAdminApi
from fleio.openstack.exceptions import APIConflict
from fleio.openstack.exceptions import handle
from fleio.openstack.images.api import Images
from fleio.openstack.images.api import get_metadata_catalog
from fleio.openstack.images.filters import OpenStackImageFilter
from fleio.openstack.models import Image
from fleio.openstack.models import Image as OpenstackImage
from fleio.openstack.models import Volume
from fleio.openstack.models import VolumeAttachments
from fleio.openstack.models import VolumeSnapshot
from fleio.openstack.models.image import OpenStackImageVisibility
from fleio.openstack.views.regions import get_regions
from fleio.reseller.utils import user_reseller_resources
from fleio.utils.model import statuses_dict_to_statuses_choices
from fleiostaff.openstack.images.serializers import StaffImageCreateSerializer
from fleiostaff.openstack.images.serializers import StaffImageSerializer
from fleiostaff.openstack.images.serializers import StaffImageUpdateSerializer
from fleiostaff.openstack.signals import staff_delete_image

LOG = logging.getLogger(__name__)


class AdminImageViewSet(viewsets.ModelViewSet):
    permission_classes = (SuperUserOnly,)
    serializer_class = StaffImageSerializer
    serializer_map = {'create': StaffImageCreateSerializer,
                      'update': StaffImageUpdateSerializer}
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend, CustomFilter, filters.SearchFilter)
    search_fields = ('name', 'id',)
    ordering_fields = ('name', 'id', 'type', 'status', 'created_at')
    filter_class = OpenStackImageFilter
    parser_classes = (JSONParser, MultiPartParser)

    def get_queryset(self):
        return OpenstackImage.objects.all().exclude(status='deleted')

    def get_serializer_class(self):
        return self.serializer_map.get(self.action, self.serializer_class)

    def list(self, request, *args, **kwargs):
        response = super().list(request=request, *args, **kwargs)
        response.data['permissions'] = permissions_cache.get_view_permissions(request.user, self.basename)
        return response

    @property
    def os_admin_api(self):
        if hasattr(self, 'request'):
            return IdentityAdminApi(request_session=self.request.session)
        else:
            return IdentityAdminApi()

    @action(detail=False, methods=['get'])
    def get_metadata_catalog(self, request, *args, **kwargs):
        del request, args, kwargs  # unused

        metadata_catalog = get_metadata_catalog(self.os_admin_api.session)
        return Response({'metadata_catalog': metadata_catalog})

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not validate_cloud_objects_limit():
            raise APIBadRequest(_('Licence cloud objects limit reached. Please check your license.'))
        try:
            os_image_api = Images(api_session=self.os_admin_api.session)
            image = os_image_api.create(owner=self.os_admin_api.project_id, **serializer.validated_data)
        except Exception as e:
            LOG.error(e)
            handle(self.request, message='Unable to create the image')
        else:
            headers = self.get_success_headers(serializer.data)
            data = serializer.data
            data['id'] = image.id
            reseller_resources = user_reseller_resources(self.request.user)
            if reseller_resources:
                Image.objects.update_or_create(
                    defaults={
                        'reseller_resources': reseller_resources,
                        'min_disk': serializer.validated_data.get('min_disk', 0),
                        'min_ram': serializer.validated_data.get('min_ram', 0),
                        'region': serializer.validated_data.get('region')
                    },
                    id=image.id,
                )
            return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_update(self, serializer):
        db_image = serializer.instance
        try:
            serializer.validated_data.pop('reseller_resources', None)
            Images(api_session=self.os_admin_api.session).update(db_image, **serializer.validated_data)
        except Exception as e:
            LOG.error("Cannot update image, reason: {}".format(repr(e)))
            handle(self.request, message='Unable to create the image')

    def get_image(self):
        db_image = self.get_object()
        os_api = Images(api_session=self.os_admin_api.session)
        return os_api.get(image=db_image)

    def perform_destroy(self, db_image):
        """Delete the image."""
        if staff_active_features.is_enabled('demo'):
            raise ForbiddenException(detail=_('Operation not allowed in demo mode'))

        img = self.get_image()
        if img.db_image.protected:
            raise APIConflict(_("Can't delete protected image"))
        try:
            img.delete()
            user = self.request.user
            staff_delete_image.send(sender=__name__, user=user, user_id=user.id,
                                    image_name=img.db_image.name, image_id=img.db_image.id,
                                    username=user.username, request=self.request)
        except Exception as e:
            LOG.error("Cannot delete image, reason: {}".format(repr(e)))
            handle(self.request)

    @action(detail=False, methods=['get'])
    def permissions(self, request):
        view_permissions = permissions_cache.get_view_permissions(request.user, self.basename)
        return Response(data=view_permissions)

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk):
        del request, pk  # unused
        image = self.get_object()
        try:
            Images(api_session=self.os_admin_api.session).deactivate(image=image)
        except (Exception, HTTPNotFound) as e:
            if type(e) == HTTPNotFound:
                raise ObjectNotFound(detail=e.details)
            LOG.exception(e)
            handle(self.request)
        return Response({'detail': _('Image {} deactivated').format(image)})

    @action(detail=True, methods=['post'])
    def reactivate(self, request, pk):
        del request, pk  # unused

        image = self.get_object()
        try:
            Images(api_session=self.os_admin_api.session).reactivate(image=image)
        except (Exception, HTTPNotFound) as e:
            if type(e) == HTTPNotFound:
                raise ObjectNotFound(detail=e.details)
            LOG.exception(e)
            handle(self.request)
        return Response({'detail': _('Image {} reactivated').format(image)})

    @action(detail=True, methods=['post'])
    def available_to_client(self, request, pk):
        del pk  # unused

        image = self.get_object()
        client_id = request.data.get('client', None)
        if not client_id:
            raise APIBadRequest(detail=_('Client ID required'))
        try:
            client = Client.objects.get(pk=client_id)
        except (Client.DoesNotExist, ValueError, TypeError):
            raise APIBadRequest(detail=_('Client does not exist'))
        needs_sharing = False
        sharing_message = None
        client_first_project = client.first_project  # Replace when multiple projects per client are supported
        # client.services.filter(openstack_project__project_id=image.owner).exists()
        if client_first_project and client_first_project.project_id != image.owner:
            # Image.owner is not in Client's project
            if image.visibility == OpenStackImageVisibility.PRIVATE:
                # Private images with owner different than Client need sharing
                needs_sharing = True
                sharing_message = _('Image is private and owned by another project')
            elif image.visibility == OpenStackImageVisibility.SHARED:
                # Shared image with owner different and client not in members need sharing
                if not image.members.filter(member=client_first_project).exists():
                    needs_sharing = False
                    sharing_message = _('Image is owned by another project')
        return Response({'needsSharing': needs_sharing,
                         'sharingMessage': sharing_message})

    @action(detail=True, methods=['get'])
    def download(self, request, pk):
        del pk, request  # unused

        if not staff_active_features.is_enabled('openstack.images.download'):
            raise ForbiddenException(_('Image download not allowed'))

        db_image = self.get_object()  # type: OpenstackImage
        try:
            images_api = Images(api_session=self.os_admin_api.session)
            image_data = images_api.download(image=db_image)
        except (Exception, HTTPNotFound) as e:
            if type(e) == HTTPNotFound:
                raise ObjectNotFound(detail=e.details)
            LOG.exception(e)
            handle(self.request)
        else:
            response = StreamingHttpResponse(streaming_content=image_data)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(db_image.name)
            return response

    @action(detail=False, methods=['GET'])
    def get_snapshots_for_instance(self, request):
        instance_uuid = request.GET.get('instance_uuid', None)
        reseller_resources = user_reseller_resources(user=self.request.user)
        volume_attachments = VolumeAttachments.objects.filter(server_id=instance_uuid).values('volume_id')
        volumes = Volume.objects.filter(id__in=volume_attachments)
        volume_snapshots_qs = VolumeSnapshot.objects.filter(volume__in=volumes)
        if reseller_resources:
            volume_snapshots_qs = volume_snapshots_qs.filter(
                project__service__client__reseller_resources=reseller_resources
            )
        volume_snapshots_count = volume_snapshots_qs.count()
        volume_snapshots_uuids = volume_snapshots_qs.values('id')
        image_snapshots = Image.objects.filter(
            Q(volume_snapshot_uuid__in=volume_snapshots_uuids) | Q(instance_uuid=instance_uuid)
        )
        if reseller_resources:
            image_snapshots = image_snapshots.filter(
                Q(reseller_resources=reseller_resources) |
                Q(project__service__client__reseller_resources=reseller_resources)
            )
        serializer = StaffImageSerializer(image_snapshots, many=True)
        return Response({
            'objects': serializer.data,
            'volume_snapshots_count': volume_snapshots_count,
        })

    @action(detail=False, methods=['get'])
    def create_options(self, request, *args, **kwargs):
        del args, kwargs  # unused

        selected_region, regions = get_regions(request)
        create_options = {'regions': regions,
                          'container_formats': [x for (x, y) in OpenstackImage.IMAGE_CONTAINER_FORMAT],
                          'disk_formats': [x for (x, y) in OpenstackImage.IMAGE_DISK_FORMAT],
                          'visibilities': [x for (x, y) in OpenstackImage.IMAGE_VISIBILITY],
                          'os_distros': [x for (x, y) in settings.OS_TYPES],
                          'hypervisor_types': [x for x in settings.OS_HYPERVISOR_TYPES],
                          'selected_region': selected_region,
                          'statuses': statuses_dict_to_statuses_choices(OpenstackImage.IMAGE_STATUS),
                          'allowed_formats': getattr(django_settings, 'OS_IMAGE_UPLOAD_FORMATS', [])
                          }
        return Response(create_options)
