from cinderclient.client import Client as CinderClient
from fleio.openstack.settings import plugin_settings


def cinder_client(api_session, region_name=None, service_type=None, version=None, interface=None, timeout=None):
    region_name = region_name or plugin_settings.DEFAULT_REGION
    interface = interface or plugin_settings.DEFAULT_INTERFACE
    version = (version or plugin_settings.volumev3_api_version or plugin_settings.volumev2_api_version or
               plugin_settings.VOLUME_API_VERSION)
    timeout = timeout or plugin_settings.TIMEOUT
    service_type = service_type or plugin_settings.VOLUME_SERVICE_TYPE
    return CinderClient(version=version,
                        service_type=service_type,
                        interface=interface,
                        timeout=timeout,
                        region_name=region_name,
                        session=api_session)
