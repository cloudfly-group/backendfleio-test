from magnumclient.client import Client as MagnumClient

from fleio.openstack.settings import plugin_settings


def magnum_client(api_session, endpoint_override, region_name=None, endpoint_type=None, service_type=None,
                  version=None, timeout=None,):
    region_name = region_name or plugin_settings.DEFAULT_REGION
    timeout = timeout or plugin_settings.TIMEOUT
    endpoint_type = endpoint_type or plugin_settings.DEFAULT_INTERFACE
    client_params = dict(
        region_name=region_name,
        service_type=service_type,
        endpoint_type=endpoint_type,
        session=api_session,
        timeout=timeout,
        endpoint_override=endpoint_override,
        api_version=version if version else 'latest'
    )
    return MagnumClient(**client_params)
