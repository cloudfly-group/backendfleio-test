from __future__ import unicode_literals

from fleio.openstack.users.api import OpenStackUserApi


class OpenStackStaffUserApi(OpenStackUserApi):

    def list_users(self, default_project=None, domain=None, group=None, **kwargs):
        """List all users from OpenStack"""

        # don't use this for filtering project specific users as it will retrieve all of them
        return self.client.users.list(default_project=default_project, domain=domain, group=group, **kwargs)
