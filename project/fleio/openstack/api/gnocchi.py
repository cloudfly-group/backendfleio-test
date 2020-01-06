from gnocchiclient.client import Client as GnocchiClient
from keystoneauth1 import adapter

from fleio.openstack.settings import plugin_settings


def gnocchi_client(api_session, region_name=None, service_type='metric', version=None, interface=None):
    region_name = region_name or plugin_settings.DEFAULT_REGION
    interface = interface or plugin_settings.DEFAULT_INTERFACE
    version = int(float((version or plugin_settings.METRIC_API_VERSION)))
    session = adapter.Adapter(api_session, service_type=service_type, interface=interface, region_name=region_name)
    return GnocchiClient(version=version, session=session)
