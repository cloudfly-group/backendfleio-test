import json
import logging

from django.utils.timezone import now as utcnow

from novaclient.exceptions import NotFound

from fleio.core.operations_base.operation_base import OperationBase
from fleio.openstack.api.identity import IdentityAdminApi
from fleio.openstack.api.nova import nova_client

from fleio.osbilling.models import ResourceUsageLog


AUTH_CACHE = dict()

LOG = logging.getLogger(__name__)


class InstanceDeletion(OperationBase):
    name = 'instance_deletion'

    def run(self, *args, **kwargs):
        operation_params = json.loads(self.db_operation.params)
        region = operation_params.get('region')
        if not region:
            return self.abort_operation()
        nc = nova_client(api_session=IdentityAdminApi(request_session=AUTH_CACHE).session, region_name=region)
        try:
            instance = nc.servers.get(server={'id': self.db_operation.primary_object_id})
        except (Exception, NotFound):
            instance = None
        if not instance:
            resource_usage_log = ResourceUsageLog.objects.filter(
                resource_uuid=self.db_operation.primary_object_id
            ).order_by('start').last()
            if not resource_usage_log:
                return self.abort_operation()
            if not resource_usage_log.end:
                timestamp = utcnow().isoformat()
                LOG.info('Instance delete operation successfully set the resource usage log end date')
                resource_usage_log.end = timestamp
                resource_usage_log.save()
                return self.mark_as_completed()
            else:
                LOG.info('Instance related resource usage log was already ended by OS messages')
                return self.mark_as_completed()
