import logging
import six

from os import environ
from collections import OrderedDict
from cryptography.fernet import InvalidToken
from django.apps import apps

from fleio.conf import exceptions
from fleio.conf.models import Option
from fleio.conf.options import ConfigOption, Empty
from fleio.conf.utils import fernet_decrypt, fernet_encrypt

LOG = logging.getLogger(__name__)


class ConfigOptsMetaclass(type):
    @classmethod
    def _get_declared_options(cls, attrs):
        opts = [(opt_name, attrs.pop(opt_name))
                for opt_name, obj in list(attrs.items())
                if isinstance(obj, ConfigOption)]

        return OrderedDict(opts)

    def __new__(cls, name, bases, attrs):
        attrs['_declared_opts'] = cls._get_declared_options(attrs)
        return super(ConfigOptsMetaclass, cls).__new__(cls, name, bases, attrs)


@six.add_metaclass(ConfigOptsMetaclass)
class ConfigOpts(object):

    class Meta:
        section = None

    def __init__(self, configuration_id=None, raise_if_required_not_set=True):
        self.configuration_id = configuration_id
        self.raise_if_required_not_set = raise_if_required_not_set
        self._options = None
        self._modified = []
        assert self.Meta.section is not None, '{} missing required section definition'.format(self.__class__.__name__)

    @property
    def declared_options(self):
        return self._declared_opts

    def get_queryset(self, model_instance, select_for_update=False):
        if select_for_update:
            val_query = model_instance.objects.select_for_update()
        else:
            val_query = model_instance.objects
        return val_query.filter(configuration_id=self.configuration_id, section=self.Meta.section)

    def get_options(self, select_for_update=False):
        """Query the database for options"""
        try:
            # Some options may be accessed before any models are loaded or while models are loading
            # We try to prevent any ProgrammingError or other fatal exceptions from propagating by
            # checking if the model is actually loaded first
            options_model = apps.get_model('conf', 'Option')
        except LookupError:
            options_model = None
        if apps.ready and options_model:
            return {opt.field.lower(): opt.value for opt in self.get_queryset(options_model, select_for_update)}
        else:
            return {}

    def save(self, clear_cached=True, update_fields: list = None):
        """
        Save to database.
        :param clear_cached: bool, Clears the attribute set on this instance to force a reread on next access
        :param update_fields: list or None, update only these fields, if not empty
        """
        if len(self._modified):
            for field_name in self._modified:
                if field_name in self._declared_opts:
                    if update_fields and field_name not in update_fields:
                        continue
                    field = self._declared_opts[field_name]
                    value = self._declared_opts[field_name].serialize(value=getattr(self, field_name))
                    if field.encrypted:
                        value = fernet_encrypt(value)

                    updated = Option.objects.filter(configuration_id=self.configuration_id,
                                                    section=self.Meta.section,
                                                    field=field_name).update(value=value)
                    if updated == 0:
                        Option.objects.create(configuration_id=self.configuration_id,
                                              section=self.Meta.section,
                                              field=field_name,
                                              value=value)
                if clear_cached:
                    try:
                        delattr(self, field_name)  # Remove the instance owned attribute after saving
                    except AttributeError:
                        pass

    def get_field_value(self, field_name, select_for_update=False):
        environ_key = '{}_{}'.format(self.Meta.section, field_name.upper())
        field = self._declared_opts[field_name]
        if field_name in self.get_options(select_for_update):
            raw_value = self.get_options()[field_name]
            if field.encrypted:
                try:
                    raw_value = fernet_decrypt(value=raw_value)
                except InvalidToken as e:
                    LOG.error('Unable to decrypt {} {}: {}'.format(self.Meta.section, field_name, e))
                    raise exceptions.ConfigDecryptException(message='Invalid configuration',
                                                            section=self.Meta.section,
                                                            configuration_id=self.configuration_id)
            return field.deserialize(value=raw_value)
        elif environ_key in environ:
            raw_value = environ[environ_key]
            # Env variables without a value equal to an empty string
            if self.raise_if_required_not_set:
                if raw_value in (None, '') and field.required is True and field.allow_null is False:
                    raise exceptions.ConfigException(message='Missing required settings {}.{}'.format(self.Meta.section,
                                                                                                      field_name),
                                                     section=self.Meta.section,
                                                     configuration_id=self.configuration_id)
            return field.deserialize(value=environ[environ_key])
        elif field.default is not Empty:
            return field.default
        elif field.required and self.raise_if_required_not_set:
            raise exceptions.ConfigException(message='Missing required settings {}.{}'.format(self.Meta.section,
                                                                                              field_name),
                                             section=self.Meta.section,
                                             configuration_id=self.configuration_id)
        else:
            return None

    def select_for_update(self, item):
        return self.getattr(item, select_for_update=True)

    def getattr(self, item, select_for_update=False):
        option = item.lower()
        if option in self._declared_opts:
            return self.get_field_value(field_name=option, select_for_update=select_for_update)
        else:
            raise AttributeError('No such option')

    def __getattr__(self, item):
        return self.getattr(item)

    def __setattr__(self, key, value):
        option = key.lower()
        if option in self._declared_opts:
            self._modified.append(option)  # Keeps track of modified options
            self._declared_opts[option].serialize(value)  # make sure the value is valid and can be serialized
        super(ConfigOpts, self).__setattr__(key, value)
