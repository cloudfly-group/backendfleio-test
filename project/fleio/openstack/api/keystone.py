from keystoneauth1 import session
from keystoneauth1.identity import v3
from keystoneclient.v3.client import Client

from fleio.openstack.settings import plugin_settings


def keystone_client(auth_url, username, password, user_domain_id, user_project_id=None, version=None, verify=None,
                    interface=None, timeout=None):
    version = version or plugin_settings.IDENTITY_API_VERSION

    if verify is None:
        verify = plugin_settings.REQUIRE_VALID_SSL

    interface = interface or plugin_settings.DEFAULT_INTERFACE
    auth = v3.Password(auth_url=auth_url, username=username, password=password,
                       user_domain_id=user_domain_id, project_id=user_project_id)
    sess = session.Session(auth=auth, verify=verify, timeout=timeout)
    c = Client(session=sess, version=version, timeout=timeout, auth_url=auth_url, interface=interface)

    return c
