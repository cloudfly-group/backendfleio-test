from __future__ import unicode_literals

import logging

from ..models import ResourceUsageLog
from ..models import BillingResource
from .generic import GenericCollector
from .event import Event, RawEvent

LOG = logging.getLogger(__name__)


class GlanceCollector(GenericCollector):
    def __init__(self):
        super(GlanceCollector, self).__init__()
        self.resource_type = 'image'
        self.query_events = ['image.activate', 'image.delete', 'image.exists']

    def store_event(self, event, region=None):
        # Overwrite trait conversion
        overwrite_mappings = {'created_at': 'datetime', 'deleted_at': 'datetime', 'size': 'integer'}
        event = Event(event, overwrite_mappings)
        # Get project_id from traits.project_id or if missing, from traits.tenant_id if present
        project_id = getattr(event.trait, 'project_id', None) or getattr(event.trait, 'tenant_id', None)
        # Get launched_at from traits.launched_at or if missing, from traits.created_at if present
        started_at = getattr(event.trait, 'launched_at', None) or getattr(event.trait, 'created_at', None)
        user_id = getattr(event.trait, 'user_id', None)
        resource_id = getattr(event.trait, 'instance_id', None) or getattr(event.trait, 'resource_id', None)
        ended_at = getattr(event.trait, 'deleted_at', None)
        message_id = getattr(event, 'message_id', 'n/a')

        # NOTE(tomo): Deleting an image may not include the deleted_at trait
        if event.event_type == 'image.delete' and ended_at is None:
            ended_at = event.generated

        if started_at is None or resource_id is None:
            LOG.debug('Ignored event: %s without "started_at" or "resource_id"' % message_id)
            return

        return ResourceUsageLog.objects.add_event(resource_type=self.resource_type,
                                                  resource_uuid=resource_id,
                                                  start=started_at,
                                                  project_id=project_id,
                                                  user_id=user_id,
                                                  end=ended_at,
                                                  region=region,
                                                  traits=event.traits)

    def store_message_event(self, event_type, payload, metadata, region=None):
        """Store one event in db"""
        # Get the resource if available, else return
        try:
            resource = BillingResource.objects.get(name=self.resource_type, type='service')
        except BillingResource.DoesNotExist:
            LOG.info('Skip event processing for missing "{}" resource definition'.format(self.resource_type))
            return
        attributes = resource.definition.get('attributes', list())
        # Overwrite trait conversion
        required_traits = {'created_at': 'datetime', 'deleted_at': 'datetime', 'size': 'integer',
                           'display_name': 'string', 'owner': 'string', 'id': 'string', 'instance_type': 'string',
                           'name': 'string'}
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
        project_id = getattr(event.trait, 'owner', None)
        started_at = getattr(event.trait, 'created_at', None)
        try:
            event.traits.append({'name': 'user_id', 'type': 'string', 'value': payload['properties']['user_id']})
            user_id = getattr(event.trait, 'user_id', None)
        except KeyError:
            user_id = getattr(event.trait, 'owner', None)
        resource_id = getattr(event.trait, 'id', None)
        ended_at = getattr(event.trait, 'deleted_at', None)
        message_id = event.message_id

        # NOTE(tomo): Deleting an image may not include the deleted_at trait
        if event_type == 'image.delete' and ended_at is None:
            ended_at = event.generated

        if started_at is None or resource_id is None:
            LOG.debug('Ignored event: %s without "started_at" or "resource_id"' % message_id)
            return

        return ResourceUsageLog.objects.add_event(resource_type=self.resource_type,
                                                  resource_uuid=resource_id,
                                                  start=started_at,
                                                  project_id=project_id,
                                                  user_id=user_id,
                                                  end=ended_at,
                                                  region=region,
                                                  traits=event.traits)
