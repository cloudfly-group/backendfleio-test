import logging
import json

from fleio.openstack.container_infra.clusters import serializers
from fleio.openstack.sync.handler import BaseHandler


LOG = logging.getLogger(__name__)


class ClusterSyncHandler(BaseHandler):
    serializer_class = serializers.ClusterSyncSerializer
    version_field = 'sync_version'

    def serialize(self, data, region, timestamp):
        cluster = data.to_dict()
        cluster[self.version_field] = self.get_version(timestamp)
        cluster['id'] = cluster.get('uuid')
        cluster['labels'] = json.dumps(cluster.get('labels', {}))
        cluster['cluster_template'] = cluster.get('cluster_template_id')
        cluster['region'] = region
        cluster['project'] = cluster.get('project_id')
        node_addr_as_list = cluster.get('node_addresses')
        if node_addr_as_list:
            cluster['node_addresses'] = str(node_addr_as_list)
        else:
            cluster['node_addresses'] = None
        master_addr_as_list = cluster.get('master_addresses')
        if master_addr_as_list:
            cluster['master_addresses'] = str(master_addr_as_list)
        else:
            cluster['master_addresses'] = None
        return cluster
