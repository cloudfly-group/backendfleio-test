from glanceclient import Client as GlanceClient
from fleio.openstack.settings import plugin_settings


def glance_client(api_session, region_name=None, version=None, interface=None):
    """
    :rtype: glanceclient.v2.client.Client
    """

    version = float(version or plugin_settings.IMAGE_API_VERSION)
    region_name = region_name or plugin_settings.DEFAULT_REGION
    interface = interface or plugin_settings.DEFAULT_INTERFACE
    return GlanceClient(version=version,
                        interface=interface,
                        session=api_session,
                        region_name=region_name)
