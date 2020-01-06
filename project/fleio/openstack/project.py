from __future__ import unicode_literals
from keystoneclient.client import Client as KeystoneClient
from keystoneclient import exceptions

from fleio.openstack.api.session import get_session
from fleio.openstack.models import Project as ProjectModel
from fleio.openstack.models import Instance as InstanceModel
from fleio.openstack.settings import plugin_settings


class Projects(object):
    @staticmethod
    def create(client):
        return ProjectModel.objects.create_project(client=client)


# TODO: this has the same name as the Project model class, we should rename this
class Project(object):
    def __init__(self, project_id, api_session):
        self.project_id = project_id
        self.api_session = api_session
        self.db_project = self.get_db_project()
        self._api_project = None

    @classmethod
    def with_scoped_session(cls, project_id, scoped_project_id, scoped_project_domain_id=None, cache=None):
        """Creates a keystone session with a token scoped to the requested project/domain."""
        scoped_session = get_session(auth_url=plugin_settings.AUTH_URL,
                                     project_id=scoped_project_id,
                                     project_domain_id=scoped_project_domain_id,
                                     admin_username=plugin_settings.USERNAME,
                                     admin_password=plugin_settings.PASSWORD,
                                     admin_domain_id=plugin_settings.USER_DOMAIN_ID,
                                     cache=cache,
                                     timeout=plugin_settings.TIMEOUT)
        return cls(project_id, scoped_session)

    @classmethod
    def with_admin_session(cls, project_id, cache=None):
        """Creates a keystone session with a token scoped to the fleio credentials."""
        return cls.with_scoped_session(project_id,
                                       plugin_settings.USER_PROJECT_ID,
                                       scoped_project_domain_id=plugin_settings.PROJECT_DOMAIN_ID or None,
                                       cache=cache)

    @property
    def identity_client(self):
        return KeystoneClient(version=plugin_settings.IDENTITY_API_VERSION,
                              interface=plugin_settings.DEFAULT_INTERFACE,
                              session=self.api_session)

    @property
    def instances(self):
        return InstanceModel.objects.filter(project=self.db_project)

    @property
    def api_project(self):
        if self._api_project is None:
            self._api_project = self.identity_client.projects.get(project=self.project_id)
        return self._api_project

    def get_db_project(self):
        return ProjectModel.objects.filter(project_id=self.project_id).first()

    def refresh_from_api(self):
        self._api_project = self.identity_client.projects.get(project=self.project_id)

    def refresh_from_db(self):
        self.db_project.refresh_from_db()

    def disable(self, reason=None):
        try:
            self.identity_client.projects.update(project=self.project_id, enabled=False)
        except exceptions.NotFound:
            # FIXME(tomo): Trying to suspend a project present in fleio but missing in OpenStack ?
            pass

    def enable(self):
        self.identity_client.projects.update(project=self.project_id, enabled=True)

    def update(self, name: str, description: str, enabled: bool):
        self.identity_client.projects.update(
            project=self.project_id,
            name=name,
            description=description,
            enabled=enabled
        )

    def delete(self):
        try:
            self.identity_client.projects.delete(project=self.project_id)
        except exceptions.NotFound:
            pass
