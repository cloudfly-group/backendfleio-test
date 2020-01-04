from django.test import TestCase

from .dynamicfields import DynamicFields, DynamicFieldValidationError

TEST_DEFINITION1 = [
    {'field_name': 'field_1',
     'definition': {'type': 'text',
                    'required': True,
                    'label': 'First field'}},
    {'field_name': 'field_2',
     'definition': {'type': 'text',
                    'required': {'field_1': 'bogus'},
                    'label': 'Second field'}},
    {'field_name': 'field_3',
     'definition': {'type': 'select',
                    'required': {'field_2': 'bogus'},
                    'label': 'Third field',
                    'values': [{'rule': True,
                                'values': [{'label': 'First value', 'value': 1},
                                           {'label': 'Second Value', 'value': 2}]}]}},
]

TEST_DEFINITION2 = [
    {'field_name': 'field_1',
     'definition': {'type': 'text',
                    'required': True,
                    'label': 'First field'}},
    {'field_name': 'field_2',
     'definition': {'type': 'text',
                    'required': {'field_9': 'bogus'},
                    'label': 'Second field'}},
    {'field_name': 'field_3',
     'definition': {'type': 'select',
                    'required': {'field_2': 'bogus'},
                    'label': 'Third field',
                    'values': [{'rule': True,
                                'values': [{'label': 'First value', 'value': 1},
                                           {'label': 'Second Value', 'value': 2}]}]}},
]


class TestDynamicFields(TestCase):

    df1 = DynamicFields(definition=TEST_DEFINITION1)
    df2 = DynamicFields(definition=TEST_DEFINITION2)

    def test_prepare_definition(self):
        """Prepared definition should not contain validator functions."""
        prepared = self.df1.prepare_definition()
        validator_found = False
        for field_def in prepared:
            validator = field_def.get('validators', None)
            if validator:
                validator_found = True
                break
        self.assertFalse(validator_found)

    def test_meets_rule_list_valid_single(self):
        """Single rule, rule type list."""
        data = {'field_1': 4}
        ruleset = {'field_1': [1, 2, 3, 4]}
        self.assertTrue(self.df1.meets_rule(data=data, ruleset=ruleset))

    def test_meets_rule_list_invalid_single(self):
        """Single rule, rule type list."""
        data = {'field_1': 4}
        ruleset = {'field_1': [1, 2, 3]}
        self.assertFalse(self.df1.meets_rule(data=data, ruleset=ruleset))

    def test_meets_rule_list_valid_multiple(self):
        """Multiple rules, rule type list."""
        data = {'field_1': 4,
                'field_2': 5}
        ruleset = {'field_1': [1, 2, 3, 4],
                   'field_2': [5, 6]}
        self.assertTrue(self.df1.meets_rule(data=data, ruleset=ruleset))

    def test_meets_rule_list_invalid_multiple(self):
        """Multiple rules, rule type list."""
        data = {'field_1': 4,
                'field_2': 5}
        ruleset = {'field_1': [1, 2, 3, 4],
                   'field_2': [6]}
        self.assertFalse(self.df1.meets_rule(data=data, ruleset=ruleset))

    def test_meets_rule_constant_valid_single(self):
        """Single rule, rule type constant."""
        data = {'field_1': 4}
        ruleset = {'field_1': 4}
        self.assertTrue(self.df1.meets_rule(data=data, ruleset=ruleset))

    def test_meets_rule_constant_valid_multiple(self):
        """Multiple rules, rule type constant."""
        data = {'field_1': 4,
                'field_2': 5}
        ruleset = {'field_1': 4,
                   'field_2': 5}
        self.assertTrue(self.df1.meets_rule(data=data, ruleset=ruleset))

    def test_meets_rule_constant_invalid_multiple(self):
        """Multiple rules, rule type constant."""
        data = {'field_1': 4,
                'field_2': 5}
        ruleset = {'field_1': 3,
                   'field_2': 5}
        self.assertFalse(self.df1.meets_rule(data=data, ruleset=ruleset))

    def test_meets_rule_boolean(self):
        """Single rule, rule type bool."""
        data = {'field_1': 4,
                'field_2': 5}
        ruleset = True
        self.assertTrue(self.df1.meets_rule(data=data, ruleset=ruleset))

    def test_get_allowed_values_valid_single(self):
        """Get allowed value list, single valid rule."""
        data = {'field_1': 9}
        fieldset = [{'rule': {'field_1': 9},
                     'values': [{'value': 'val2', 'label': 'Value 1'},
                                {'value': 'val1', 'label': 'Value 2'}]

                     }]
        allowed_values = self.df1.get_allowed_values(data=data, fieldset=fieldset)
        self.assertEqual(sorted(['val1', 'val2']), sorted(allowed_values))

    def test_get_allowed_values_invalid_single(self):
        """Get allowed value list, single invalid rule."""
        data = {'field_1': 9}
        fieldset = [{'rule': {'field_1': 8},
                     'values': [{'value': 'val2', 'label': 'Value 1'},
                                {'value': 'val1', 'label': 'Value 2'}]

                     }]
        allowed_values = self.df1.get_allowed_values(data=data, fieldset=fieldset)
        self.assertEqual([], allowed_values)

    def test_get_allowed_values_valid_multiple(self):
        """Get allowed value list, multiple valid rules."""
        data = {'field_1': 9}
        fieldset = [{'rule': {'field_1': 9},
                     'values': [{'value': 'val2', 'label': 'Value 1'},
                                {'value': 'val1', 'label': 'Value 2'}]

                     },
                    {'rule': True,
                     'values': [{'value': 'val3', 'label': 'Value 3'},
                                {'value': 'val4', 'label': 'Value 4'}]

                     }]
        allowed_values = self.df1.get_allowed_values(data=data, fieldset=fieldset)
        self.assertEqual(sorted(['val1', 'val2', 'val4', 'val3']), sorted(allowed_values))

    def test_get_allowed_values_partial_multiple(self):
        """Get allowed value list, multiple partially valid rules."""
        data = {'field_1': 9}
        fieldset = [{'rule': {'field_1': 9},
                     'values': [{'value': 'val2', 'label': 'Value 1'},
                                {'value': 'val1', 'label': 'Value 2'}]

                     },
                    {'rule': False,
                     'values': [{'value': 'val3', 'label': 'Value 3'},
                                {'value': 'val4', 'label': 'Value 4'}]

                     }]
        allowed_values = self.df1.get_allowed_values(data=data, fieldset=fieldset)
        self.assertEqual(sorted(['val1', 'val2']), sorted(allowed_values))

    def test_validate_no_data(self):
        """Test validity with empty input data."""
        self.assertRaises(DynamicFieldValidationError, self.df1.validate_custom_fieldset, {})

    def test_validate_invalid_data(self):
        """Test validity with invalid input data."""
        data = {'field_1': 'bogus',
                'field_2': 'bogus',
                'field_3': 7}
        self.assertRaises(DynamicFieldValidationError, self.df1.validate_custom_fieldset, data)

    def test_validate_valid_data_no_pops(self):
        """Test validity with valid data and no additional (non-required) data."""
        data = {'field_1': 'bogus',
                'field_2': 'bogus',
                'field_3': 2}
        validated_data = self.df1.validate_custom_fieldset(data)
        self.assertDictEqual(validated_data, data)

    def test_validate_valid_data_with_pops(self):
        """Test validity with valid data and with additional (non-required) data."""
        data = {'field_1': 'bogus',
                'field_2': 'test',
                'field_3': 2}
        validated_data = self.df1.validate_custom_fieldset(data)
        # field_3 isn't required in this case (field_2 != 'bogus')
        self.assertTrue(validated_data.get('field_3', None) is None)

    def test_validate_valid_data_outsider(self):
        """Test validity with valid data and with data not present in definition."""
        data = {'field_1': 'bogus',
                'field_2': 'test',
                'field_7': 2}
        validated_data = self.df1.validate_custom_fieldset(data)
        self.assertDictEqual(validated_data, data)

    def test_validate_rule_depends_on_data_not_present_in_definition_invalid(self):
        """Validation can depend on data not present in definition."""
        data = {'field_1': 'bogus',
                'field_9': 'bogus'}
        # field_2 is required when field_9 is 'bogus', field_9 is not present in definition
        self.assertRaises(DynamicFieldValidationError, self.df2.validate_custom_fieldset, data)
