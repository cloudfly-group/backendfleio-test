import json
import logging
import os
from typing import Dict

LOG = logging.getLogger(__name__)


DEFAULT_CONFIGURATION_FILE = 'default_custom_fields.config.json'
USER_CONFIGURATION_FILE = 'custom_fields.config.json'


class CustomFieldsConfiguration:
    def __init__(self):
        directory = os.path.dirname(__file__)
        user_json_file_path = os.path.join(directory, 'config', USER_CONFIGURATION_FILE)
        default_json_file_path = os.path.join(directory, 'config', DEFAULT_CONFIGURATION_FILE)

        user_custom_fields_dict = default_custom_fields_dict = None

        if os.path.isfile(user_json_file_path):
            # if user configuration file exists attempt to load it
            try:
                with open(user_json_file_path, 'r', encoding='utf-8') as file:
                    user_custom_fields_dict = json.load(file)
            except Exception as e:
                LOG.exception('Exception {} when loading user configuration file'.format(e))

        if os.path.isfile(default_json_file_path):
            # if user configuration file exists attempt to load it
            try:
                with open(default_json_file_path, 'r', encoding='utf-8') as file:
                    default_custom_fields_dict = json.load(file)
            except Exception as e:
                LOG.exception('Exception {} when loading default configuration file'.format(e))

        self.custom_fields_dict = default_custom_fields_dict if default_custom_fields_dict else {}
        self.custom_fields = CustomFieldsConfiguration.parse_custom_fields(
            custom_fields_to_parse=self.custom_fields_dict
        )

        if user_custom_fields_dict:
            user_custom_fields = CustomFieldsConfiguration.parse_custom_fields(
                custom_fields_to_parse=user_custom_fields_dict
            )
            self.custom_fields.update(user_custom_fields)

    @staticmethod
    def parse_custom_fields(custom_fields_to_parse):
        resulting_custom_fields = {}
        for tlds_custom_fields in custom_fields_to_parse:
            tld_names = tlds_custom_fields.get('tlds', None)
            if tld_names:
                resulting_custom_fields[tld_names] = {}
                fields = tlds_custom_fields.get('fields', None)
                for field_name in fields:
                    fields[field_name]['category'] = '{} fields'.format(tld_names)
                    resulting_custom_fields[tld_names][field_name] = fields[field_name]

        return resulting_custom_fields

    def get_definitions_for_tld(self, tld_name: str) -> Dict[str, Dict]:
        for tld_names in self.custom_fields:  # type: str
            if tld_name in tld_names.split(','):
                return self.custom_fields[tld_names]

        return {}


tld_custom_fields = CustomFieldsConfiguration()
