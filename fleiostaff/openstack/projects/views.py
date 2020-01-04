import logging

from django.db.models import Count, Q
from django_filters.rest_framework import DjangoFilterBackend
from django_filters.rest_framework import FilterSet
from django_filters.rest_framework import NumberFilter
from django.utils.translation import ugettext_lazy as _
from rest_framework import filters
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action

from fleio.activitylog.utils.decorators import log_staff_activity
from fleio.core.permissions.permissions_cache import permissions_cache
from fleio.core.drf import CustomPermissions, StaffOnly
from fleio.core.exceptions import ForbiddenException, ObjectNotFound
from fleio.core.features import staff_active_features
from fleio.core.filters import CustomFilter

from fleio.openstack.api.identity import IdentityAdminApi
from fleio.openstack.models import Project
from fleio.openstack.project import Project as OpenstackProject
from fleio.openstack import tasks
from fleio.openstack.settings import plugin_settings
from fleio.openstack.settings import get_excluded_projects

from keystoneauth1.exceptions.http import NotFound

from fleiostaff.openstack.projects.serializers import StaffProjectSerializers

LOG = logging.getLogger(__name__)


class ProjectFilters(FilterSet):
    services_count = NumberFilter(field_name='services_count')

    class Meta:
        model = Project
        fields = ['services_count']


@log_staff_activity(
    category_name='openstack', object_name='project',
    additional_activities={
        'delete_project': _('Staff user {username} ({user_id}) deleted project ({object_id}).'),
    }
)
class StaffProjectViewSet(viewsets.ModelViewSet):
    serializer_class = StaffProjectSerializers
    serializer_map = {
        'create': StaffProjectSerializers,
        'update': StaffProjectSerializers
    }
    permission_classes = (CustomPermissions, StaffOnly,)
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend, CustomFilter, filters.SearchFilter)
    filter_class = ProjectFilters
    ordering_fields = ('project_id', 'project_domain_id', 'disabled', 'is_domain', 'name', 'created_at', 'updated_at')
    search_fields = ('project_id', 'project_domain_id', 'fleio_disabled_reason', 'name', 'description')
    ordering = ['-created_at']

    @property
    def identity_admin_api(self):
        if hasattr(self, 'request'):
            return IdentityAdminApi(request_session=self.request.session)
        else:
            return IdentityAdminApi()

    def get_queryset(self):
        if self.action == 'list':
            services_count = Count('service')
            return Project.objects.exclude(
                Q(project_id__in=get_excluded_projects()) | Q(deleted=True)
            ).annotate(
                services_count=services_count
            ).all()
        else:
            return Project.objects.all()

    def list(self, request, *args, **kwargs):
        response = super().list(request=request, *args, **kwargs)
        response.data['permissions'] = permissions_cache.get_view_permissions(request.user, self.basename)
        return response

    def get_serializer_class(self):
        return self.serializer_map.get(self.action, self.serializer_class)

    def destroy(self, request, *args, **kwargs):
        return Response(status=501, data={'detail': _('Not implemented')})

    def perform_update(self, serializer):
        db_project = Project.objects.get(id=serializer.validated_data['id'])
        openstack_project = OpenstackProject.with_admin_session(db_project.project_id)
        try:
            openstack_project.update(
                name=serializer.validated_data['name'],
                description=serializer.validated_data['description'],
                enabled=not serializer.validated_data['disabled']
            )
        except NotFound as e:
            raise ObjectNotFound(detail=e)

    def perform_create(self, serializer):
        self.identity_admin_api.client.projects.create(
            name=serializer.validated_data['name'],
            description=serializer.validated_data['description'],
            domain=plugin_settings.PROJECT_DOMAIN_ID,
            enabled=not serializer.validated_data.get('disabled', False)
        )

    @action(detail=True, methods=['post'])
    def delete_project(self, request, pk):
        del pk  # unused

        if staff_active_features.is_enabled('demo'):
            raise ForbiddenException(detail=_('Operation not allowed in demo mode'))

        delete_all_resources = request.data.get('delete_all_resources', False)
        instance = self.get_object()
        if delete_all_resources:
            tasks.delete_client_project_resources.delay(project_id=instance.project_id, mark_project_as_deleted=False)
            return Response(
                status=200,
                data={'details': _('Project delete scheduled')}
            )
        else:
            project = OpenstackProject.with_admin_session(instance.project_id)
            project.delete()
            return Response(
                status=200,
                data={'details': _('Project deleted')}
            )

    @action(detail=False, methods=['get'])
    def permissions(self, request):
        view_permissions = permissions_cache.get_view_permissions(request.user, self.basename)
        return Response(data=view_permissions)
