from __future__ import unicode_literals

import json

from novaclient.client import exceptions

from fleio.openstack.api.nova import nova_client
from fleio.openstack.models import OpenstackInstanceFlavor


class Flavors(object):
    def __init__(self, api_session):
        """
        :type api_session: keystoneauth1.session.Session
        """
        self.api_session = api_session

    def get(self, flavor):
        """
        :type flavor: fleio.openstack.models.OpenstackInstanceFlavor
        :rtype: Flavor
        """
        return Flavor(flavor, api_session=self.api_session)

    def create(self, name, ram, vcpus, disk, flavorid, ephemeral=0, swap=0, rxtx_factor=1.0, is_public=True,
               region=None):

        novaclient = nova_client(api_session=self.api_session, region_name=region)

        return novaclient.flavors.create(name, ram, vcpus, disk, flavorid=flavorid, ephemeral=ephemeral,
                                         swap=swap, rxtx_factor=rxtx_factor, is_public=is_public)

    def delete_all(self):
        flavors = OpenstackInstanceFlavor.objects.all()
        for flavor in flavors:
            Flavor(db_flavor=flavor, api_session=self.api_session).delete()


class Flavor(object):
    def __init__(self, db_flavor, api_session=None):
        """
        :type db_flavor: fleio.openstack.models.OpenstackInstanceFlavor
        """
        self.db_flavor = db_flavor
        self.api_session = api_session

    @property
    def nova_api(self):
        """
        :rtype: novaclient.v2.client.Client
        """
        assert self.api_session is not None, 'Unable to use nova_api without an api_session!'
        # TODO(Marius): refactor this class, the way it uses the nova client
        return nova_client(api_session=self.api_session, region_name=self.db_flavor.region.id)

    def set_properties(self, new_properties):
        api_flavor = self.nova_api.flavors.get(self.db_flavor.id)
        api_flavor.set_keys(metadata=new_properties)
        self.db_flavor.properties = json.dumps(api_flavor.get_keys())
        self.db_flavor.save()

    def unset_property(self, property_key):
        api_flavor = self.nova_api.flavors.get(self.db_flavor.id)
        api_flavor.unset_keys([property_key])
        self.db_flavor.properties = json.dumps(api_flavor.get_keys())
        self.db_flavor.save()

    def delete(self):
        """Delete the flavor from Nova."""
        try:
            self.nova_api.flavors.delete(flavor=self.db_flavor)
        except exceptions.NotFound:
            pass
        else:
            self.db_flavor.delete()
