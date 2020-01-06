from fleio.openstack.api.identity import IdentityAdminApi
from fleio.openstack.models import Cluster
from fleio.openstack.sync.handler import BaseHandler
from fleio.openstack.container_infra.clusters import serializers
from fleio.openstack.tasks import sync_clusters_in_background


class ClusterHandler(BaseHandler):
    def serialize(self, data, region, timestamp):
        pass

    serializer_class = serializers.ClusterUpdatedSerializer
    model_class = Cluster

    def __init__(self, api_session=None):
        self.api_session = api_session or IdentityAdminApi().session
        self.event_handlers = {
            'magnum.cluster.create': self.create_or_update,
            'magnum.cluster.delete': self.create_or_update,
            'magnum.cluster.update': self.create_or_update,
        }
        self.error_handlers = {
            'magnum.cluster.create': self.create_or_update,
            'magnum.cluster.delete': self.create_or_update,
            'magnum.cluster.update': self.create_or_update,
        }

    def create_or_update(self, data, region, timestamp):
        initiator = data.get('initiator')
        project_id = None
        if initiator:
            project_id = initiator.get('project_id')
        sync_clusters_in_background.delay(project_id=project_id, region=region)
