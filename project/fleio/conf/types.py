from __future__ import unicode_literals

import decimal
import json
import re

from django.template import Context, Template
from django.template.exceptions import TemplateSyntaxError
from django.utils.encoding import force_text
from rfc3986 import api, exceptions, validators
import six


class ConfigType(object):
    def __init__(self, type_name='unknown type'):
        self.type_name = type_name

    def serialize(self, value):
        return value

    def deserialize(self, value):
        return value


class String(ConfigType):
    def __init__(self, choices=None, regex=None, ignore_case=False, max_length=None, type_name='string value'):
        super(String, self).__init__(type_name=type_name)
        if choices and regex:
            raise ValueError("Specify either 'choices' or 'regex', not both")
        self.ignore_case = ignore_case
        self.max_length = max_length or 0
        self.choices = choices
        self.lower_case_choices = None
        if self.choices is not None and self.ignore_case:
            self.lower_case_choices = [six.text_type(c).lower() for c in choices]
        self.regex = regex
        if self.regex is not None:
            re_flags = re.IGNORECASE if self.ignore_case else 0
            if isinstance(regex, six.string_types):
                self.regex = re.compile(regex, re_flags)
            else:
                self.regex = re.compile(regex.pattern, re_flags | regex.flags)

    def serialize(self, value):
        value = six.text_type(value)

        if len(value) > self.max_length > 0:
            raise ValueError("Value '%s' exceeds maximum length %d" %
                             (value, self.max_length))

        if self.regex and not self.regex.search(value):
            raise ValueError("Value %r doesn't match regex %r" %
                             (value, self.regex.pattern))

        if self.choices is None:
            return value

        # Check for case insensitive
        processed_value, choices = ((value.lower(), self.lower_case_choices)
                                    if self.ignore_case else
                                    (value, self.choices))
        if processed_value in choices:
            return value

        raise ValueError(
            'Valid values are [%s], but found %s' % (
                ', '.join([str(v) for v in self.choices]),
                repr(value)))

    def deserialize(self, value):
        return value


class Number(ConfigType):
    def __init__(self, num_type, type_name, min, max, choices=None):
        super(Number, self).__init__(type_name=type_name)

        if min is not None and max is not None and max < min:
            raise ValueError('Max value is less than min value')

        invalid_choices = [c for c in choices or [] if (min is not None and min > c) or (max is not None and max < c)]
        if invalid_choices:
            raise ValueError("Choices %s are out of bounds [%s..%s]"
                             % (invalid_choices, min, max))
        self.min = min
        self.max = max
        self.choices = choices
        self.num_type = num_type

    def serialize(self, value):
        if not isinstance(value, self.num_type):
            s = six.text_type(value).strip()
            if s == '':
                return None
            value = self.num_type(value)

        if self.choices is None:
            if self.min is not None and value < self.min:
                raise ValueError('Should be greater than or equal to %g' %
                                 self.min)
            if self.max is not None and value > self.max:
                raise ValueError('Should be less than or equal to %g' %
                                 self.max)
        else:
            if value not in self.choices:
                raise ValueError('Valid values are %r, but found %g' % (
                    self.choices, value))
        return six.text_type(value)

    def deserialize(self, value):
        return self.num_type(value)


class Integer(Number):
    def __init__(self, min=None, max=None, type_name='integer value', choices=None):
        super(Integer, self).__init__(int, type_name=type_name, min=min, max=max, choices=choices)


class Float(Number):
    def __init__(self, min=None, max=None, type_name='integer value', choices=None):
        super(Float, self).__init__(float, type_name=type_name, min=min, max=max, choices=choices)


class Decimal(ConfigType):
    def __init__(self, max_digits, decimal_places, coerce_to_string=False, min=None, max=None,
                 type_name='decimal value', choices=None):
        super(Decimal, self).__init__(type_name=type_name)
        self.max_digits = max_digits
        self.decimal_places = decimal_places
        self.coerce_to_string = coerce_to_string
        if self.max_digits is not None and self.decimal_places is not None:
            self.max_whole_digits = self.max_digits - self.decimal_places
        else:
            self.max_whole_digits = None
        if min is not None:
            min = decimal.Decimal(min)
        if max is not None:
            max = decimal.Decimal(max)
        if choices is not None:
            choices = [decimal.Decimal(c) for c in choices]
        if min is not None and max is not None and max < min:
            raise ValueError('Max value is less than min value')

        invalid_choices = [c for c in choices or [] if (min is not None and min > c) or (max is not None and max < c)]
        if invalid_choices:
            raise ValueError("Choices %s are out of bounds [%s..%s]"
                             % (invalid_choices, min, max))
        self.min = min
        self.max = max
        self.choices = choices

    def quantize(self, value):
        """
        Quantize the decimal value to the configured precision.
        """
        if self.decimal_places is None:
            return value

        context = decimal.getcontext().copy()
        if self.max_digits is not None:
            context.prec = self.max_digits
        return value.quantize(
            decimal.Decimal('.1') ** self.decimal_places,
            context=context
        )

    def serialize(self, value):
        if not isinstance(value, decimal.Decimal):
            s = six.text_type(value).strip()
            if s == '':
                return None
            try:
                value = decimal.Decimal(value)
            except decimal.DecimalException:
                raise ValueError('Invalid decimal value')

        if value != value or value in (decimal.Decimal('Inf'), decimal.Decimal('-Inf')):
            # Check for NaN
            raise ValueError('Invalid decimal value')

        if self.choices is None:
            if self.min is not None and value < self.min:
                raise ValueError('Should be greater than or equal to %g' %
                                 self.min)
            if self.max is not None and value > self.max:
                raise ValueError('Should be less than or equal to %g' %
                                 self.max)
        else:
            if value not in self.choices:
                raise ValueError('Valid values are %r, but found %g' % (
                    self.choices, value))
        return six.text_type(self.quantize(value)).strip()

    def deserialize(self, value):
        decimal_value = decimal.Decimal(value)
        quantized = self.quantize(decimal_value)
        return quantized


class Boolean(ConfigType):
    """Boolean type.
    Values are case insensitive and can be set using
    1/0, yes/no, true/false or on/off.
    """
    TRUE_VALUES = ['true', '1', 'on', 'yes']
    FALSE_VALUES = ['false', '0', 'off', 'no']

    def __init__(self, type_name='boolean value'):
        super(Boolean, self).__init__(type_name=type_name)

    def serialize(self, value):
        if value is True:
            return 'true'
        elif value is False:
            return 'false'
        elif value is None:
            return 'null'
        else:
            raise ValueError('Unexpected boolean value %r' % value)

    def deserialize(self, value):
        s = value.lower()
        if s in self.TRUE_VALUES:
            return True
        elif s in self.FALSE_VALUES:
            return False
        elif s == 'null':
            return None
        else:
            raise ValueError('Unexpected boolean value %r' % value)


class Port(Integer):
    """Port type
    Represents a L4 Port.
    :param min: Optional check that value is greater than or equal to min.
    :param max: Optional check that value is less than or equal to max.
    :param type_name: Type name to be used in the sample config file.
    :param choices: Optional sequence of valid values.
    .. versionadded:: 3.16
    """

    PORT_MIN = 0
    PORT_MAX = 65535

    def __init__(self, min=None, max=None, type_name='port', choices=None):
        min = self.PORT_MIN if min is None else min
        max = self.PORT_MAX if max is None else max
        if min < self.PORT_MIN:
            raise ValueError('Min value cannot be less than %(min)d' %
                             {'min': self.PORT_MIN})
        if max > self.PORT_MAX:
            raise ValueError('Max value cannot be more than %(max)d' %
                             {'max': self.PORT_MAX})

        super(Port, self).__init__(min=min, max=max, type_name=type_name,
                                   choices=choices)


class URI(ConfigType):
    """URI type
    Represents URI. Value will be validated as RFC 3986.
    :param max_length: Optional integer. If a positive value is specified,
                       a maximum length of an option value must be less than
                       or equal to this parameter. Otherwise no length check
                       will be done.
    :param schemes: List of valid schemes.
    """

    def __init__(self, max_length=None, schemes=None, require_authority=True, type_name='uri value'):
        super(URI, self).__init__(type_name=type_name)
        self.max_length = max_length
        if schemes is None:
            schemes = ['http', 'https', 'ftp', 'ftps']
        self.schemes = schemes
        self.require_authority = require_authority

    def serialize(self, value):
        value = six.text_type(value)

        if self.max_length is not None and len(value) > self.max_length:
            raise ValueError("Value '%s' exceeds maximum length %d" %
                             (value, self.max_length))

        validator = validators.Validator().require_presence_of('scheme').allow_schemes(*self.schemes)
        try:
            validator.validate(api.uri_reference(value))
        except exceptions.RFC3986Exception as e:
            # NOTE(erno): treat all exceptions as one for now
            raise ValueError('Invalid url: {}'.format(force_text(e)))
        return value

    def deserialize(self, value):
        return value


class JsonType(ConfigType):
    def __init__(self, type_name='json type'):
        super(JsonType, self).__init__(type_name=type_name)

    def serialize(self, value):
        return json.dumps(value)

    def deserialize(self, value):
        return json.loads(value)


class List(ConfigType):
    def __init__(self, item_type=None, type_name='list value'):
        super(List, self).__init__(type_name=type_name)
        if item_type is None:
            self.item_type = String()
        else:
            self.item_type = item_type

    def serialize(self, value):
        if value is None:
            return json.dumps(value)
        else:
            return json.dumps(list(map(self.item_type.serialize, value)))

    def deserialize(self, value):
        try:
            deserialized_list = json.loads(value)
        except ValueError:
            try:
                deserialized_list = [v.strip() for v in value.split(',')]
            except Exception:
                raise ValueError('Invalid value {} for {}'.format(value, self.__class__.__name__))

        if deserialized_list is None:
            return None
        else:
            return list(map(self.item_type.deserialize, deserialized_list))


class Dict(ConfigType):
    def __init__(self, item_type=None, type_name='dict value'):
        super(Dict, self).__init__(type_name=type_name)
        if item_type is None:
            self.item_type = String()
        else:
            self.item_type = item_type

    def serialize(self, value):
        if value is None:
            return json.dumps(value)
        else:
            result = {}
            for key, val in iter(value.items()):
                result[key] = self.item_type.serialize(val)
            return json.dumps(result)

    def deserialize(self, value):
        deserialized_dict = json.loads(value)

        if deserialized_dict is None:
            return None
        else:
            result = {}
            for k, v in iter(deserialized_dict.items()):
                result[k] = self.item_type.deserialize(v)
            return result


class DjangoStringTemplate(String):
    def serialize(self, value):
        try:
            Template(value).render(Context())
        except TemplateSyntaxError as e:
            raise ValueError(e)
        return super(DjangoStringTemplate, self).serialize(value)
