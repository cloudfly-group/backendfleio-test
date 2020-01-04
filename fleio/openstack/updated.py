import logging
import json
import oslo_messaging
from django import db
from django.conf import settings
from django.db import IntegrityError
from oslo_config import cfg

# noinspection PyCompatibility,PyUnresolvedReferences
from six.moves.queue import Queue

from django.utils.timezone import now as utcnow

from fleio.core.models import AppStatus
from fleio.core.models.appstatus import StatusTypesMap
from fleio.openstack.models import OpenstackRegion
from fleio.openstack.settings import plugin_settings
from fleio.openstack.signals.signals import openstack_error
from fleio.openstack.container_infra.clusters.notification_handler import ClusterHandler
from fleio.osbilling.collectors.cinder import CinderCollector
from fleio.osbilling.collectors.glance import GlanceCollector
from fleio.osbilling.collectors.compute import NovaCollector
from fleio.openstack.instances.event_handlers import InstanceEventHandler
from fleio.openstack.volume_backups.notification_handler import VolumeBackupHandler
from fleio.openstack.volume_snapshots.notification_handler import VolumeSnapshotHandler
from fleio.openstack.volumes.notification_handler import QoSSpecHandler
from fleio.openstack.volumes.notification_handler import VolumeHandler
from fleio.openstack.volumes.notification_handler import VolumeTypeExtraSpecHandler
from fleio.openstack.volumes.notification_handler import VolumeTypeHandler

from fleio.openstack.projects.event_handlers import ProjectEventHandler  # noqa

from fleio.openstack.networking.event_handlers import PortEventHandler
from fleio.openstack.networking.event_handlers import NetworkEventHandler
from fleio.openstack.networking.event_handlers import NetworkRbacEventHandler
from fleio.openstack.networking.event_handlers import SubnetEventHandler
from fleio.openstack.networking.event_handlers import SubnetPoolEventHandler
from fleio.openstack.networking.event_handlers import FloatingIPEventHandler
from fleio.openstack.networking.event_handlers import RouterEventHandler
from fleio.openstack.networking.event_handlers import SecurityGroupRuleEventHandler
from fleio.openstack.networking.event_handlers import SecurityGroupEventHandler
from fleio.openstack.images.event_handlers import ImageEventHandler
from fleio.openstack.images.event_handlers import ImageMemberEventHandler

LOG = logging.getLogger(__name__)

EXECUTOR = str('threading')

p_queue = Queue()


event_handler_classes = [
    ClusterHandler,
    FloatingIPEventHandler,
    ImageEventHandler,
    ImageMemberEventHandler,
    InstanceEventHandler,
    NetworkEventHandler,
    NetworkRbacEventHandler,
    PortEventHandler,
    ProjectEventHandler,
    QoSSpecHandler,
    RouterEventHandler,
    SecurityGroupEventHandler,
    SecurityGroupRuleEventHandler,
    SubnetEventHandler,
    SubnetPoolEventHandler,
    VolumeHandler,
    VolumeBackupHandler,
    VolumeSnapshotHandler,
    VolumeTypeHandler,
    VolumeTypeExtraSpecHandler,
]


EVH = []  # NOTE(tomo): Keeps initialized event handlers global


def event_handlers(evh):
    if not evh:
        for handler in event_handler_classes:
            evh.append(handler())
    return evh


def db_wrap(to_call):
    try:
        return to_call()
    except db.utils.OperationalError:
        db.connection.close()
        return to_call()


def sum_updated_messages(new_count: int, last_updated):
    """Updates the updated received messages counter"""
    app_info = AppStatus.objects.filter(status_type=StatusTypesMap.updated_messages_count).first()
    if app_info:
        old_details = app_info.details_as_dict
        new_details = dict(updated_messages_count=old_details['updated_messages_count'] + new_count)
        app_info.details = json.dumps(new_details)
        app_info.last_updated = last_updated
        app_info.save()
    else:
        AppStatus.objects.create(
            status_type=StatusTypesMap.updated_messages_count,
            last_updated=last_updated,
            details=json.dumps(dict(updated_messages_count=1))
        )


def _get_os_resource_id_from_payload(payload):
    possible_ids = ('id', 'uuid', 'instance_id', 'volume_id', 'image_id', 'network_id', 'snapshot_id', 'flavor_id',
                    'cluster_id', 'router_id', 'security_group_id', 'floatingip_id', 'subnetpool_id', 'subnet_id',
                    'port_id', 'backup_id', 'resource_info', 'qos_specs_id', 'volume_type_id', )
    for possible_id in possible_ids:
        found_id = payload.get(possible_id, None)
        if found_id:
            return found_id
    return 'Could not determine resource id'


def handle_queued_events():
    """Runs from a thread and processes events as soon as they are available"""
    messages = 0
    last_count = utcnow()
    while True:
        event_data = p_queue.get()

        # count received messages but with a delay of 5s
        now = utcnow()
        messages = messages + 1
        delta = now - last_count
        delta = delta.total_seconds()
        if delta > 5:
            last_count = now
            sum_updated_messages(new_count=messages, last_updated=last_count)
            messages = 0

        logging_keywords = getattr(settings, 'OPENSTACK_EVENT_NOTIFICATIONS_LOGGING_KEYWORDS', [])
        if len(logging_keywords):
            metadata = event_data.get('metadata', {})
            payload = event_data.get('payload', {})
            for keyword in logging_keywords:
                if keyword in event_data['event_type']:
                    with open('/var/log/fleio/os_event_notifications.txt', 'a') as log_file:
                        log_file.write('{} - {} - Message type: {} - Region: {} - Resource id: {}\n'.format(
                            metadata.get('timestamp', 'Missing timestamp'),
                            event_data['event_type'],
                            event_data['message_type'],
                            event_data['region'],
                            _get_os_resource_id_from_payload(payload=payload),
                        ))
                    break

        try:
            if event_data['message_type'] == 'info':
                handle_infos(event_data['event_type'], event_data['metadata'], event_data['payload'],
                             event_data['region'])
            elif event_data['message_type'] == 'error':
                handle_errors(event_data['event_type'], event_data['metadata'], event_data['payload'],
                              event_data['region'])
        except db.utils.OperationalError:
            db.close_old_connections()
        except Exception as e:
            LOG.exception('Handle exception {}'.format(e))
        finally:
            p_queue.task_done()


def handle_infos(event_type, metadata, payload, region):
    collector = None
    if event_type.startswith('compute'):
        collector = NovaCollector()
    elif event_type.startswith('image'):
        collector = GlanceCollector()
    elif event_type.startswith('volume'):
        collector = CinderCollector()
    if collector and event_type in collector.query_events:
        try:
            collector.store_message_event(event_type=event_type, payload=payload, metadata=metadata, region=region)
        except IntegrityError as e:
            LOG.error('Error when trying to store message event {} from collector. Reason: {}.'.format(
                event_type, str(e)
            ))

    for eh in event_handlers(EVH):
        if event_type in eh.event_handlers:
            handler = eh.event_handlers[event_type]
            if callable(handler):
                handler(payload, region, metadata.get('timestamp', None))


def handle_errors(event_type, metadata, payload, region):
    openstack_error.send(
        sender=__name__,
        event_type=event_type,
        payload=payload,
        region=region,
        timestamp=metadata.get('timestamp', None)
    )
    for eh in event_handlers(EVH):
        if hasattr(eh, 'error_handlers') and event_type in eh.error_handlers:
            handler = eh.error_handlers[event_type]
            if callable(handler):
                handler(payload, region, metadata.get('timestamp', None))


class GenericEndpoint(object):
    def info(self, ctxt, publisher_id, event_type, payload, metadata):
        LOG.debug('{} -- {} -- {} -- {} -- {}\n'.format(event_type, publisher_id, metadata, payload, ctxt))
        region = None
        if ctxt:
            region = ctxt.get('fleio_region', None)
        if region is None:
            # FIXME(tomo): We take the first region, however, we might not be right.
            db_region = db_wrap(lambda: OpenstackRegion.objects.enabled().first())
            if db_region:
                region = db_region.id
            else:
                region = plugin_settings.DEFAULT_REGION
        if region is None:
            LOG.error('Unable to find any OpenStack regions')
        p_queue.put(dict(event_type=event_type, metadata=metadata, payload=payload, message_type='info', region=region))
        return oslo_messaging.NotificationResult.HANDLED

    def error(self, ctxt, publisher_id, event_type, payload, metadata):
        LOG.debug('ERROR: {} -- {} -- {} -- {} -- {}'.format(event_type, publisher_id, payload, metadata, ctxt))
        region = None
        if ctxt:
            region = ctxt.get('fleio_region', None)
        if region is None:
            db_region = db_wrap(lambda: OpenstackRegion.objects.first())
            if db_region:
                region = db_region.id
        if region is None:
            LOG.error('Unable to find any OpenStack regions')
        p_queue.put(dict(event_type=event_type, metadata=metadata, payload=payload, message_type='error',
                         region=region))
        return oslo_messaging.NotificationResult.HANDLED

    def warn(self, ctxt, publisher_id, event_type, payload, metadata):
        LOG.debug('WARN: {} - {} - {} - {} - {}'.format(event_type, publisher_id, payload, metadata, ctxt))
        return oslo_messaging.NotificationResult.HANDLED

    def critical(self, ctxt, publisher_id, event_type, payload, metadata):
        LOG.debug('CRITICAL: {} - {} - {} - {} - {}'.format(event_type, publisher_id, payload, metadata, ctxt))
        return oslo_messaging.NotificationResult.HANDLED

    def debug(self, ctxt, publisher_id, event_type, payload, metadata):
        LOG.debug('DEBUG: {} - {} - {} - {} - {}'.format(event_type, publisher_id, payload, metadata, ctxt))
        return oslo_messaging.NotificationResult.HANDLED

    def audit(self, ctxt, publisher_id, event_type, payload, metadata):
        LOG.debug('AUDIT: {} - {} - {} - {} - {}'.format(event_type, publisher_id, payload, metadata, ctxt))
        return oslo_messaging.NotificationResult.HANDLED


def get_listeners():
    endpoints = [GenericEndpoint()]
    listeners = list()
    notifications_urls = plugin_settings.NOTIFICATIONS_URL or []
    for url in notifications_urls:
        try:
            parsed_url = oslo_messaging.TransportURL.parse(cfg.CONF, url)
        except Exception as e:
            LOG.exception(e)
            continue
        transport = oslo_messaging.get_notification_transport(cfg.CONF, url=parsed_url)
        targets = list()
        for exchange in plugin_settings.NOTIFICATIONS_EXCHANGE:
            for topic in plugin_settings.NOTIFICATIONS_TOPIC:
                if topic and exchange:
                    targets.append(oslo_messaging.Target(topic=topic, exchange=exchange))

        listener = oslo_messaging.get_notification_listener(transport=transport,
                                                            targets=targets,
                                                            endpoints=endpoints,
                                                            allow_requeue=True,
                                                            pool=plugin_settings.NOTIFICATIONS_POOL,
                                                            executor=EXECUTOR)
        listeners.append(listener)
    return listeners
