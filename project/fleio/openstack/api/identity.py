from __future__ import unicode_literals

from keystoneclient.client import Client

from .session import get_session
from ..settings import plugin_settings
from ..utils import OSAuthCache


class RoleDoesNotExist(Exception):
    pass


class IdentityUserApi(object):
    """Interface as admin user to OpenStack Identity API."""

    def __init__(self, project_id, project_domain_id=None, cache=None, version=None):
        """
        :param cache: Django HTTP session object or dict like object.
        """
        self._session = None
        self.version = version
        self.cache = None
        self._identity_client = None
        self.project_id = project_id
        self.project_domain_id = project_domain_id

        if cache is not None:
            self.cache = OSAuthCache(cache)

    def create_project(self, name, domain, description=None, enabled=True):
        return self.client.projects.create(name=name, domain=domain,
                                           description=description, enabled=enabled)

    def delete_project(self, project_id):
        return self.client.projects.delete(project=project_id)

    def grant_user_role(self, project_id, user, role):
        """
        Add user with role to project_id

        :param project_id:
        :param user: user name
        :param role: role name
        :return:
        """
        try:
            role_obj = self.client.roles.list(name=role)[0]
        except IndexError:
            raise RoleDoesNotExist()
        user_obj = self.client.users.list(name=user)[0]

        return self.client.roles.grant(role=role_obj.id, user=user_obj.id, project=project_id)

    @property
    def session(self):
        """The Keystone tenant session."""
        if self._session is None:
            self._session = get_session(auth_url=plugin_settings.AUTH_URL,
                                        project_id=self.project_id,
                                        project_domain_id=self.project_domain_id,
                                        admin_username=plugin_settings.USERNAME,
                                        admin_password=plugin_settings.PASSWORD,
                                        admin_domain_id=plugin_settings.USER_DOMAIN_ID,
                                        timeout=plugin_settings.TIMEOUT,
                                        cache=self.cache,
                                        verify=plugin_settings.REQUIRE_VALID_SSL)
        return self._session

    @property
    def client(self):
        """The Keystone tenant session."""
        if self._identity_client is None:
            self._identity_client = Client(version=self.version,
                                           session=self.session,
                                           interface=plugin_settings.DEFAULT_INTERFACE,
                                           auth_url=plugin_settings.AUTH_URL)
        return self._identity_client

    def get_available_regions(self, endpoint_type=None):
        auth_ref = self.session.auth.get_access(self.session)
        regions = list()
        if not auth_ref.has_service_catalog():
            # FIXME(tomo): Retrieve the service catalog from API
            return regions
        if endpoint_type is None:
            for service in auth_ref.service_catalog.catalog:
                for endp in service.get('endpoints'):
                    if service.get('type') is not None:
                        new_region = endp.get('region_id', endp.get('region', None))
                        if new_region is not None and new_region not in regions:
                            regions.append(new_region)
        else:
            for service in auth_ref.service_catalog.catalog:
                for endp in service.get('endpoints'):
                    if service.get('type') == endpoint_type:
                        new_region = endp.get('region_id', endp.get('region', None))
                        if new_region is not None and new_region not in regions:
                            regions.append(new_region)
        return regions


class IdentityAdminApi(IdentityUserApi):
    def __init__(self, request_session=None, version=None):
        super(IdentityAdminApi, self).__init__(project_id=plugin_settings.USER_PROJECT_ID,
                                               project_domain_id=plugin_settings.PROJECT_DOMAIN_ID,
                                               version=version,
                                               cache=request_session)
