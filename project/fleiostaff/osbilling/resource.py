import logging
from django.utils.functional import cached_property

from fleio.openstack.api.cinder import cinder_client
from fleio.openstack.api.nova import nova_client
from fleio.openstack.api.identity import IdentityAdminApi
from fleio.openstack.settings import plugin_settings
from fleio.openstack.settings import OS_TYPES
from fleio.openstack.models import OpenstackInstanceFlavor
from fleio.openstack.models import VolumeType
from fleio.osbilling.models import BillingResource

LOG = logging.getLogger(__name__)


class ResourceHelper(object):
    def __init__(self, region=None, interface=None):
        self.name = 'resource'
        self.type = 'service'
        self.choice_functions = list()
        self.region = region or plugin_settings.DEFAULT_REGION
        self.interface = interface or plugin_settings.DEFAULT_INTERFACE

    def get_resource(self):
        try:
            resource = BillingResource.objects.get(name=self.name, type=self.type)
        except BillingResource.DoesNotExist:
            LOG.error('Unable to get the billing resource: {}'.format(self.name))
            resource = None
        return resource

    def get_attributes_choices(self):
        resource = self.get_resource()
        result = dict()
        if not resource:
            return result
        for attr in resource.attributes:
            f_name = 'list_{}'.format(attr['name'])
            if f_name in self.choice_functions and hasattr(self, f_name):
                result[attr['name']] = getattr(self, f_name)()
        return result


class InstanceHelper(ResourceHelper):
    def __init__(self):
        super(InstanceHelper, self).__init__()
        self.type = 'service'
        self.name = 'instance'
        self.choice_functions = ('list_instance_type', 'list_availability_zone', 'list_os_type')
        self.identity_admin = IdentityAdminApi

    @property
    def admin_session(self):
        return self.identity_admin().session

    @cached_property
    def nova_admin_api(self):
        """
        :rtype: novaclient.v2.client.Client
        """
        assert self.admin_session is not None, 'Unable to use admin_api without a Keystoneauth session'

        return nova_client(api_session=self.admin_session,
                           region_name=self.region,
                           endpoint_type=self.interface,
                           extensions=True)

    def list_instance_type(self):
        flavor_names = OpenstackInstanceFlavor.objects.values_list('name', flat=True)
        return sorted(set(flavor_names))

    def list_availability_zone(self):
        # FIXME(tomo): List AZs from all regions.
        # FIXME(tomo): Fail gracefully if api is not available
        azs = list()
        try:
            azs = self.nova_admin_api.availability_zones.list()
        except Exception as e:
            LOG.exception(e)
        return [az.zoneName for az in azs]

    def list_os_type(self):
        os_types = (ost[0] for ost in OS_TYPES)
        return os_types


class VolumeHelper(ResourceHelper):
    def __init__(self):
        super(VolumeHelper, self).__init__()
        self.type = 'service'
        self.name = 'volume'
        self.choice_functions = ('list_volume_type', )
        self.identity_admin = IdentityAdminApi

    @property
    def admin_session(self):
        return self.identity_admin().session

    @cached_property
    def cinder_admin_api(self):
        """
        :rtype: cinderclient.v3.client.Client
        """
        assert self.admin_session is not None, 'Unable to use admin_api without a Keystoneauth session'

        return cinder_client(api_session=self.admin_session)

    @staticmethod
    def list_volume_type():
        vtypes = VolumeType.objects.values_list('volume_type_id', flat=True)
        return sorted(set(vtypes))


class InstanceTrafficHelper(ResourceHelper):
    def __init__(self):
        super(InstanceTrafficHelper, self).__init__()
        self.type = 'internal'
        self.name = 'instance_traffic'
        self.choice_functions = ('list_instance_type', 'list_availability_zone', 'list_os_type')
        self.identity_admin = IdentityAdminApi

    @property
    def admin_session(self):
        return self.identity_admin().session

    @cached_property
    def nova_admin_api(self):
        """
        :rtype: novaclient.v2.client.Client
        """
        assert self.admin_session is not None, 'Unable to use admin_api without a Keystoneauth session'

        return nova_client(api_session=self.admin_session,
                           region_name=self.region,
                           endpoint_type=self.interface,
                           extensions=True)

    def list_instance_type(self):
        flavor_names = OpenstackInstanceFlavor.objects.values_list('name', flat=True)
        return sorted(set(flavor_names))

    def list_availability_zone(self):
        # FIXME(tomo): List AZs from all regions.
        # FIXME(tomo): Fail gracefully if api is not available
        azs = list()
        try:
            azs = self.nova_admin_api.availability_zones.list()
        except Exception as e:
            LOG.exception(e)
        return [az.zoneName for az in azs]

    def list_os_type(self):
        os_types = (ost[0] for ost in OS_TYPES)
        return os_types
