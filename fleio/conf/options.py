import logging

from fleio.conf import types

LOG = logging.getLogger(__name__)


class Empty(object):
    pass


class ConfigOption(object):
    def __init__(self, label=None, option_type=None, default=Empty, encrypted=False,
                 help_text=None, required=False, allow_null=False):
        self.label = label
        self.help_text = help_text
        self.required = required
        self.allow_null = allow_null
        self.encrypted = encrypted
        if option_type is None:
            option_type = types.String()
        self.type = option_type
        self.default = default
        self._check_default()

    def _check_default(self):
        if self.default is Empty:
            return
        elif (self.default == '' or self.default is None) and self.allow_null:
            return
        elif (self.default == '' or self.default is None) and not self.allow_null:
            raise ValueError(
                'Incorrect default value for option {} not allowing null'.format(self.__class__.__name__)
            )
        elif self.default is not None:
            try:
                self.type.serialize(self.default)
            except Exception:
                raise ValueError('Incorrect default value of {} for type {}'.format(self.default, self.type))

    def serialize(self, value):
        if value == '' or value is None:
            if self.allow_null:
                return None
            else:
                raise ValueError('This option may not be null')
        return self.type.serialize(value)

    def deserialize(self, value):
        if value == '' or value is None:
            if self.allow_null:
                return None
            LOG.error('Null or empty value for non null configuration option {}'.format(self.label))
        return self.type.deserialize(value)


class StringOpt(ConfigOption):
    def __init__(self, label=None, choices=None, regex=None, ignore_case=None, max_length=None, **kwargs):
        super(StringOpt, self).__init__(label=label,
                                        option_type=types.String(choices=choices,
                                                                 regex=regex,
                                                                 ignore_case=ignore_case,
                                                                 max_length=max_length),
                                        **kwargs)


class IntegerOpt(ConfigOption):
    def __init__(self, label=None, choices=None, min=None, max=None, **kwargs):
        super(IntegerOpt, self).__init__(label=label,
                                         option_type=types.Integer(choices=choices,
                                                                   min=min,
                                                                   max=max),
                                         **kwargs)


class DecimalOpt(ConfigOption):
    def __init__(self, max_digits, decimal_places, coerce_to_string=False, label=None, choices=None, min=None,
                 max=None, **kwargs):
        super(DecimalOpt, self).__init__(label=label,
                                         option_type=types.Decimal(choices=choices,
                                                                   min=min,
                                                                   max=max,
                                                                   max_digits=max_digits,
                                                                   decimal_places=decimal_places,
                                                                   coerce_to_string=coerce_to_string),
                                         **kwargs)


class URIOpt(ConfigOption):
    def __init__(self, label=None, max_length=None, schemes=None, require_authority=True, **kwargs):
        super(URIOpt, self).__init__(label,
                                     option_type=types.URI(max_length=max_length,
                                                           schemes=schemes,
                                                           require_authority=require_authority),
                                     **kwargs)
        self.schemes = schemes


class BoolOpt(ConfigOption):
    def __init__(self, label=None, **kwargs):
        super(BoolOpt, self).__init__(label, option_type=types.Boolean(), **kwargs)


class JsonOpt(ConfigOption):
    def __init__(self, label=None, **kwargs):
        super(JsonOpt, self).__init__(label, option_type=types.JsonType(), **kwargs)


class ListOpt(ConfigOption):
    def __init__(self, label=None, item_type=None, **kwargs):
        if item_type is None:
            self.item_type = StringOpt()
        else:
            self.item_type = item_type
        invalid_item_type = 'ListOpt can only take StringOpt, IntegerOpt, URIOpt or BoolOpt as item_type'
        assert isinstance(self.item_type, (StringOpt, IntegerOpt, URIOpt, BoolOpt)), invalid_item_type
        super(ListOpt, self).__init__(label, option_type=types.List(item_type=self.item_type.type), **kwargs)


class DictOpt(ConfigOption):
    """Simple key:value dict"""
    def __init__(self, label=None, item_type=None, **kwargs):
        if item_type is None:
            self.item_type = StringOpt()
        else:
            self.item_type = item_type
        invalid_item_type = 'DictOpt can only take StringOpt, IntegerOpt, URIOpt or BoolOpt as item_type'
        assert isinstance(self.item_type, (StringOpt, IntegerOpt, URIOpt, BoolOpt)), invalid_item_type
        super(DictOpt, self).__init__(label, option_type=types.Dict(item_type=self.item_type.type), **kwargs)


class DjangoStringTemplateOpt(ConfigOption):
    def __init__(self, label=None, choices=None, regex=None, ignore_case=None, max_length=None, **kwargs):
        super(DjangoStringTemplateOpt, self).__init__(
            label=label,
            option_type=types.DjangoStringTemplate(
                choices=choices,
                regex=regex,
                ignore_case=ignore_case,
                max_length=max_length
            ),
            **kwargs
        )
