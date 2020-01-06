import copy
import logging

from keystoneauth1.exceptions import ClientException, Conflict, ConnectFailure
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from django.utils.translation import ugettext_lazy as _

from fleio.billing.credit_checker import check_if_enough_credit
from fleio.core.permissions.permissions_cache import permissions_cache
from fleio.core.drf import CustomPermissions, EndUserOnly
from fleio.core.exceptions import APIConflict, ServiceUnavailable
from fleio.openstack.api.identity import IdentityAdminApi
from fleio.openstack.settings import plugin_settings
from .api import OpenStackUserApi
from .serializers import UserCreateSerializer, UserUpdateSerializer


LOG = logging.getLogger(__name__)


def fetch_os_project(request):
    """Returns the first openstack project for the user performing the request or throws exceptions"""

    # TODO(Marius): as soon as a client supports multiple projects, implement a create options view which
    # will return the available projects to select from to create a user in and also a list of roles
    client = request.user.clients.filter(services__openstack_project__isnull=False).first()

    if client is None:
        raise APIConflict(_('No client with an OpenStack project found'))

    return client.first_project


class OpenStackUsersViewSet(viewsets.ViewSet):
    permission_classes = (CustomPermissions, EndUserOnly, )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__os_api = None
        self.__os_user_api = None

    @property
    def identity_admin_api(self):
        if hasattr(self, 'request'):
            return IdentityAdminApi(request_session=self.request.session)
        else:
            return IdentityAdminApi()

    @property
    def os_api(self):
        if self.__os_api is None:
            try:
                self.__os_api = self.identity_admin_api
            except (ClientException, ConnectFailure):
                raise ServiceUnavailable(_('Could not connect to openstack'))

        return self.__os_api

    @property
    def os_user_api(self):
        if self.__os_user_api is None:
            try:
                self.__os_user_api = OpenStackUserApi(keystone_client=self.os_api.client)
            except (ClientException, ConnectFailure):
                raise ServiceUnavailable(_('Could not connect to openstack'))

        return self.__os_user_api

    @staticmethod
    def get_api_user_prefix(request):
        return '{}_'.format(request.user.username)

    def fetch_users_in_project(self, pk=None, project_id=None):
        """Fetches user(s) from an OpenStack project

        pk: str, the uuid of the user in OpenStack
        project_id: str, the uuid of the project in OpenStack

        rtype list of dicts, user(s) from project_id"""

        if not project_id:
            LOG.error('Cannot retrieve data without an OpenStack project id')
            raise ValidationError({'detail': _('Unable to fetch data. Please contact support for more info')})

        role_assignments = self.os_user_api.list_role_assignments(user=pk, project=project_id, include_names=True)

        # NOTE(Marius): If a user has more than one role on a project then they will have two entries for that user.
        duplicate_users = [role_assignment.user
                           for role_assignment in role_assignments
                           if role_assignment.user['name'] != plugin_settings.username]

        return list({user['id']: user for user in duplicate_users}.values())

    def list(self, request):
        """List all users associated with the first project of the first client of request.user in OpenStack"""

        project_id = fetch_os_project(request).project_id

        try:
            os_users = self.fetch_users_in_project(project_id=project_id)
        except ClientException as e:
            LOG.error('OpenStack list users failed, reason: {0}'.format(e))
            raise ValidationError({'detail': _('Unable to list users. Please contact support for more info')})
        else:
            return Response(os_users, status=HTTP_200_OK)

    def create(self, request):
        """Create a user in the first project of the first client of request.user in OpenStack and grant that user
        the default role in that project"""

        project = fetch_os_project(request)
        if project.disabled:
            # NOTE that this will still create the user in OpenStack if the database is not synced accurately
            raise ValidationError({'detail': _('Unable to create the user in OpenStack. Project is suspended')})

        create_data = copy.deepcopy(request.data)
        if plugin_settings.PREFIX_API_USERS_WITH_USERNAME:
            create_data['name'] = '{}{}'.format(
                self.get_api_user_prefix(request),
                create_data['name'],
            )

        serializer = UserCreateSerializer(data=create_data)
        serializer.is_valid(raise_exception=True)

        os_user = None

        try:
            serializer.validated_data['default_project'] = project.project_id
            serializer.validated_data['domain'] = project.project_domain_id or None
            # OpenStack user will have the same email as the user creating it
            serializer.validated_data['email'] = request.user.email
            os_user = self.os_user_api.create_user(**serializer.validated_data)
            self.os_user_api.grant_user_role(project_id=os_user.default_project_id,
                                             user=os_user.name,
                                             role=plugin_settings.default_role)
        except Conflict:
            raise APIConflict({'detail': _('Username taken. Choose a different name')})
        except ClientException as e:
            LOG.error('OpenStack user creation failed, reason: {0}'.format(e))
            if os_user is not None:
                self.os_user_api.delete_user(os_user)
            raise ValidationError({'detail': _('Unable to create the user in OpenStack')})

        return Response(os_user.to_dict(), status=HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        """Fetch an OpenStack user and its associated data from the first project of the first client of request.user"""

        project_id = fetch_os_project(request).project_id

        try:
            os_user_id = self.fetch_users_in_project(pk, project_id)[0]['id']
            os_user = self.os_user_api.get_user(user=os_user_id).to_dict()
        except (ClientException, IndexError):
            LOG.error('Could not fetch user {pk}. User not found in OpenStack'.format(pk=pk))
            raise ValidationError({'detail': _('Unable to fetch the user from OpenStack. User not found')})
        else:
            return Response(os_user, status=HTTP_200_OK)

    def update(self, request, pk=None):
        """Update an OpenStack users password from the first project of the first client of request.user"""

        serializer = UserUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        project = fetch_os_project(request)
        if project.disabled:
            # NOTE that this will still update the user in OpenStack if the database is not synced accurately
            raise ValidationError({'detail': _('Unable to create the user in OpenStack. Project is suspended')})

        if not serializer.validated_data:
            return Response(status=200)

        update_data = copy.deepcopy(serializer.validated_data)
        if plugin_settings.PREFIX_API_USERS_WITH_USERNAME:
            prefix = self.get_api_user_prefix(request)
            if not update_data['name'].startswith(prefix):
                update_data['name'] = update_data['name'] = '{}{}'.format(prefix, update_data['name'])

        try:
            os_user_id = self.fetch_users_in_project(pk, project.project_id)[0]['id']
            user = self.os_user_api.update_user(user=os_user_id, **update_data)
        except (ClientException, IndexError) as e:
            LOG.error('Could not update user {pk}. Reason {0}'.format(e, pk=pk))
            raise ValidationError({'detail': _('Unable to update user in OpenStack.'
                                               'Try again later or contact support')})
        else:
            return Response(user.to_dict(), status=HTTP_200_OK)

    def destroy(self, request, pk=None):
        """Delete an OpenStack user from the first project of the first client of request.user"""

        project = fetch_os_project(request)
        if project.disabled:
            # NOTE that this will still delete the user in OpenStack if the database is not synced accurately
            raise ValidationError({'detail': _('Unable to create the user in OpenStack. Project is suspended')})

        try:
            os_user_id = self.fetch_users_in_project(pk, project.project_id)[0]['id']
            self.os_user_api.delete_user(user=os_user_id)
        except (ClientException, IndexError):
            LOG.error('Could not delete user {pk}. User not found in OpenStack'.format(pk=pk))
            raise ValidationError({'detail': _('Unable to delete the user from OpenStack. '
                                               'Try again later or contact support')})
        else:
            return Response({'detail': _('User deleted')}, status=HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def permissions(self, request):
        view_permissions = permissions_cache.get_view_permissions(request.user, self.basename)
        return Response(data=view_permissions)

    @action(detail=False, methods=['get'])
    def create_options(self, request, *args, **kwargs):
        del args, kwargs  # unused
        create_options = {
            'prefix': self.get_api_user_prefix(request),
            'prefix_api_users_with_username': plugin_settings.PREFIX_API_USERS_WITH_USERNAME,
            'can_create_resource': check_if_enough_credit(
                client=self.request.user.clients.all().first(), update_uptodate_credit=False,
            ),
        }
        return Response(create_options)

    @action(detail=False, methods=['post'])
    def get_openrc_file_content(self, request):
        region = request.data.get('region', '')
        user_name = request.data.get('user_name')
        client = self.request.user.clients.all().first()
        project_id = ''
        if client:
            project_id = client.first_project.project_id if client.first_project else ''
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
""".format(user_name, project_id, plugin_settings.auth_url, region)
        return Response({'content': content})
