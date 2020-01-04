import logging

from typing import Optional

from fleio.openstack.api import identity
from fleio.openstack.settings import plugin_settings

LOG = logging.getLogger(__name__)


def get_magnum_endpoint_for_region(region_id: str, endpoint_type='public') -> Optional[str]:
    try:
        if not region_id:
            region_id = plugin_settings.default_region
        session = identity.IdentityAdminApi().session
        service_catalog = session.auth.get_access(session).service_catalog
        if service_catalog.catalog:
            for item in service_catalog.catalog:
                if item.get('type', None) == 'container-infra':
                    endpoints = item.get('endpoints', [])
                    for endpoint in endpoints:
                        if endpoint.get('interface', None) == endpoint_type:
                            if endpoint.get('region') == region_id:
                                return endpoint.get('url', '')
        return None
    except Exception as e:
        LOG.error('Error when trying to get magnum endpoint: {}'.format(str(e)))
        return None
