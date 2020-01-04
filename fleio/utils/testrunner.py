import logging
import os

import requests
import sys
import uuid
import urllib3

from os import environ
from os.path import dirname, realpath

from six.moves.urllib.parse import urlparse

from fleio.utils.test import backup_current_license, get_a_license, make_license_version_on_server, \
    remove_license_version_on_server, remove_live_license, restore_current_license
from fleiostaff.core.views import _set_license

try:
    # NOTE(tomo): On python 2 subprocess32 is recommended and should be installed
    from subprocess32 import Popen
except ImportError:
    from subprocess import Popen


from django.test.runner import DiscoverRunner
from django.conf import settings as test_settings
from requests.auth import HTTPBasicAuth

from fleio.openstack.settings import plugin_settings

# disable "InsecureRequestWarning: Unverified HTTPS request is being made." for tests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LOG = logging.getLogger(__name__)


def start_updated_daemon(script, test_database_name, rabbit_pool):
    try:
        updated_daemon = Popen([sys.executable, script, '--test_database_name', test_database_name, '--pool',
                                rabbit_pool])
        return updated_daemon
    except Exception as e:
        LOG.error(e)


def stop_updated_daemon(daemon):
    try:
        daemon.terminate()
        daemon.wait()
    except Exception as e:
        LOG.error(e)


def get_basic_http_auth(url):
    parsed_url = urlparse(url)
    credentials, host = parsed_url.netloc.split('@')
    user, password = credentials.split(':')
    auth = HTTPBasicAuth(user, password)
    return auth, host


def delete_existing_rabbit_test_queue():
    rabbit_urls = plugin_settings.NOTIFICATIONS_URL
    if not rabbit_urls:
        return None
    headers = {'content-type': 'application/json'}
    queue = ''
    if plugin_settings.NOTIFICATIONS_POOL:
        queue = 'test_{}'.format(plugin_settings.NOTIFICATIONS_POOL)
    for rabbit_url in rabbit_urls:
        auth, host_with_port = get_basic_http_auth(rabbit_url)
        try:
            host, port = host_with_port.split(':')
        except ValueError:
            host = host_with_port
        rabbit_management_default_port = '15672'
        if queue:
            rabbit_management_url = 'http://{}:{}/api/queues/%2F/{}'.format(host, rabbit_management_default_port, queue)
            try:
                response = requests.get(rabbit_management_url, headers=headers, auth=auth)
                if response.status_code == 200:
                    requests.delete(rabbit_management_url, headers=headers, auth=auth)
            except Exception as e:
                LOG.error('Error: {}'.format(e))
    return queue


class FleioTestRunner(DiscoverRunner):
    def setup_databases(self, **kwargs):
        if '-k' in sys.argv or '--keepdb' in sys.argv:
            # do not generate unique database name
            test_database_name = 'fleio'
        else:
            test_database_name = '{}'.format(uuid.uuid4())
        environ['test_database_name'] = test_database_name
        test_settings.DATABASES['default']['NAME'] = test_database_name
        names = super(FleioTestRunner, self).setup_databases(**kwargs)
        # test database is created at this point so we create a test pool for Rabbit MQ in the test db
        queue = delete_existing_rabbit_test_queue()
        if queue is None:
            raise ValueError("Missing OpenStack notifications URL setting\n"
                             "Set \"OPENSTACK_PLUGIN_NOTIFICATIONS_URL\" as an environment variable\n"
                             "with a valid RabbitMQ/Qpid URL where the Updated daemon can connect\n"
                             "to receive OpenStack notifications\n")
        script = '{}/openstack/bin/updated.py'.format(dirname(dirname(realpath(__file__))))
        self.daemon = start_updated_daemon(script, test_database_name, queue)

        if os.environ.get('FLEIO_TEST_WITH_REAL_LICENSE', False) == 'true':
            self.license_version = str(uuid.uuid4())
            LOG.info('Backing up license')
            backup_current_license(self.license_version)
            # patch fleio version for licensing server to send license for this version
            test_settings.FLEIO_BACKEND_VERSION = self.license_version
            LOG.info('Make license version {} on server'.format(self.license_version))
            make_license_version_on_server(self.license_version, commit_id=os.environ.get('FLEIO_COMMIT_ID', None))
            license_key = get_a_license()
            test_settings.FLEIO_LICENSE_KEY = license_key
            LOG.info('Setting license {}'.format(license_key))
            _set_license(license_key)
        return names

    def teardown_databases(self, old_config, **kwargs):
        stop_updated_daemon(self.daemon)
        delete_existing_rabbit_test_queue()
        super(FleioTestRunner, self).teardown_databases(old_config, **kwargs)

    def teardown_test_environment(self, **kwargs):
        if os.environ.get('FLEIO_TEST_WITH_REAL_LICENSE', False) == 'true':
            LOG.info('Remove license version {} on server'.format(self.license_version))
            remove_license_version_on_server(self.license_version)
            remove_live_license()
            LOG.info('Restore current license')
            restore_current_license(self.license_version)
        super().teardown_test_environment(**kwargs)
