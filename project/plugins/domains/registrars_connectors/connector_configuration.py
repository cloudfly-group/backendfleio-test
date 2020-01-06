import json
import os


class ConnectorConfiguration:
    def __init__(self, name: str):
        directory = os.path.dirname(__file__)
        self.json_file_path = os.path.join(directory, 'config', '{}.config.json'.format(name))
        with open(self.json_file_path, 'r') as file:
            config_contents = file.read()

        self.configuration = json.loads(config_contents)
        self.custom_fields = {}
        self.parse_custom_fields()

    def parse_custom_fields(self):
        custom_fields = self.configuration.get('custom_fields', {})

        for tld_custom_fields in custom_fields:
            tld_name = tld_custom_fields.get('tld', None)
            if tld_name:
                self.custom_fields[tld_name] = {}
                fields = tld_custom_fields.get('fields', None)
                for field_name in fields:
                    # TODO: check if field name exists here
                    self.custom_fields[tld_name][field_name] = fields[field_name]
