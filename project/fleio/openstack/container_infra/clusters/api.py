import logging
from typing import Optional

from magnumclient.common.apiclient.exceptions import EndpointNotFound

from fleio.openstack.container_infra.endpoint import get_magnum_endpoint_for_region

from fleio.openstack.api.magnum import magnum_client

from magnumclient.exceptions import NotFound

LOG = logging.getLogger(__name__)


class Clusters:
    def __init__(self, api_session):
        self.api_session = api_session

    def get(self, cluster):
        return Cluster(cluster, api_session=self.api_session)

    def create(self, region_id, keypair, *args, **kwargs):
        endpoint_override = get_magnum_endpoint_for_region(region_id=region_id)
        if not endpoint_override:
            raise EndpointNotFound('Magnum endpoint not found for this region.')
        mc = magnum_client(api_session=self.api_session, region_name=region_id, endpoint_override=endpoint_override)
        try:
            return mc.clusters.create(keypair=keypair, *args, **kwargs)
        except Exception as e:
            raise e


class Cluster:
    def __init__(self, cluster, api_session=None):
        self.api_session = api_session
        self.cluster = cluster

    @property
    def magnum_api(self):
        assert self.api_session is not None, 'Unable to use magnum_client without a Keystoneauth session'
        region = self.cluster.region if self.cluster.region else None
        if not region and self.cluster.cluster_template:
            region = self.cluster.cluster_template.region
        endpoint_override = get_magnum_endpoint_for_region(region_id=region)
        if not endpoint_override:
            raise EndpointNotFound('Magnum endpoint not found for this region.')
        return magnum_client(api_session=self.api_session, region_name=region, endpoint_override=endpoint_override)

    def get_details_from_os(self):
        try:
            return self.magnum_api.clusters.get(id=self.cluster.id)
        except NotFound:
            return None

    def delete(self):
        try:
            self.magnum_api.clusters.delete(id=self.cluster.id)
        except NotFound:
            self.cluster.delete()

    def update(self, *args, **kwargs):
        raise NotImplementedError()

    def resize(self, node_count: int, nodes_to_remove: Optional[list] = None):
        return self.magnum_api.clusters.resize(
            cluster_uuid=self.cluster.id,
            node_count=node_count,
            nodes_to_remove=nodes_to_remove
        )

    def generate_certificate(self, csr):
        return self.magnum_api.certificates.create(cluster_uuid=self.cluster.id, csr=csr)

    def get_certificate(self):
        return self.magnum_api.certificates.get(cluster_uuid=self.cluster.id)
