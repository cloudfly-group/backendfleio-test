from __future__ import unicode_literals

import logging

from fleio.openstack.api.nova import nova_client

LOG = logging.getLogger(__name__)


class Keypairs(object):
    def __init__(self, api_session, region_name):
        self.api_session = api_session
        self.region_name = region_name

    @property
    def compute_api(self):
        """
        :rtype: novaclient.v2.client.Client
        """
        assert self.api_session is not None, 'Unable to use compute_api without a Keystoneauth session'

        return nova_client(api_session=self.api_session, region_name=self.region_name)

    def create(self, name, public_key=None, **kwargs):
        """
        :type public_key: str or unicode, the key content. If None, a new one will be created
        :type name: str or unicode, the key name
        :rtype: novaclient.v2.keypairs.Keypair
        """
        return self.compute_api.keypairs.create(name=name, public_key=public_key, **kwargs)

    def delete(self, key_id, **kwargs):
        return self.compute_api.keypairs.delete(key=key_id, **kwargs)

    def delete_by_user(self, user):
        # TODO: maybe we should check if project is not None here
        project_id = user.clients.first().first_project.project_id
        nova_key_pattern = '{0}_{1}_{2}'.format('fleio', project_id, user.id)
        for key in [key_name.id for key_name in self.compute_api.keypairs.list()
                    if key_name.id.startswith(nova_key_pattern)]:
            self.compute_api.keypairs.delete(key)

    def list(self, **kwargs):
        """
        :rtype list[novaclient.v2.keypairs.Keypair]
        """
        return self.compute_api.keypairs.list(**kwargs)

    def list_by_name(self, name):
        keys = []
        for key in self.list():
            if name.lower() == key.name.lower():
                keys.append(key)
        return keys

    def create_if_missing(self, name, public_key):
        """Try to import a SSH Key in Nova if it's not already present."""
        key_list = self.list_by_name(name=name)
        if len(key_list) == 0:
            self.create(name=name, public_key=public_key)
        return name
