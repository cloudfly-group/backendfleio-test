import logging
import calendar
from django.db import transaction
from django.utils import dateparse
from fleio.openstack.sync.utils import retry_on_deadlock

LOG = logging.getLogger(__name__)


class BaseHandler(object):
    serializer_class = None
    version_field = 'sync_version'

    @property
    def model_class(self):
        """The model class reference"""
        return self.get_serializer().Meta.model

    @property
    def model_pk_name(self):
        """The model primary key field name"""
        return self.model_class._meta.pk.name

    def get_serializer(self):
        """The ModelSerializer defined for the handler"""
        return self.serializer_class

    @staticmethod
    def get_version(timestamp):
        pdt = dateparse.parse_datetime(timestamp)
        return calendar.timegm(pdt.utctimetuple()) * 1000 + pdt.microsecond // 1000

    def serialize(self, data, region, timestamp):
        raise NotImplementedError('serialize() method needs to be implemented on {}'.format(self.__class__.__name__))

    def create_or_update(self, data, region, timestamp):
        try:
            serialized_data = self.serialize(data, region, timestamp)
        except Exception as e:
            LOG.exception('Unable to serialize: {}'.format(e))
            return

        return self.sync(data=serialized_data)

    @retry_on_deadlock
    def sync(self, data):
        """Create or update if newer version"""
        # TODO(tomo): Switch to optimistic locking ?
        # Right now we use pessimistic locking (select_for_update()).
        # Do note that while this works perfectly fine for a single
        #  MySQL server, it will not sync the locks on a Galera/XtraDB cluster.
        if not data:
            LOG.warning('Sync called without data for {}'.format(self.model_class.__name__))
            return None
        serializer = self.get_serializer()
        model = self.model_class  # The actual model class
        pk_name = self.model_pk_name  # Primary key field name (eg: id)
        model_name = model.__name__  # The model name, mainly for logging
        version = data.get(self.version_field, 0)
        # Make sure the primary key exists in data
        if pk_name not in data:
            LOG.debug('Ignoring update for {} without {} in data: {}'.format(model_name, pk_name, data))
            return None
        with transaction.atomic():
            try:
                instance = model.objects.select_for_update().get(pk=data[pk_name])
            except model.DoesNotExist:
                instance = None
            if instance and getattr(instance, self.version_field, -1) > version:
                LOG.debug('Ignoring {} with older sync version: {}'.format(model_name, data[pk_name]))
                return None
            serialized = serializer(instance=instance,
                                    data=data,
                                    partial=(instance is not None))
            if serialized.is_valid():
                instance = serialized.save()
                LOG.debug('Updated %s: %s Partial: %s' % (model_name, data[pk_name], (instance is not None)))
            else:
                LOG.error('Unable to update {}({}): {}'.format(model_name, data[pk_name], serialized.errors))
        return instance

    @retry_on_deadlock
    def delete(self, obj_id, region, timestamp):
        try:
            return self.model_class.objects.filter(pk=obj_id).delete()
        except TypeError:
            # NOTE(tomo): filter may return None
            pass
