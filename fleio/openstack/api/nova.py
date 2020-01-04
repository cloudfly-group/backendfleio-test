from novaclient.api_versions import APIVersion
from novaclient.client import Client as NovaClient
from novaclient.client import discover_extensions
from fleio.openstack.settings import plugin_settings


def nova_client(api_session, region_name=None, endpoint_type=None, service_type='compute', version=None, timeout=None,
                extensions=False):
    """
    :rtype: novaclient.v2.client.Client
    """

    endpoint_type = endpoint_type or plugin_settings.DEFAULT_INTERFACE
    timeout = timeout or plugin_settings.TIMEOUT
    region_name = region_name or plugin_settings.DEFAULT_REGION
    if version:
        if not isinstance(version, APIVersion):
            version = APIVersion(version_str=version)
    else:
        version = APIVersion(plugin_settings.COMPUTE_API_VERSION)

    exts = discover_extensions(version=version) if extensions else None

    return NovaClient(version=version,
                      region_name=region_name,
                      service_type=service_type,
                      endpoint_type=endpoint_type,
                      session=api_session,
                      timeout=timeout,
                      extensions=exts)
