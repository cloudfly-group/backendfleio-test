import logging

from keystoneauth1.exceptions import ClientException, Conflict, ConnectFailure
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from django.utils.translation import ugettext_lazy as _

from fleio.core.permissions.permissions_cache import permissions_cache
from fleio.core.drf import CustomPermissions, StaffOnly
from fleio.core.exceptions import APIConflict, ForbiddenException
from fleio.core.exceptions import ServiceUnavailable
from fleio.core.features import staff_active_features

from fleio.openstack.api.identity import IdentityAdminApi
from fleio.openstack.models import Project
from fleio.openstack.settings import plugin_settings
from fleio.openstack.settings import get_excluded_projects
from fleiostaff.openstack.users.api import OpenStackStaffUserApi
from fleiostaff.openstack.users.serializers import UserCreateSerializer, UserSerializer

LOG = logging.getLogger(__name__)


class AdminOpenStackUsersViewSet(viewsets.ViewSet):
    permission_classes = (CustomPermissions, StaffOnly, )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__os_api = None
        self.__os_user_api = None

    def projects_queryset(self):
        return Project.objects.all()

    def get_identity_admin_api(self):
        if hasattr(self, 'request'):
            return IdentityAdminApi(request_session=self.request.session)
        else:
            return IdentityAdminApi()

    @property
    def os_api(self):
        if self.__os_api is None:
            try:
                self.__os_api = self.get_identity_admin_api()
            except (ClientException, ConnectFailure):
                raise ServiceUnavailable(_('Could not connect to openstack'))

        return self.__os_api

    @property
    def os_user_api(self):
        if self.__os_user_api is None:
            try:
                self.__os_user_api = OpenStackStaffUserApi(keystone_client=self.os_api.client)
            except (ClientException, ConnectFailure):
                raise ServiceUnavailable(_('Could not connect to openstack'))

        return self.__os_user_api

    def get_api_users(self):
        projects = {project.project_id: project for project in self.projects_queryset()}
        os_users = []

        excluded_project_ids = get_excluded_projects()

        for os_user in self.os_user_api.list_users():
            user_project_id = getattr(os_user, 'default_project_id', None)
            if user_project_id in excluded_project_ids:
                continue
            if user_project_id in projects.keys():
                os_user_data = os_user.to_dict()
                os_user_data["project_name"] = str(projects[os_user.default_project_id])
                os_users.append(os_user_data)
        return os_users

    def list(self, request):
        try:
            os_users = self.get_api_users()
            serializer = UserSerializer(data=os_users, many=True)
            serializer.is_valid(raise_exception=True)
        except ClientException as e:
            LOG.error('OpenStack list users failed, reason: {0}'.format(e))
            raise ValidationError({'detail': _('Unable to list users. Please contact support for more info')})
        else:
            return Response(serializer.data, status=HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def edit_user_data(self, request):
        projects = [{'id': project.project_id, 'name': str(project.name)} for project in self.projects_queryset()]
        return Response(projects)

    def create(self, request):
        """Create a user in OpenStack either in a project and assign default role or standalone"""

        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        os_user = None

        try:
            os_user = self.os_user_api.create_user(**serializer.validated_data)
            # only grant default role if it's assigned for somebody
            if getattr(os_user, 'default_project_id', None):
                self.os_user_api.grant_user_role(project_id=os_user.default_project_id,
                                                 user=os_user.name,
                                                 role=plugin_settings.default_role)
        except Conflict:
            raise APIConflict({'detail': _('Username taken. Choose a different name')})
        except ClientException as e:
            LOG.error('OpenStack user creation failed, reason: {0}'.format(e))
            if os_user is not None:
                self.os_user_api.delete_user(os_user)
            raise ValidationError({'detail': _('Unable to create the user in OpenStack. Check logs for more info')})
        else:
            serializer = UserSerializer(data=os_user.to_dict())
            serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        """Fetch an OpenStack user and its associated data"""

        try:
            os_user = self.os_user_api.get_user(user=pk).to_dict()
            serializer = UserSerializer(data=os_user)
            serializer.is_valid(raise_exception=True)
        except (ClientException, IndexError) as e:
            LOG.error('Could not fetch user {pk}, reason {0}'.format(e, pk=pk))
            raise ValidationError({'detail': _('Unable to fetch the user from OpenStack. Check logs for more info')})
        else:
            return Response(serializer.data, status=HTTP_200_OK)

    def update(self, request, pk=None):
        """Update an OpenStack user"""

        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            # TODO(Marius): when wanting to change projects for users, what needs to be done is the roles, so staff
            # TODO(Marius): should be able to mingle with which roles are active in which projects for which user
            user = self.os_user_api.update_user(user=pk, **serializer.validated_data)
        except (ClientException, IndexError) as e:
            LOG.error('Could not update user {pk}. Reason {0}'.format(e, pk=pk))
            raise ValidationError({'detail': _('Unable to update user in OpenStack. Check logs for more info')})
        else:
            serializer = UserSerializer(data=user.to_dict())
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, status=HTTP_200_OK)

    def destroy(self, request, pk=None):
        """Delete an OpenStack user"""

        if staff_active_features.is_enabled('demo'):
            raise ForbiddenException(detail=_('Operation not allowed in demo mode'))

        try:
            project_ids = [project.project_id for project in self.projects_queryset()]

            os_user = self.os_user_api.get_user(user=pk)
            if getattr(os_user, 'default_project_id', None) not in project_ids:
                LOG.error('Could not delete user with id {pk}, because project {project} not found in database.'
                          .format(pk=pk, project=os_user.default_project_id))
                raise ValidationError(
                    {'detail': _('Unable to delete the user from OpenStack. Check logs for more info')})

            self.os_user_api.delete_user(user=pk)
        except (ClientException, IndexError) as e:
            LOG.error('Could not delete user with id {pk}, reason: {0}'.format(e, pk=pk))
            raise ValidationError({'detail': _('Unable to delete the user from OpenStack. Check logs for more info')})
        else:
            return Response({'detail': _('User deleted')}, status=HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def permissions(self, request):
        view_permissions = permissions_cache.get_view_permissions(request.user, self.basename)
        return Response(data=view_permissions)

    @action(detail=False, methods=['post'])
    def get_openrc_file_content(self, request):
        region = request.data.get('region', '')
        user_name = request.data.get('user_name')
        default_project_id = request.data.get('default_project_id', '')
        content = """export OS_ENDPOINT_TYPE=publicURL
export OS_INTERFACE=publicURL

# COMMON OPENSTACK ENVS
export OS_USERNAME={}
export OS_PROJECT_ID={}
echo "Please enter your OpenStack password as user $OS_USERNAME: "
read -sr OS_PASSWORD_INPUT
export OS_PASSWORD=$OS_PASSWORD_INPUT
export OS_AUTH_URL={}
export OS_NO_CACHE=1
export OS_USER_DOMAIN_NAME=Default
export OS_PROJECT_DOMAIN_NAME=Default
export OS_REGION_NAME={}

# For openstackclient
export OS_IDENTITY_API_VERSION=3
export OS_AUTH_VERSION=3
""".format(user_name, default_project_id, plugin_settings.auth_url, region)
        return Response({'content': content})
