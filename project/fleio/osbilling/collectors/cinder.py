from __future__ import unicode_literals

import logging

from ..models import ResourceUsageLog
from ..models import BillingResource
from .generic import GenericCollector
from .event import Event, RawEvent

LOG = logging.getLogger(__name__)


class CinderCollector(GenericCollector):
    def __init__(self):
        super(CinderCollector, self).__init__()
        self.resource_type = 'volume'
        self.query_events = ['volume.create.end',
                             'volume.delete.end',
                             'volume.resize.end',
                             ]

    def store_event(self, event, region=None):
        """Store one event in db"""

        event = Event(event)

        project_id = getattr(event.trait, 'project_id', None) or getattr(event.trait, 'tenant_id', None)
        started_at = getattr(event.trait, 'created_at', None)
        user_id = getattr(event.trait, 'user_id', None)
        # resource id == the volume which this event belongs to
        resource_id = getattr(event.trait, 'resource_id', None)
        ended_at = getattr(event.trait, 'deleted_at', None)
        message_id = getattr(event, 'message_id', 'n/a')

        if event.event_type == 'volume.delete.end' and ended_at is None:
            ended_at = event.generated
        elif event.event_type == 'volume.resize.end':
            started_at = event.generated
        if started_at is None or resource_id is None:
            # We ignore events without a resource start date or without an identifier (volume id)
            LOG.debug('Ignored event: {} without started_at'.format(message_id))
            return

        if event.event_type.startswith('volume.resize.'):
            # a rare scenario, but if it does happen, some clients tickets will be avoided :)
            if not ResourceUsageLog.objects.filter(resource_type=self.resource_type,
                                                   resource_uuid=resource_id).exists():
                # TODO(Marius): if indeed this does happen, find a way to get whatever happened before this event
                # for the past 365 days, using 'volume.exists' as the event type
                logging.info('Your db is out of sync, there are events created in OpenStack but missing from '
                             'your db: you are trying to record an event of type {} but no '
                             'parent of this record is stored in db (the initial [created] one '
                             'is missing)'.format(event.event_type))

        return ResourceUsageLog.objects.add_event(resource_type=self.resource_type,
                                                  resource_uuid=resource_id,
                                                  start=started_at,
                                                  project_id=project_id,
                                                  user_id=user_id,
                                                  end=ended_at,
                                                  region=region,
                                                  traits=event.traits)

    def store_message_event(self, event_type, payload, metadata, region=None):
        """Called from updated"""

        # Get the resource if available, else return
        try:
            resource = BillingResource.objects.get(name=self.resource_type, type='service')
        except BillingResource.DoesNotExist:
            LOG.info('Skip event processing for missing "{}" resource definition'.format(self.resource_type))
            return
        attributes = resource.definition.get('attributes', list())
        required_traits = {'user_id': 'string', 'tenant_id': 'string', 'project_id': 'string', 'volume_id': 'string',
                           'display_name': 'string', 'launched_at': 'datetime', 'created_at': 'datetime',
                           'deleted_at': 'datetime', 'size': 'integer'}
        keep_traits = list(required_traits)  # TODO(tomo): py2to3 list(keys())
        overwrite_mappings = required_traits
        for attribute in attributes:
            name = attribute.get('name', None)
            value_type = attribute.get('type', None)
            if name:
                keep_traits.append(name)
                if value_type:
                    overwrite_mappings[name] = value_type
        event = RawEvent(event_type=event_type,
                         payload=payload,
                         metadata=metadata,
                         keep_traits=keep_traits,
                         overwrite_mappings=overwrite_mappings,
                         region=region)
        project_id = getattr(event.trait, 'tenant_id', None) or getattr(event.trait, 'project_id', None)
        started_at = getattr(event.trait, 'created_at', None)
        user_id = getattr(event.trait, 'user_id', None)
        resource_id = getattr(event.trait, 'volume_id', None)
        ended_at = getattr(event.trait, 'deleted_at', None)
        message_id = event.message_id

        if event.event_type == 'volume.delete.end':
            ended_at = event.generated
        elif event.event_type == 'volume.resize.end':
            started_at = event.generated
        if started_at is None or resource_id is None:
            LOG.debug('Ignored event: {} without "started_at" or "resource_id"'.format(message_id))
            return

        if event.event_type.startswith('volume.resize.'):
            # TODO(Marius): see store_event method for verbosity
            # also use a better approach at using a new procedure to avoid duplicate code
            if not ResourceUsageLog.objects.filter(resource_type=self.resource_type,
                                                   resource_uuid=resource_id).exists():
                logging.info('Your db is out of sync, there are events created in OpenStack but missing from '
                             'your db: you are trying to record an event of type {} but no '
                             'parent of this record is stored in db (the initial [created] one '
                             'is missing)'.format(event.event_type))

        return ResourceUsageLog.objects.add_event(resource_type=self.resource_type,
                                                  resource_uuid=resource_id,
                                                  start=started_at,
                                                  project_id=project_id,
                                                  user_id=user_id,
                                                  end=ended_at,
                                                  region=region,
                                                  traits=event.traits)
