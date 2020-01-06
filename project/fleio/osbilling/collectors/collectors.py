from __future__ import unicode_literals

import logging
import datetime
from django.utils.timezone import now as utcnow

from fleio.openstack.api.identity import IdentityAdminApi

from ..exceptions import CollectorException
from .compute import NovaCollector
from .glance import GlanceCollector
from .cinder import CinderCollector

LOG = logging.getLogger(__name__)


class EventsCollector(object):
    """Gather all collectors and collect the events"""
    COLLECTOR_CLASSES = (CinderCollector, NovaCollector, GlanceCollector)

    def __init__(self):
        self.collector_instances = [ccls() for ccls in self.COLLECTOR_CLASSES]
        self.init_days_collect = 30  # How many days to go back to on first collection
        self.default_last_collected = utcnow().replace(microsecond=0) - datetime.timedelta(days=self.init_days_collect)

    def collect(self, project_id, region_name):
        api_session = IdentityAdminApi().session
        for collector in self.collector_instances:
            end_date = utcnow().replace(microsecond=0)
            last_collected = end_date - datetime.timedelta(days=31)
            try:
                collector.collect_events(start_date=last_collected,
                                         end_date=end_date,
                                         api_session=api_session,
                                         region_name=region_name,
                                         project_id=project_id)
            except CollectorException as e:
                LOG.error(e)
                continue
