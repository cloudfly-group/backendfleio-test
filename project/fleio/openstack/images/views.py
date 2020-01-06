import logging

from django.db.models import Q
from django.http import StreamingHttpResponse
from django.conf import settings as django_settings

from glanceclient.exc import Forbidden as GlanceForbiddenException
from glanceclient.exc import HTTPNotFound as GlanceNotFoundException
from django.utils.translation import ugettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser, MultiPartParser

from fleio.activitylog.utils.decorators import log_enduser_activity
from fleio.billing.credit_checker import check_if_enough_credit
from fleio.core.exceptions import APIBadRequest
from fleio.core.exceptions import ObjectNotFound
from fleio.core.features import active_features
from fleio.core.permissions.permissions_cache import permissions_cache
from fleio.openstack.api.identity import IdentityUserApi
from fleio.openstack.configuration import OpenstackSettings
from fleio.openstack.models import Instance, Project, Volume, VolumeAttachments, VolumeSnapshot
from fleio.openstack.models.image import OpenStackImageVisibility
from fleio.openstack.models.image_members import ImageMembers, ImageMemberStatus
from fleio.openstack.views.regions import get_regions
from fleio.utils.model import statuses_dict_to_statuses_choices
from fleio.core.drf import CustomPermissions, EndUserOnly
from fleio.core.filters import CustomFilter
from fleio.core.validation_utils import validate_cloud_objects_limit
from fleio.openstack import settings
from fleio.openstack.exceptions import APIConflict, ForbiddenException, handle
from fleio.openstack.images.serializers import ImageSerializer
from fleio.openstack.osapi import OSApi
from fleio.openstack.signals.signals import user_delete_image
from .filters import OpenStackImageFilter
from ..models import Image
from .serializers import ImageCreateSerializer
from .serializers import ImageUpdateSerializer
from fleio.openstack.images.api import Image as APIImage

LOG = logging.getLogger(__name__)


@log_enduser_activity(
    category_name='openstack', object_name='image',
)
class ImageViewSet(viewsets.ModelViewSet):
    serializer_class = ImageSerializer
    permission_classes = (EndUserOnly, CustomPermissions)
    serializer_map = {'create': ImageCreateSerializer,
                      'update': ImageUpdateSerializer}
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend, CustomFilter, filters.SearchFilter)
    search_fields = ('name', 'id',)
    ordering_fields = ('name', 'id', 'type', 'status', 'created_at')
    filter_class = OpenStackImageFilter
    parser_classes = (JSONParser, MultiPartParser)

    def get_serializer_class(self):
        return self.serializer_map.get(self.action, self.serializer_class)

    def get_queryset(self):
        filter_params = Q(project__service__client__in=self.request.user.clients.all())
        try:
            project_id = self.request.user.clients.first().first_project.project_id
        except Exception:
            raise APIConflict(_('No client with an OpenStack project found'))
        else:
            if active_features.is_enabled('openstack.images.showshared'):
                filter_params = filter_params | Q(
                    visibility=OpenStackImageVisibility.SHARED, members__member_id=project_id,
                    members__status__in=(ImageMemberStatus.ACCEPTED, ImageMemberStatus.PENDING)
                )
        queryset = Image.objects.filter(filter_params).exclude(status='deleted')
        return queryset

    @property
    def os_api(self):
        return OSApi.from_request(request=self.request)

    def get_image(self):
        db_image = self.get_object()
        return self.os_api.images.get(image=db_image)

    def list(self, request, *args, **kwargs):
        response = super().list(request=request, *args, **kwargs)
        response.data['permissions'] = permissions_cache.get_view_permissions(request.user, self.basename)
        return response

    @action(detail=False, methods=['get'])
    def permissions(self, request):
        view_permissions = permissions_cache.get_view_permissions(request.user, self.basename)
        return Response(data=view_permissions)

    @action(detail=True, methods=['get'])
    def get_member_status(self, request, pk):
        del pk  # unused
        image = self.get_object()
        try:
            project = request.user.clients.first().first_project
        except (Exception, AttributeError) as e:
            del e  # unused
            raise APIBadRequest(_('Could not find related client OpenStack project.'))

        member = ImageMembers.objects.filter(image=image, member=project).first()
        if not member:
            raise APIBadRequest(_('Could not find details about image member.'))
        return Response({
            'status': member.status
        })

    @action(detail=True, methods=['post'])
    def update_image_member_status(self, request, pk):
        del pk  # unused
        image = self.get_object()
        member_status = request.data.get('member_status', None)

        if not member_status or (member_status != ImageMemberStatus.PENDING and
                                 member_status != ImageMemberStatus.ACCEPTED and
                                 member_status != ImageMemberStatus.REJECTED):
            raise APIBadRequest(_('Invalid member status received.'))

        try:
            project = request.user.clients.first().first_project
        except (Exception, AttributeError) as e:
            del e  # unused
            raise APIBadRequest(_('Could not find related client OpenStack project.'))
        api_session = IdentityUserApi(
            project.project_id,
            project.project_domain_id,
            cache=request.session
        ).session
        api_image = APIImage(db_image=image, api_session=api_session)
        try:
            api_image.update_member(member_project_id=project.project_id, member_status=member_status)
        except Exception as e:
            raise APIBadRequest(str(e))
        return Response({'detail': _('Image member status update sent.')})

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not validate_cloud_objects_limit():
            raise APIBadRequest(_('Licence cloud objects limit reached. Please check your license.'))
        if not active_features.is_enabled('openstack.images.updatecreate'):
            raise ForbiddenException(_('Image creation not allowed'))
        try:
            image = self.os_api.images.create(owner=self.os_api.project, **serializer.validated_data)
        except Exception as e:
            LOG.error(e)
            handle(self.request, message='Unable to create the image')
        else:
            headers = self.get_success_headers(serializer.data)
            data = serializer.data
            data['id'] = image.id
            return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_destroy(self, db_image):
        """Delete the image."""
        img = self.get_image()
        if img.db_image.protected:
            raise APIConflict(_("Can't delete protected image"))
        try:
            img.delete()
        except Exception as e:
            LOG.error(e)
            handle(self.request)
        else:
            user = self.request.user
            user_delete_image.send(sender=__name__, user=user, user_id=user.id,
                                   image_name=db_image.name, image_id=db_image.id,
                                   username=user.username, request=self.request)

    def perform_update(self, serializer):
        db_image = serializer.instance
        if not active_features.is_enabled('openstack.images.updatecreate'):
            raise ForbiddenException(_('Image editing not allowed'))
        try:
            self.os_api.images.update(image=db_image, **serializer.validated_data)
        except GlanceForbiddenException as e:
            LOG.exception(e)
            handle(self.request, message=_('Image update forbidden'))
        except Exception as e:
            LOG.exception(e)
            handle(self.request, message=_('Image update failed'))

    @action(detail=False, methods=['get'])
    def create_options(self, request):
        selected_region, regions = get_regions(request, for_end_user=True)
        client = request.user.clients.first()
        openstack_settings = OpenstackSettings.for_client(client=client) if client else None
        create_options = {
            'regions': regions,
            'container_formats': [x for (x, y) in Image.IMAGE_CONTAINER_FORMAT],
            'disk_formats': [x for (x, y) in Image.IMAGE_DISK_FORMAT],
            'visibilities': OpenStackImageVisibility.get_user_choices(),
            'os_distros': [x for (x, y) in settings.OS_TYPES],
            'selected_region': selected_region,
            'hypervisor_types': [x for x in settings.OS_HYPERVISOR_TYPES],
            'statuses': statuses_dict_to_statuses_choices(Image.IMAGE_STATUS),
            'cleanup_enabled': openstack_settings.auto_cleanup_images if openstack_settings else False,
            'cleanup_days': openstack_settings.auto_cleanup_number_of_days if openstack_settings else False,
            'cleanup_formats': openstack_settings.auto_cleanup_image_types if openstack_settings else None,
            'allowed_formats': getattr(django_settings, 'OS_IMAGE_UPLOAD_FORMATS', []),
            'can_create_resource': check_if_enough_credit(
                client=self.request.user.clients.all().first(), update_uptodate_credit=False,
            ),
        }
        return Response(create_options)

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk):
        del request, pk  # unused

        image = self.get_object()
        if not active_features.is_enabled('openstack.images.updatecreate'):
            raise ForbiddenException(_('Image deactivation not allowed'))
        try:
            self.os_api.images.deactivate(image=image)
        except (Exception, GlanceNotFoundException) as e:
            if type(e) == GlanceNotFoundException:
                raise ObjectNotFound(detail=e.details)
            LOG.exception(e)
            handle(self.request)
        return Response({'detail': _('Image {} deactivated').format(image)})

    @action(detail=True, methods=['post'])
    def reactivate(self, request, pk):
        del request, pk  # unused

        image = self.get_object()
        if not active_features.is_enabled('openstack.images.updatecreate'):
            raise ForbiddenException(_('Image reactivation not allowed'))
        try:
            self.os_api.images.reactivate(image=image)
        except (Exception, GlanceNotFoundException) as e:
            if type(e) == GlanceNotFoundException:
                raise ObjectNotFound(detail=e.details)
            LOG.exception(e)
            handle(self.request)
        return Response({'detail': _('Image {} reactivated').format(image)})

    @action(detail=True, methods=['get'])
    def download(self, request, pk):
        del pk, request  # unused

        if not active_features.is_enabled('openstack.images.download'):
            raise ForbiddenException(_('Image download not allowed'))

        db_image = self.get_object()  # type: Image
        try:
            image_data = self.os_api.images.download(image=db_image)
        except (Exception, GlanceNotFoundException) as e:
            if type(e) == GlanceNotFoundException:
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
        # check if the user requests snapshots for an instance that he owns
        instance = Instance.objects.filter(id=instance_uuid).first()
        if not instance:
            raise APIBadRequest(_('Cannot get snapshots for non existing instance.'))
        client_project = Project.objects.filter(service__client__in=request.user.clients.all()).first()  # type: Project
        if not client_project:
            raise APIBadRequest(_('Client does not have any project.'))
        if instance.project.project_id != client_project.project_id:
            raise ObjectNotFound()
        volume_attachments = VolumeAttachments.objects.filter(server_id=instance_uuid).values('volume_id')
        volumes = Volume.objects.filter(id__in=volume_attachments)
        volume_snapshots_qs = VolumeSnapshot.objects.filter(volume__in=volumes)
        volume_snapshots_count = volume_snapshots_qs.count()
        volume_snapshots_uuids = volume_snapshots_qs.values('id')
        image_snapshots = Image.objects.get_images_for_project(project_id=client_project.project_id).filter(
            Q(volume_snapshot_uuid__in=volume_snapshots_uuids) | Q(instance_uuid=instance_uuid)
        )
        serializer = ImageSerializer(image_snapshots, many=True)
        return Response({
            'objects': serializer.data,
            'volume_snapshots_count': volume_snapshots_count,
        })
