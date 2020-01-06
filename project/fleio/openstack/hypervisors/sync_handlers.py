import logging

from fleio.openstack.hypervisors.serializers import HypervisorSyncSerializer
from fleio.openstack.sync.handler import BaseHandler

LOG = logging.getLogger(__name__)


class HypervisorSyncHandler(BaseHandler):
    serializer_class = HypervisorSyncSerializer
    version_field = 'sync_version'

    def serialize(self, data, region, timestamp):
        hypervisor = data.to_dict()
        if data.service:
            host_name = data.service.get('host', None)
            if host_name:
                hypervisor['host_name'] = host_name

        hypervisor['region'] = region
        hypervisor[self.version_field] = self.get_version(timestamp)

        return hypervisor
