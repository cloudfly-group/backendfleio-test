import json
import logging
import os

WHOIS_CONFIG_FILE_NAME = 'dist.whois.json'

LOG = logging.getLogger(__name__)


class TLDWhoisConfig:
    def __init__(self, tld: str, whois_server: str, available_search_string: str):
        self.tld = tld
        self.whois_server = whois_server
        self.available_search_string = available_search_string


class WhoisConfig:
    def __init__(self):
        self.tld_whois_configurations = {}

    def load_config(self, app_path: str):
        config_file_path = os.path.join(app_path, WHOIS_CONFIG_FILE_NAME)
        with open(config_file_path, 'r') as file:
            config_contents = file.read()

        whois_list = json.loads(config_contents)

        for whois_entry in whois_list:
            extensions = whois_entry['extensions'].split(',')
            for extension in extensions:
                extension = extension.lower()
                tld_config = TLDWhoisConfig(
                    tld=extension,
                    whois_server=whois_entry['uri'],
                    available_search_string=whois_entry['available']
                )

                if extension in self.tld_whois_configurations:
                    LOG.error('Duplicate extension {}'.format(extension))

                self.tld_whois_configurations[extension] = tld_config

        LOG.info('Loaded whois configuration for {} distinct TLDs'.format(len(self.tld_whois_configurations)))


whois_config = WhoisConfig()
