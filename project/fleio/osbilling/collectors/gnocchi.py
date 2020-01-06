from __future__ import unicode_literals

from fleio.openstack.api.identity import IdentityAdminApi
from fleio.openstack.metrics import GnocchiMetrics


class MetricRegistry(object):
    def __init__(self):
        self.metrics = dict(instance=list(), volume=list(), image=list())

    def metric(self, resource, value_type=None, unit=None, description='Units'):
        """Used to mark a method on a class as a metric"""
        value_type = 'float' if (value_type is None) else value_type
        unit = 'u' if (unit is None) else unit

        def decorator(func):
            metric_func = dict(name=func.__name__, value_type=value_type, unit=unit, description=description)
            self.metrics[resource].append(metric_func)
            return func
        return decorator


class GnocchiCollector:
    reg = MetricRegistry()

    def __init__(self, region_name=None):
        self.region_name = region_name
        self.admin_session = IdentityAdminApi()
        self.metrics = self.reg.metrics

    @property
    def gnocchi_metrics(self):
        return GnocchiMetrics(api_session=self.admin_session.session, region_name=self.region_name)

    @property
    def gnocchi_client(self):
        return self.gnocchi_metrics.gc

    def has_metric(self, resource, name):
        for m in self.metrics.get(resource, list()):
            if m['name'] == name:
                return True
        return False

    def get_metric(self, resource, name):
        for m in self.metrics.get(resource, list()):
            if m['name'] == name:
                return m

    def get_interfaces_for_instance(self, instance_id):
        """Retrieve instance_network_interface resource for an instance"""
        return self.gnocchi_client.resource.search(resource_type='instance_network_interface',
                                                   query={'=': {'instance_id': instance_id}},
                                                   details=True)

    @staticmethod
    def get_measures_sum(measures):
        result = float(0)
        for measure in measures:
            result += measure[2]
        return result

    def instance_traffic(self, resource_id, start, end, granularity=300, metric='network.incoming.bytes.rate'):
        # FIXME(tomo): Get the nic associated with a network tagged as fleio_public or fleio_private
        interface_resources = self.get_interfaces_for_instance(instance_id=resource_id)
        if interface_resources:
            first_resource = interface_resources[1]
            metric_id = first_resource['metrics'].get(metric, None)
            if metric_id:
                measures = self.gnocchi_client.metric.get_measures(metric=metric_id,
                                                                   granularity=granularity,
                                                                   aggregation='sum',
                                                                   start=start,
                                                                   end=end)
                return self.get_measures_sum(measures)
        return float(0)

    @reg.metric(resource='instance', unit='b', description='Bytes')
    def instance_total_traffic(self, resource_id, start, end, granularity=300):
        incoming = self.instance_traffic(resource_id, start, end, granularity)
        outgoing = self.instance_traffic(resource_id, start, end, granularity)
        return incoming + outgoing

    @reg.metric(resource='instance', unit='b', description='Bytes')
    def instance_outgoing_traffic(self, resource_id, start, end, granularity=300):
        return self.instance_traffic(resource_id, start, end, granularity)

    @reg.metric(resource='instance', unit='b', description='Bytes')
    def instance_incoming_traffic(self, resource_id, start, end, granularity=300):
        return self.instance_traffic(resource_id, start, end, granularity)
