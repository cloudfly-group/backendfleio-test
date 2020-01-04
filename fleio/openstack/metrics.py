import logging
from gnocchiclient.exceptions import NotFound

from fleio.openstack.api.gnocchi import gnocchi_client
from fleio.openstack.api.identity import IdentityAdminApi

LOG = logging.getLogger(__name__)


class GnocchiMetrics(object):
    def __init__(self, api_session, region_name=None):
        self.gc = gnocchi_client(api_session=api_session, region_name=region_name)
        self.gca = None
        """:type : gnocchiclient.v1.client.Client"""
        self.region_name = region_name
        self.no_measures = []

    @property
    def gnocchi_admin(self):
        if self.gca is None:
            self.gca = gnocchi_client(api_session=IdentityAdminApi().session, region_name=self.region_name)
        return self.gca

    @staticmethod
    def delete_resources(project_id):
        admin_session = IdentityAdminApi().session
        gnocchi_cl = gnocchi_client(api_session=admin_session)
        try:
            resources = gnocchi_cl.resource.search(query={'=': {'project_id': project_id}})
            for resource in resources:
                try:
                    gnocchi_cl.resource.delete(resource['id'])
                except NotFound:
                    pass
        except Exception as e:
            LOG.error(e)

    def get_measures(self, resource_id, metric, granularity=None, period_start=None, period_end=None, **kwargs):
        """Get measures for a metric associated with a resource id"""
        metrics = self.gc.metric.get_measures(metric=metric,
                                              start=period_start,
                                              stop=period_end,
                                              resource_id=resource_id,
                                              granularity=granularity,
                                              **kwargs)
        return metrics

    def get_cpu_util_measures(self, resource_id, granularity=None, period_start=None, period_end=None, **kwargs):
        """Get measures for a metric associated with a resource id"""
        aggregated_metrics = self.gnocchi_admin.aggregates.fetch(
            operations='(/ (rateofchange (metric {} max)) {})'.format('cpu', granularity * 10000000),
            resource_type='instance',
            search={'=': {'id': resource_id}},
            granularity=granularity,
            start=period_start,
            stop=period_end,
            needed_overlap=0,
            fill=0,
        )
        resource_measures = aggregated_metrics['measures'].popitem()[1]
        metrics = resource_measures['cpu']['max']
        return metrics

    def get_network_interface_metrics(self, granularity, period_start, period_end, resource_id, resource_type):
        response = {}
        metrics = (('network.incoming.bytes', 'bytes_in'),
                   ('network.incoming.packets', 'packets_in'),
                   ('network.outgoing.bytes', 'bytes_out'),
                   ('network.outgoing.packets', 'packets_out'))
        result = {'date': None}
        for metric in metrics:
            # FIXME(tomo): We can't do aggregation without an admin session because the
            # current gnocchi policy rules do not allow us to. This is a bug in Gnocchi
            # server and it should be fixed. Recheck with newer versions of gnocchi.
            aggregated_metrics = self.gnocchi_admin.aggregates.fetch(
                operations='(/ (rateofchange (metric {} max)) {})'.format(metric[0], granularity),
                resource_type='instance_network_interface',
                search={'=': {'instance_id': resource_id}},
                granularity=granularity,
                start=period_start,
                stop=period_end,
                needed_overlap=0,
                fill=0,
            )
            resource_measures = aggregated_metrics['measures'].popitem()[1]
            measures_values = resource_measures[metric[0]]['max']
            response[metric[1]] = measures_values
            result[metric[1]] = [stat[2] for stat in response[metric[1]]]
            if result['date'] is None:
                result['date'] = [stat[0] for stat in response[metric[1]]]
        # FIXME(tomo): We assume the number of samples and date/times are the same for all measures
        end_result = [{'bytes_in': r[0],
                       'bytes_out': r[1],
                       'packets_in': r[2],
                       'packets_out': r[3],
                       'date': r[4]}
                      for r in zip(result['bytes_in'],
                                   result['bytes_out'],
                                   result['packets_in'],
                                   result['packets_out'],
                                   result['date'])]
        return end_result

    def get_instance_measures(self, instance, vdata):
        """
        Get the measures associated with an instance taking into account the query_parameters
        :param instance: fleio.openstack.instance.Instance
        :param vdata: OrderedDict, serializer validated data
        """
        result = None

        if vdata['metric'] == 'interface_traffic':
            # FIXME(tomo): Special case where we retrieve 4 meters at once. Try a more generic approach
            # maybe we can use groupby for metrics such that gnocchi will split the result for us.
            result = self.get_network_interface_metrics(
                resource_id=instance.uuid,
                granularity=vdata['granularity'],
                period_start=vdata['period_start'],
                period_end=vdata['period_end'],
                resource_type='instance_network_interface',
            )
        if vdata['metric'] == 'cpu_util':
            measures = self.get_cpu_util_measures(
                resource_id=instance.uuid,
                granularity=vdata['granularity'],
                period_end=vdata['period_end'],
                period_start=vdata['period_start'],
            )
            result = [{'date': m[0], 'value': m[2]} for m in measures]

        if not result:
            measures = self.get_measures(
                resource_id=instance.uuid,
                metric=vdata['metric'],
                granularity=vdata['granularity'],
                period_end=vdata['period_end'],
                period_start=vdata['period_start'],
            )
            result = [{'date': m[0], 'value': m[2]} for m in measures]

        return result
