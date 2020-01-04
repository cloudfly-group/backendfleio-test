from __future__ import unicode_literals


class OpenStackUserApi(object):
    """Interface as admin user to OpenStack Identity API."""

    def __init__(self, keystone_client):
        self.client = keystone_client

    def create_user(self, name, domain=None, default_project=None, password=None, email=None,
                    description=None, enabled=True, **kwargs):
        """Create a user in OpenStack

        :returns: the created user returned from server.
        :rtype: :class:`keystoneclient.v3.users.User`
        """

        return self.client.users.create(name, domain=domain, default_project=default_project,
                                        password=password, email=email, description=description,
                                        enabled=enabled, **kwargs)

    def delete_user(self, user):
        """Delete a user in OpenStack

        :param user: str, the user to be deleted on the server.
        :returns: Response object with 204 status.
        :rtype: :class:`requests.models.Response`
        """

        return self.client.users.delete(user)

    def get_user(self, user):
        """Retrieve a user from OpenStack

        :param user: str, the user to be retrieved from the server.

        :returns: the specified user returned from server.
        :rtype: :class:`keystoneclient.v3.users.User`
        """

        return self.client.users.get(user)

    def list_role_assignments(self, user=None, group=None, project=None, domain=None, role=None, include_names=False):
        """:rtype list of OpenStack role assignment objects"""

        return self.client.role_assignments.list(user=user, group=group, project=project,
                                                 domain=domain, role=role, include_names=include_names)

    def update_user(self, user, name=None, domain=None, password=None, email=None, description=None, enabled=None,
                    default_project=None, **kwargs):
        """Update a user in OpenStack

        default_project: str, the new default project for the user
        enabled: bool, whether the user is enabled.

        :returns: the updated user returned from server.
        :rtype: :class:`keystoneclient.v3.users.User`
        """
        return self.client.users.update(user, name=name, domain=domain,
                                        password=password, email=email, description=description,
                                        enabled=enabled, default_project=default_project, **kwargs)

    def grant_user_role(self, project_id, user, role):
        """
        Add user with role to project_id

        :param project_id:
        :param user: user name
        :param role: role name
        :return:
        """
        role_obj = self.client.roles.list(name=role)[0]
        user_obj = self.client.users.list(name=user)[0]

        return self.client.roles.grant(role=role_obj.id, user=user_obj.id, project=project_id)
