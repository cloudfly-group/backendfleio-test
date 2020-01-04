import logging
import collections
import operator
import six

from fleio.conf import types

LOG = logging.getLogger(__name__)


class Missing:
    pass


comparators = {
    'in': lambda x, y: operator.contains(y, x) if x is not Missing else False,
    'nin': lambda x, y: operator.not_(operator.contains(y, x)) if x is not Missing else True,
    'eq': operator.eq,
    'ne': operator.ne,
    'exists': lambda x, y: x is not Missing if y else x is Missing,
    'null': lambda x, y: x is not None if y else x is None,
}


class CustomFieldException(Exception):
    pass


class FieldDefinitionException(CustomFieldException):
    pass


class ValidationException(CustomFieldException):
    pass


class FieldValidationException(ValidationException):
    pass


class CustomField(object):
    def __init__(self, name, definition=None):
        self.name = name
        self._definition = definition
        self.allowed_value_types = ('string', 'int', 'uri', 'bool', 'decimal')
        self.value_type = 'string'
        self.value_type_options = {}

    @staticmethod
    def parse_choices(field_name, choices):
        parsed_choices = []
        if callable(choices):
            choices = choices()
        if not isinstance(choices, list):
            return parsed_choices
        for choice in choices:
            if isinstance(choice, tuple) or isinstance(choice, list):
                if len(choice) == 2:
                    choice_value = choice[0]
                    choice_label = choice[1]
                elif len(choice) == 1 and isinstance(choice[0], six.string_types):
                    choice_label = choice_value = choice[0]
                else:
                    LOG.debug('Ignoring custom field "{}" invalid choice "{}"'.format(field_name, choice))
                    continue
            elif isinstance(choice, six.string_types):
                choice_value = choice
                choice_label = choice_value
            else:
                LOG.debug('Ignoring custom field "{}" unknown choice format "{}"'.format(field_name, choice))
                continue
            parsed_choices.append({'value': choice_value, 'label': choice_label})
        return parsed_choices

    def definition(self):
        # Set label to label or uppercase name
        new_field_definition = {
            'label': self._definition.get('label', None) or self.name.upper(),
            'type': self._definition.get('type', None) or 'text',
            'optional': self._definition.get('optional', False),
            'required': self._definition.get('required', False),
            'category': self._definition.get('category', ''),
            'validator': self._definition.get('validator', None),
        }
        if callable(new_field_definition['optional']):
            new_field_definition['optional'] = new_field_definition['optional']()
        if callable(new_field_definition['required']):
            new_field_definition['required'] = new_field_definition['required']()

        # Parse value types
        value_type = self._definition.get('value_type', 'string')
        value_type_options = self._definition.get('value_type_options', {})
        if value_type not in self.allowed_value_types:
            raise FieldDefinitionException('Invalid value_type: "{}" for "{}"'.format(self.name, value_type))
        self.value_type = value_type
        self.value_type_options = value_type_options
        # Parse choices
        raw_choices = self._definition.get('choices', Missing)
        if raw_choices is not Missing:
            try:
                choices = self.parse_choices(self.name, self._definition['choices'])
            except (TypeError, AttributeError, ValueError, KeyError):
                raise FieldValidationException('Invalid choices for "{}"'.format(self.name))
            if len(choices):
                new_field_definition['choices'] = choices
        return new_field_definition


class CustomFieldDefinition(object):
    def __init__(self, config=None):
        self.config = config
        self.allowed_types = ('text', 'select', 'check')
        self.allowed_value_types = ('string', 'int', 'uri', 'bool', 'decimal')

    @property
    def original_definition(self):
        if not isinstance(self.config, collections.Mapping):
            return {}
        else:
            return self.config

    @property
    def definition(self):
        """Initial definition parsing and validation"""
        definition = {}
        if not isinstance(self.original_definition, collections.Mapping):
            return {}
        for field_name, field_definition in iter(self.original_definition.items()):
            new_field = CustomField(name=field_name, definition=field_definition)
            try:
                new_field_definition = new_field.definition()
            except FieldDefinitionException as e:
                LOG.error('Ignoring custom field "{}": {}'.format(field_name, e))
                continue
            definition[field_name] = new_field_definition
        return definition

    @staticmethod
    def get_field_value(field_name, new_fields, old_instance):
        """
        Get an attribute/key value from a dict or a model instance.
        The new_fields dict has priority.
        We return Missing if we don't find anything.
        """
        if field_name in new_fields:
            return new_fields[field_name]
        else:
            return getattr(old_instance, field_name, Missing)

    def parse_rule(self, rule, new_fields, old_instance):
        """Returns the boolean result of a rule.
        Parse a single rule like {'operator': <list>} and return it's value.
        """
        if isinstance(rule, bool):
            # {"required": True}, True is a boolean, no need to evaluate
            return rule
        elif isinstance(rule, collections.Mapping):
            """{"country": {"in": ['AB', 'CD']}}"""
            for object_field, rule_data in iter(rule.items()):
                object_field_value = self.get_field_value(field_name=object_field,
                                                          new_fields=new_fields,
                                                          old_instance=old_instance)
                if isinstance(rule_data, collections.Mapping):
                    for operand_key, operand in iter(rule_data.items()):
                        if operand_key not in comparators:
                            return False
                        try:
                            if not comparators[operand_key](object_field_value, operand):
                                return False
                        except TypeError:
                            # Unable to compare. Invalid rule ?
                            return False
                else:
                    # Only support dict rules for now like {"eq": True}
                    return False
            return True
        else:
            return False

    def parse_rules(self, new_fields, old_instance):
        parsed_definition = {}
        for field_name, field_definition in iter(self.definition.items()):
            required_rule = field_definition.get('required', False)
            optional_rule = field_definition.get('optional', False)
            required = False
            optional = False
            if required_rule:
                required = self.parse_rule(rule=required_rule, new_fields=new_fields, old_instance=old_instance)
            if optional_rule:
                optional = self.parse_rule(rule=optional_rule, new_fields=new_fields, old_instance=old_instance)

            parsed_definition[field_name] = {'label': field_definition['label'],
                                             'required': required,
                                             'optional': optional,
                                             'type': field_definition['type'],
                                             'value_type': field_definition.get('value_type', 'string'),
                                             'value_type_options': field_definition.get('value_type_options', {})}
            if 'choices' in field_definition:
                parsed_definition[field_name]['choices'] = field_definition['choices']
        return parsed_definition

    def validate(self, new_fields, instance=None):
        custom_fields = {}
        parsed_definition = self.parse_rules(new_fields=new_fields, old_instance=instance)
        # Get the custom fields names and values as dict
        custom_fields_values = {}
        if 'custom_fields' in new_fields and isinstance(new_fields['custom_fields'], list):
            for v in new_fields['custom_fields']:
                custom_fields_values[v['name']] = v['value']

        for cf_name, cf_def in iter(parsed_definition.items()):
            cf_value = self.get_field_value(cf_name,
                                            custom_fields_values,
                                            None)
            if cf_def.get('required', False):
                if cf_value is Missing:
                    raise FieldValidationException('{} is required'.format(cf_name))
                elif cf_def.get('choices', None):
                    if cf_value not in [c['value'] for c in cf_def.get('choices')]:
                        raise FieldValidationException('{} invalid choice'.format(cf_name))
                    custom_fields[cf_name] = cf_value
                else:
                    custom_fields[cf_name] = cf_value
            elif cf_def.get('optional', False):
                if cf_value is not Missing:
                    if cf_def.get('choices', None):
                        if cf_value not in [c['value'] for c in cf_def.get('choices')]:
                            raise FieldValidationException('{} invalid choice'.format(cf_name))
                    custom_fields[cf_name] = cf_value
        return custom_fields


class CustomFields(object):
    def __init__(self, definition):
        self.definition = CustomFieldDefinition(config=definition)
        self.value_type_map = {'string': types.String,
                               'int': types.Integer,
                               'decimal': types.Decimal,
                               'uri': types.URI,
                               'bool': types.Boolean}

    def get_type(self, value_type, value_type_options):
        """Returns the instance of type serializer"""
        return self.value_type_map[value_type](**value_type_options)

    def serialize_value(self, value_type, value_type_options, value):
        return self.get_type(value_type, value_type_options).serialize(value)

    def deserialize_value(self, value_type, value_type_options, value):
        return self.get_type(value_type, value_type_options).deserialize(value)

    def validate(self, data, extra_attributes=None):
        custom_fields = {}
        parsed_definition = self.definition.parse_rules(new_fields=data, old_instance=extra_attributes)
        # Get the custom fields names and values as dict
        for cf_name, cf_def in iter(parsed_definition.items()):
            cf_value = self.definition.get_field_value(cf_name, data, None)
            # Validate single field value
            if cf_value is not Missing:
                try:
                    cf_value = self.serialize_value(value_type=cf_def['value_type'],
                                                    value_type_options=cf_def['value_type_options'],
                                                    value=cf_value)
                except ValueError:
                    raise FieldValidationException('Invalid value')
            required = cf_def.get('required', False)
            optional = cf_def.get('optional', False)
            if required:
                if cf_value is Missing:
                    raise FieldValidationException('{} is required'.format(cf_name))
                elif cf_def.get('choices', None):
                    if cf_value not in [c['value'] for c in cf_def.get('choices')]:
                        raise FieldValidationException('{} invalid choice'.format(cf_name))
                    custom_fields[cf_name] = cf_value
                else:
                    custom_fields[cf_name] = cf_value
            elif optional:
                if cf_value is not Missing:
                    if cf_def.get('choices', None):
                        if cf_value not in [c['value'] for c in cf_def.get('choices')]:
                            raise FieldValidationException('{} invalid choice'.format(cf_name))
                    custom_fields[cf_name] = cf_value
        return custom_fields

    def serialize(self, data):
        return self.validate(data)

    def deserialize(self, value, extra_attributes=None):
        custom_fields = {}
        parsed_definition = self.definition.parse_rules(new_fields=value, old_instance=extra_attributes)
        for cf_name, cf_def in iter(parsed_definition.items()):
            cf_value = self.definition.get_field_value(cf_name, value, None)
            custom_fields[cf_name] = cf_value
        return custom_fields
