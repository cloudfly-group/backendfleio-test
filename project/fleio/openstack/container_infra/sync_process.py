import logging

from magnumclient.common.apiclient.exceptions import EndpointNotFound as MagnumEndpointNotFound

from django.utils.timezone import now as utcnow

from fleio.openstack.api import identity
from fleio.openstack.api.magnum import magnum_client
from fleio.openstack.container_infra.cluster_templates.sync_handlers import ClusterTemplateSyncHandler
from fleio.openstack.container_infra.clusters.sync_handlers import ClusterSyncHandler
from fleio.openstack.container_infra.endpoint import get_magnum_endpoint_for_region


LOG = logging.getLogger(__name__)


def sync_coe(region_id, auth_cache=None, project_id=None):
    timestamp = utcnow().isoformat()
    endpoint_override = get_magnum_endpoint_for_region(region_id=region_id)
    if endpoint_override:
        if project_id:
            api_session = identity.IdentityUserApi(project_id=project_id).session
        else:
            api_session = identity.IdentityAdminApi(request_session=auth_cache).session
        try:
            mc = magnum_client(
                api_session=api_session,
                region_name=region_id,
                endpoint_override=endpoint_override
            )
        except MagnumEndpointNotFound:
            pass
        else:
            try:
                list_limit = 50
                # sync cluster templates
                has_more = True
                marker = None
                cth = ClusterTemplateSyncHandler()
                while has_more:
                    cluster_templates = mc.cluster_templates.list(limit=list_limit, marker=marker)
                    if not cluster_templates:
                        break
                    cluster_templates_count = 0
                    for cluster_template in cluster_templates:
                        cth.create_or_update(cluster_template, region=region_id, timestamp=timestamp)
                        marker = cluster_template.uuid
                        cluster_templates_count += 1
                    has_more = cluster_templates_count == list_limit
                version = cth.get_version(timestamp)
                delete_filter = {'{}__lt'.format(cth.version_field): version, 'region': region_id}
                if project_id:
                    delete_filter['project__project_id'] = project_id
                cth.model_class.objects.filter(**delete_filter).delete()
                # sync clusters
                has_more = True
                marker = None
                ch = ClusterSyncHandler()
                while has_more:
                    clusters = mc.clusters.list(detail=True, limit=list_limit, marker=marker)
                    if not clusters:
                        break
                    clusters_count = 0
                    for cluster in clusters:
                        ch.create_or_update(cluster, region=region_id, timestamp=timestamp)
                        marker = cluster.uuid
                        clusters_count += 1
                    has_more = clusters_count == list_limit
                version = ch.get_version(timestamp)
                delete_filter = {'{}__lt'.format(ch.version_field): version, 'region': region_id}
                if project_id:
                    delete_filter['project__project_id'] = project_id
                ch.model_class.objects.filter(**delete_filter).delete()
            except Exception as e:
                LOG.error(str(e))
                return
