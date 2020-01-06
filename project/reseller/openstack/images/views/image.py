import logging

from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from rest_framework.decorators import action

from common_admin.openstack.images.views.image import AdminImageViewSet
from fleio.activitylog.utils.decorators import log_reseller_activity
from fleio.core.drf import CustomPermissions
from fleio.core.drf import ResellerOnly
from fleio.core.exceptions import ForbiddenException
from fleio.openstack.models import Instance
from fleio.openstack.models.image import Image, OpenStackImageVisibility
from fleio.reseller.utils import user_reseller_resources

LOG = logging.getLogger(__name__)


@log_reseller_activity(
    category_name='openstack', object_name='image',
    additional_activities={
        'deactivate': _('Staff user {username} ({user_id}) deactivated {object_name} {object_id}.'),
        'reactivate': _('Staff user {username} ({user_id}) reactivated {object_name} {object_id}.'),
    }
)
class ResellerImageViewSet(AdminImageViewSet):
    permission_classes = (CustomPermissions, ResellerOnly,)

    def get_queryset(self):
        reseller_resources = user_reseller_resources(user=self.request.user)
        queryset = super().get_queryset().filter(
            Q(project__service__client__reseller_resources=reseller_resources) |
            Q(reseller_resources=reseller_resources) |
            (Q(visibility=OpenStackImageVisibility.PUBLIC) & Q(reseller_resources=None)),
        ).all()

        return queryset

    @staticmethod
    def is_manageable_by_reseller(user, db_image: Image, message):
        reseller_resources = user_reseller_resources(user=user)
        manageable = False
        try:
            if db_image.reseller_resources == reseller_resources:
                manageable = True
            if (not manageable and db_image.project.service and
                    (db_image.project.service.client.reseller_resources and
                     db_image.project.service.client.reseller_resources == reseller_resources)):
                manageable = True
            if (not manageable and 'image_type' in db_image.properties and
                    db_image.properties['image_type'] == 'snapshot'):
                # if snapshot, first check if related instance is related to the reseller resources
                if 'instance_uuid' in db_image.properties:
                    related_instance = Instance.objects.filter(id=db_image.properties['instance_uuid']).first()
                    if related_instance:
                        if related_instance.project.service.client.reseller_resources == reseller_resources:
                            manageable = True
        except Exception:
            raise ForbiddenException(_('Could not determine if image is related to reseller service.'))
        if not manageable:
            raise ForbiddenException(message)

    def perform_update(self, serializer):
        image = self.get_object()
        self.is_manageable_by_reseller(
            user=self.request.user,
            db_image=image,
            message=_('Cannot update image not related to reseller account')
        )
        serializer.validated_data['reseller_resources'] = image.reseller_resources
        super().perform_update(serializer)

    def perform_create(self, serializer):
        reseller_resources = user_reseller_resources(user=self.request.user)
        serializer.validated_data['reseller_resources'] = reseller_resources
        super().perform_update(serializer)

    def perform_destroy(self, db_image):
        self.is_manageable_by_reseller(
            user=self.request.user,
            db_image=db_image,
            message=_('Cannot delete image not related to reseller account')
        )
        super().perform_destroy(db_image=db_image)

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk):
        image = self.get_object()
        self.is_manageable_by_reseller(
            user=self.request.user,
            db_image=image,
            message=_('Cannot deactivate image not related to reseller account')
        )
        return super().deactivate(request=request, pk=pk)

    @action(detail=True, methods=['post'])
    def reactivate(self, request, pk):
        image = self.get_object()
        self.is_manageable_by_reseller(
            user=self.request.user,
            db_image=image,
            message=_('Cannot reactivate image not related to reseller account')
        )
        return super().reactivate(request=request, pk=pk)
