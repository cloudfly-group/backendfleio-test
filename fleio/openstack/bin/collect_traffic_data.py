import logging
import sys
from collections import OrderedDict
from datetime import datetime
from datetime import timedelta
from math import ceil
from os import environ
from os.path import abspath
from os.path import dirname
from typing import List
from typing import Optional
from typing import Tuple

import django
from dateutil.relativedelta import relativedelta
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db import transaction
from django.db.models.functions import Coalesce
from django.utils import timezone
from gnocchiclient import exceptions as gnocchi_exceptions

current_path = dirname(abspath(__file__))
fleio_path = dirname(dirname(dirname(current_path)))

sys.path.append(fleio_path)
environ.setdefault("DJANGO_SETTINGS_MODULE", "fleio.settings")
django.setup()

from fleio.openstack.instances.instance_status import InstanceStatus  # noqa

LOG = logging.getLogger(__name__)

from django.conf import settings  # noqa

from fleio.billing.settings import CyclePeriods  # noqa
from fleio.openstack.models.network_port_traffic import NetworkPortTrafficTypes  # noqa
from fleio.openstack.api.identity import IdentityAdminApi  # noqa
from fleio.openstack.metrics import GnocchiMetrics  # noqa
from fleio.openstack.models import Instance, Project  # noqa
from fleio.openstack.models import OpenstackRegion, NetworkPortResource  # noqa
from fleio.openstack.models import Port as PortModel  # noqa
from fleio.openstack.models import NetworkPortTraffic  # noqa


os_admin_api = IdentityAdminApi()

IGNORE_UNRESOLVED_RESOURCE = True

INCOMING_BYTES_METRIC = 'network.incoming.bytes'
OUTGOING_BYTES_METRIC = 'network.outgoing.bytes'

RESOURCE_LIST_PAGE_SIZE = 100
RESOURCE_TYPE = 'instance_network_interface'

BYTES_PER_GB = 1024 * 1024 * 1024

TRAFFIC_DATA_GRANULARITY = getattr(settings, 'TRAFIC_DATA_GRANULARITY', 300)
PUBLIC_TRAFFIC_ONLY = getattr(settings, 'INSTANCE_TRAFFIC_DISPLAY', 'all') == 'public'


def discover_port(vnic_name: str, instance: Instance) -> Optional[PortModel]:
    """
    Attempts to resolve port based on vnic name and instance id.
    :param vnic_name: vnic name
    :param instance: openstack instance
    :return: found port or None if discovery failed
    """

    # TODO: investigate if notifications receive in update.d contains vnic name
    port_id_part = vnic_name[3:]
    for port in instance.ports:  # type: PortModel
        if port.id.startswith(port_id_part):
            return port


def update_db_resource(resource: dict, region: OpenstackRegion) -> Optional[NetworkPortResource]:
    with transaction.atomic():
        db_instance = Instance.objects.filter(id=resource['instance_id']).first()  # type: Instance

        if IGNORE_UNRESOLVED_RESOURCE and not db_instance:
            # ignore unresolved resources
            return None

        db_port = discover_port(vnic_name=resource['name'], instance=db_instance) if db_instance else None

        if IGNORE_UNRESOLVED_RESOURCE and not db_port:
            return None

        db_resource = NetworkPortResource.objects.filter(resource_id=resource['id']).first()
        if not db_resource:
            try:
                project_id = db_instance.project.project_id
            except Project.DoesNotExist:
                project_id = None

            db_resource = NetworkPortResource.objects.create(
                resource_id=resource['id'],
                vnic_name=resource['name'],
                instance_id=resource['instance_id'],
                region=region,
                port=db_port,
                existing_instance=db_instance,
                project_id=project_id,
                found_port_id=db_port.id if db_port else None,
                is_private=db_port.is_private() if db_port else False,
            )

        return db_resource


def sync_resources_for_region(region: OpenstackRegion):
    gnocchi_metrics = GnocchiMetrics(api_session=os_admin_api.session, region_name=region.id)

    try:
        marker = None
        while True:
            resources = gnocchi_metrics.gc.resource.list(
                resource_type=RESOURCE_TYPE,
                limit=RESOURCE_LIST_PAGE_SIZE,
                marker=marker
            )

            for resource in resources:
                update_db_resource(resource=resource, region=region)

            if len(resources) < RESOURCE_LIST_PAGE_SIZE:
                break
            else:
                marker = resources[len(resources) - 1]['id']
    except Exception as e:
        del e  # we ignore all exceptions here


def sync_resources():
    for region in OpenstackRegion.objects.all():
        sync_resources_for_region(region=region)


def get_billing_cycle(
        network_port_resource: NetworkPortResource, timestamp: datetime,
) -> Optional[Tuple[datetime, datetime]]:
    try:
        project = Project.objects.filter(project_id=network_port_resource.project_id).first()
        if project and project.service:
            service = project.service
            if service.cycle and service.cycle.cycle in [CyclePeriods.month, CyclePeriods.year]:
                next_due_date = service.next_due_date
                if not next_due_date:
                    next_due_date = service.get_next_due_date(previous_due_date=service.created_at)
                    service.next_due_date = next_due_date

                while next_due_date <= timestamp:
                    next_due_date = service.get_next_due_date(previous_due_date=next_due_date)
                    service.next_due_date = next_due_date

                previous_due_date = service.get_previous_due_date()

                while not (previous_due_date <= timestamp and timestamp <= service.next_due_date):
                    service.next_due_date = previous_due_date
                    previous_due_date = service.get_previous_due_date()

                return previous_due_date, service.next_due_date

    except ObjectDoesNotExist:
        # project or service may be deleted, in this case we will return no cycle
        pass

    return None


def get_month(timestamp: datetime) -> Tuple[datetime, datetime]:
    start = datetime(
        year=timestamp.year, month=timestamp.month, day=1,
        hour=0, minute=0, second=0,
        tzinfo=timezone.utc,
    )

    end = start + relativedelta(months=1) - timedelta(seconds=1)
    return start, end


def get_db_port_traffic(
        traffic_type: str,
        period: Tuple[datetime, datetime],
        old_port_traffic: Optional[NetworkPortTraffic],
        db_resource: NetworkPortResource,
        save_old_traffic_on_change: bool = True,
) -> Optional[NetworkPortTraffic]:
    if old_port_traffic:
        if old_port_traffic.start_datetime == period[0] and old_port_traffic.end_datetime == period[1]:
            return old_port_traffic
        else:
            if save_old_traffic_on_change:
                old_port_traffic.save()

    db_port_traffic = NetworkPortTraffic.objects.filter(
        resource=db_resource, type=traffic_type, start_datetime=period[0], end_datetime=period[1],
    ).first()

    if not db_port_traffic:
        db_port_traffic = NetworkPortTraffic.objects.create(
            type=traffic_type,
            start_datetime=period[0],
            end_datetime=period[1],
            resource=db_resource,
        )
        db_port_traffic.init_from_previous()

    return db_port_traffic


def update_network_traffic(db_resource, found_measures_dict):
    last_check_date = timezone.utc.localize(datetime.min)
    month_traffic = None
    cycle_traffic = None
    billing_cycle = None
    for timestamp in found_measures_dict:
        measures = found_measures_dict[timestamp]
        last_check_date = max(last_check_date, timestamp)

        # TODO: see what happens when month and billing_cycle are exactly the same
        month = get_month(timestamp=timestamp)
        if not (billing_cycle and billing_cycle[0] <= timestamp and timestamp < billing_cycle[1]):
            billing_cycle = get_billing_cycle(
                network_port_resource=db_resource,
                timestamp=timestamp,
            )

        month_traffic = get_db_port_traffic(
            traffic_type=NetworkPortTrafficTypes.per_month,
            period=month, old_port_traffic=month_traffic,
            db_resource=db_resource,
        )
        month_traffic.add_measures(new_measures=measures)

        if billing_cycle:
            cycle_traffic = get_db_port_traffic(
                traffic_type=NetworkPortTrafficTypes.per_billing_cycle,
                period=billing_cycle, old_port_traffic=cycle_traffic,
                db_resource=db_resource,
            )
            cycle_traffic.add_measures(new_measures=measures)

    if month_traffic:
        month_traffic.save()
    if cycle_traffic:
        cycle_traffic.save()
    db_resource.last_check = last_check_date
    db_resource.save()


def merge_measures(existing_measures: dict, new_measures: List, key: str):
    for measure in new_measures:
        if not measure[0] in existing_measures:
            existing_measures[measure[0]] = {
                key: measure[2],
            }
        else:
            existing_measures[measure[0]][key] = measure[2]


def collect_traffic_for_resource(db_resource, gnocchi_metrics):
    period_stop = timezone.utc.localize(datetime.utcnow())
    period_start = period_stop - timedelta(days=32)
    if db_resource.last_check and period_start < db_resource.last_check:
        period_start = db_resource.last_check

    try:
        found_measures = {}
        # get incoming measures
        incoming_measures = gnocchi_metrics.gc.metric.get_measures(
            metric=INCOMING_BYTES_METRIC,
            resource_type=RESOURCE_TYPE,
            aggregation='max',
            granularity=TRAFFIC_DATA_GRANULARITY,
            resource_id=db_resource.resource_id,
            start=period_start,
            stop=period_stop,
        )

        merge_measures(existing_measures=found_measures, new_measures=incoming_measures, key='bytes_in')

        # get outgoing measures
        outgoing_measures = gnocchi_metrics.gc.metric.get_measures(
            metric=OUTGOING_BYTES_METRIC,
            resource_type=RESOURCE_TYPE,
            aggregation='max',
            granularity=TRAFFIC_DATA_GRANULARITY,
            resource_id=db_resource.resource_id,
            start=period_start,
            stop=period_stop,
        )

        merge_measures(existing_measures=found_measures, new_measures=outgoing_measures, key='bytes_out')
    except gnocchi_exceptions.NotFound:
        # TODO: more detailed logs here
        LOG.debug('Metric not found')
    else:
        if len(found_measures):
            sorted_measures = OrderedDict()
            measures_keys = sorted(found_measures.keys())
            for key in measures_keys:
                sorted_measures[key] = found_measures[key]

            update_network_traffic(db_resource, sorted_measures)


def collect_traffic_for_region(region: OpenstackRegion):
    gnocchi_metrics = GnocchiMetrics(api_session=os_admin_api.session, region_name=region.id)
    for db_resource in NetworkPortResource.objects.filter(
        region=region,
        found_port_id__isnull=not IGNORE_UNRESOLVED_RESOURCE,
    ):  # type: NetworkPortResource
        collect_traffic_for_resource(db_resource, gnocchi_metrics)


def collect_traffic():
    for region in OpenstackRegion.objects.all():
        collect_traffic_for_region(region=region)


def update_instances_traffic():
    # TODO: this function should be optimized, the for can be replaced with a single query
    current_date = datetime.utcnow().replace(tzinfo=timezone.utc)
    port_traffic_query = NetworkPortTraffic.objects.all()
    if PUBLIC_TRAFFIC_ONLY:
        port_traffic_query = port_traffic_query.filter(resource__is_private=False)
    for instance in Instance.objects.exclude(status__in=[InstanceStatus.DELETED, InstanceStatus.ERROR]).all():
        cycle_traffic = port_traffic_query.filter(
            resource__instance_id=instance.id,
            start_datetime__lt=current_date,
            end_datetime__gt=current_date,
            type=NetworkPortTrafficTypes.per_billing_cycle,
        ).aggregate(
            incoming_bytes_sum=Coalesce(models.Sum('incoming_bytes'), models.Value(0)),
            outgoing_bytes_sum=Coalesce(models.Sum('outgoing_bytes'), models.Value(0)),
        )
        month_traffic = port_traffic_query.filter(
            resource__instance_id=instance.id,
            start_datetime__lt=current_date,
            end_datetime__gt=current_date,
            type=NetworkPortTrafficTypes.per_month
        ).aggregate(
            incoming_bytes_sum=Coalesce(models.Sum('incoming_bytes'), models.Value(0)),
            outgoing_bytes_sum=Coalesce(models.Sum('outgoing_bytes'), models.Value(0)),
        )
        instance.current_cycle_traffic = cycle_traffic['incoming_bytes_sum'] + cycle_traffic['outgoing_bytes_sum']
        instance.current_cycle_traffic = ceil(instance.current_cycle_traffic / BYTES_PER_GB)
        instance.current_month_traffic = month_traffic['incoming_bytes_sum'] + month_traffic['outgoing_bytes_sum']
        instance.current_month_traffic = ceil(instance.current_month_traffic / BYTES_PER_GB)
        instance.save(update_fields=['current_cycle_traffic', 'current_month_traffic'])


def run():
    sync_resources()
    collect_traffic()
    update_instances_traffic()


if __name__ == '__main__':
    run()
