from __future__ import unicode_literals

import logging

from ceilometerclient.client import Client as CeiloClient
from ceilometerclient.client import exceptions as ceilo_exceptions
from django.utils.translation import ugettext_lazy as _

from fleio.openstack.settings import plugin_settings
from fleio.osbilling.exceptions import CollectorException

LOG = logging.getLogger(__name__)


class GenericCollector(object):
    def __init__(self):
        self.query_events = list()
        self.resource_type = 'generic'

    def get_raw_events(self, start_date, end_date, api_session, region_name, project_id=None):
        """
        Get the events from Ceilometer.
        Note: As of OpenStack Liberty this is no longer working
                without an OpenStack patch from us.
        """
        # Get the ceilometer client
        try:
            c = CeiloClient(version=plugin_settings.METERING_API_VERSION,
                            interface='public',
                            session=api_session,
                            region_name=region_name)
        except Exception as e:
            msg = _('Unable to initialize the ceilometer client')
            LOG.error('{}: {}'.format(msg, e))
            raise CollectorException(msg)
        # Create the api queries and retrieve the events
        raw_events = list()
        sts = {'field': 'start_timestamp', 'value': start_date, 'type': 'datetime'}
        ets = {'field': 'end_timestamp', 'value': end_date, 'type': 'datetime'}
        # TODO(tomo): Optimize when support for complex queries is available in ceilometer
        for event in self.query_events:
            q = [{'field': 'event_type', 'value': event}, sts, ets]
            if project_id:
                q.append({'field': 'project_id', 'value': project_id})
            try:
                raw_events.append(c.events.list(q=q))
            except ceilo_exceptions.ClientException as e:
                msg = _('Unable to retrieve events')
                LOG.error('{}: {}'.format(msg, e))
                raise CollectorException(msg)

        return raw_events

    def store_event(self, event, region=None):
        """Store an event"""
        raise NotImplementedError()

    def store_message_event(self, event_type, payload, metadata, region=None):
        """Store an event from messaging server"""
        raise NotImplementedError()

    def collect_events(self, start_date, end_date, api_session, region_name, project_id=None):
        ceilo_events = self.get_raw_events(start_date, end_date, api_session, region_name, project_id=project_id)
        for evs in ceilo_events:
            for ev in evs:
                self.store_event(ev, region=region_name)
