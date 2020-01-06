from designateclient.v2.client import Client as DesignateClient
from fleio.openstack.settings import plugin_settings


def designate_client(api_session, region_name=None, endpoint_type=None, all_projects=False,
                     extensions=None, auth=None, timeout=None, sudo_project_id=None, edit_managed=False):
    """Wrapper procedure around the designate client

    :rtype: designateclient.v2.client.Client type
    """

    region_name = region_name or plugin_settings.DEFAULT_REGION
    timeout = timeout or plugin_settings.TIMEOUT
    endpoint_type = endpoint_type or plugin_settings.DEFAULT_INTERFACE

    return DesignateClient(region_name=region_name, endpoint_type=endpoint_type, extensions=extensions,
                           all_projects=all_projects, session=api_session, auth=auth,
                           timeout=timeout, sudo_project_id=sudo_project_id, edit_managed=edit_managed)
