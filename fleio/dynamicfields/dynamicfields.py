from __future__ import unicode_literals

import copy
from collections import OrderedDict

from django.utils.translation import ugettext_lazy as _


class DynamicFieldValidationError(Exception):
    pass


class DynamicFields(object):
    def __init__(self, definition):
        self.definition = definition

    def incorrect_value_error(self, data):
        return _('Incorrect value: {0}').format(data)

    def validate_custom_fieldset(self, data):
        """
        Validate data based on a definition.
        :param data: Dataset
        :return: Validated data
        :raises DynamicFieldValidationError
        """
        errors = OrderedDict()
        pop_elements = []
        for field in self.definition:
            data_element = data.get(field['field_name'], None)
            required_rule = field['definition'].get('required', None)
            optional_rule = field['definition'].get('optional', None)
            if self.meets_rule(data, required_rule):
                if data_element is None:
                    errors[field['field_name']] = _('Field is required')
            else:
                meets_rule = self.meets_rule(data, optional_rule) or self.meets_rule(data, required_rule)
                if not meets_rule:
                    pop_elements.append(field['field_name'])
            max_length = field['definition'].get('max_length', None)
            if max_length and data_element and len(str(data_element)) > max_length:
                errors[field['field_name']] = _('Ensure this field has no more than {} characters').format(max_length)
            if not errors.get(field['field_name']) and data_element and field['field_name'] not in pop_elements:
                if field['definition']['type'] in ['radio', 'select']:
                    allowed_values = self.get_allowed_values(data, copy.deepcopy(field['definition']['values']))
                    if data_element not in allowed_values:
                        errors[field['field_name']] = self.incorrect_value_error(data_element)
                if field['definition']['type'] == 'decimal':
                    try:
                        float(data_element)
                    except ValueError:
                        errors[field['field_name']] = self.incorrect_value_error(data_element)
                if field['definition']['type'] == 'int':
                    try:
                        if int(data_element) != float(data_element):
                            errors[field['field_name']] = self.incorrect_value_error(data_element)
                    except ValueError:
                        errors[field['field_name']] = self.incorrect_value_error(data_element)

            validators = field.get('validators', None)
            if validators and not errors.get(field['field_name']) and field['field_name'] not in pop_elements:
                for validator in validators:
                    try:
                        validator(data_element)
                    except Exception as ex:
                        errors[field['field_name']] = ex.message

        for field_to_pop in pop_elements:
            data.pop(field_to_pop, None)
            errors.pop(field_to_pop, None)

        if errors:
            raise DynamicFieldValidationError(errors)

        return data

    def prepare_definition(self, defaults=None):
        """
        Removes attached validators function from fields definition and loads defaults.
        """
        prepared = copy.deepcopy(self.definition)
        for field in prepared:
            field.pop('validators', None)
            if defaults:
                field['default'] = defaults.get(field['field_name'], None)
            if field['definition']['type'] in ['radio', 'select', 'autocomplete']:
                for value_option in field['definition']['values']:
                    if callable(value_option['values']):
                        value_option['values'] = value_option['values']()
        return prepared

    @staticmethod
    def meets_rule(data, ruleset):
        """
        Checks if the data meets the ruleset.
        :param data: The initial dataset
        :param ruleset: Rule set for a field
        :return: True if meets the ruleset, False otherwise
        """
        if ruleset is None:
            return False
        if isinstance(ruleset, bool):
            return ruleset
        if isinstance(ruleset, dict):
            for field in ruleset:
                if isinstance(ruleset[field], list):
                    if not data.get(field, None) in ruleset[field]:
                        return False
                else:
                    if data.get(field) != ruleset[field]:
                        return False
        if callable(ruleset):
            return ruleset(data)
        return True

    def get_allowed_values(self, data, fieldset):
        """
        Return allowed values for a field of type radio, select, etc.
        :param data: The initial dataset
        :param fieldset: Possible values definition for a field
        :return: Allowed values
        """
        values = []
        for definition in fieldset:
            if self.meets_rule(data, definition.get('rule', None)):
                if callable(definition['values']):
                    definition['values'] = definition['values']()
                values = values + [obj['value'] for obj in definition['values']]
        return values
