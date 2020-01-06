from __future__ import unicode_literals

from keystoneclient.exceptions import EndpointNotFound

from fleio.openstack.api.nova import nova_client


class Hypervisors(object):
    def __init__(self, api_session):
        """
        :type api_session: keystoneauth1.session.Session
        """
        self.api_session = api_session

    def get_hypervisors(self, region=None):
        """
        :param region: Openstack region name
        :return:
        """
        try:
            nc = nova_client(api_session=self.api_session, region_name=region)
            hypervisors = nc.hypervisors.list()
        except EndpointNotFound:

            return []
        else:
            return hypervisors
