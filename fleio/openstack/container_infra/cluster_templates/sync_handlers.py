import logging
import json

from fleio.openstack.container_infra.cluster_templates import serializers
from fleio.openstack.sync.handler import BaseHandler


LOG = logging.getLogger(__name__)


class ClusterTemplateSyncHandler(BaseHandler):
    serializer_class = serializers.ClusterTemplateSyncSerializer
    version_field = 'sync_version'

    def serialize(self, data, region, timestamp):
        cluster_template = data.to_dict()
        cluster_template[self.version_field] = self.get_version(timestamp)
        cluster_template['id'] = cluster_template.get('uuid')
        cluster_template['region'] = region
        cluster_template['labels'] = json.dumps(cluster_template.get('labels', {}))
        cluster_template['project'] = cluster_template.get('project_id')
        return cluster_template
