import logging

from magnumclient.common.apiclient.exceptions import EndpointNotFound

from fleio.openstack.api.magnum import magnum_client
from fleio.openstack.container_infra.endpoint import get_magnum_endpoint_for_region

from fleio.openstack.models import ClusterTemplate as ClusterTemplateModel

from magnumclient.exceptions import NotFound

LOG = logging.getLogger(__name__)


class ClusterTemplates:
    def __init__(self, api_session):
        self.api_session = api_session

    def get(self, cluster_template):
        return ClusterTemplate(cluster_template, api_session=self.api_session)

    def create(self, *args, **kwargs):
        region = kwargs.pop('region')
        endpoint_override = get_magnum_endpoint_for_region(region_id=region)
        if not endpoint_override:
            raise EndpointNotFound('Magnum endpoint not found for this region.')
        mc = magnum_client(api_session=self.api_session, region_name=region, endpoint_override=endpoint_override)
        try:
            response = mc.cluster_templates.create(
                *args, **kwargs
            )
        except Exception as e:
            raise e
        else:
            return ClusterTemplateModel.objects.create(
                id=response.uuid,
                created_at=response.created_at,
                http_proxy=response.http_proxy,
                https_proxy=response.https_proxy,
                no_proxy=response.no_proxy,
                server_type=response.server_type,
                coe=response.coe,
                image_id=response.image_id,
                public=response.public,
                registry_enabled=response.registry_enabled,
                tls_disabled=response.tls_disabled,
                keypair_id=response.keypair_id,
                flavor_id=response.flavor_id,
                master_flavor_id=response.master_flavor_id,
                volume_driver=response.volume_driver,
                docker_storage_driver=response.docker_storage_driver,
                docker_volume_size=response.docker_volume_size,
                insecure_registry=response.insecure_registry,
                network_driver=response.network_driver,
                external_network_id=response.external_network_id,
                project_id=response.project_id,
                fixed_network=response.fixed_network,
                fixed_subnet=response.fixed_subnet,
                dns_nameserver=response.dns_nameserver,
                master_lb_enabled=response.master_lb_enabled,
                floating_ip_enabled=response.floating_ip_enabled,
                labels=response.labels,
                name=response.name,
                region=region,
            )


class ClusterTemplate:
    def __init__(self, cluster_template, api_session=None):
        self.api_session = api_session
        self.cluster_template = cluster_template

    @property
    def magnum_api(self):
        assert self.api_session is not None, 'Unable to use magnum_client without a Keystoneauth session'
        region = self.cluster_template.region if len(self.cluster_template.region) else None
        endpoint_override = get_magnum_endpoint_for_region(region_id=region)
        if not endpoint_override:
            raise EndpointNotFound('Magnum endpoint not found for this region.')
        return magnum_client(api_session=self.api_session, region_name=region, endpoint_override=endpoint_override)

    def get_details_from_os(self):
        try:
            return self.magnum_api.cluster_templates.get(id=self.cluster_template.id)
        except NotFound:
            return None

    def delete(self):
        try:
            self.magnum_api.cluster_templates.delete(id=self.cluster_template.id)
        except NotFound:
            self.cluster_template.delete()
        else:
            self.cluster_template.delete()

    def update(self, *args, **kwargs):
        return self.magnum_api.cluster_templates.update(
            id=self.cluster_template.id,
            *args, **kwargs,
        )
