import argparse
import sys
import logging
import cotyledon
import multiprocessing
import threading
import time
import fcntl
import json
from django.conf import settings as django_settings
from django import apps
from os.path import abspath, dirname
from os import environ
import django

current_path = dirname(abspath(__file__))
fleio_path = dirname(dirname(dirname(current_path)))
sys.path.append(fleio_path)

parser = argparse.ArgumentParser()
parser.add_argument('--pool', help='rabbit_mq pool used in case multiple consumers share the same queue.')
parser.add_argument('--test_database_name', help='the test db for updated to use, solely for testing.')
args = parser.parse_args()

if args.pool:
    environ['OPENSTACK_PLUGIN_NOTIFICATIONS_POOL'] = args.pool

if args.test_database_name:
    django_settings.DATABASES['default']['NAME'] = 'test_{}'.format(args.test_database_name)

environ.setdefault("DJANGO_SETTINGS_MODULE", "fleio.settings")
django.setup()

from fleio.openstack.updated import get_listeners, handle_queued_events
from fleio.openstack.settings import plugin_settings
from fleio.core.models import Operation
from fleio.core.operations_base.operation_factory import operations_factory

LOG = logging.getLogger(__name__)


class UpdatedService(cotyledon.Service):
    name = "fleio"

    def __init__(self, worker_id, reload_event):
        super(UpdatedService, self).__init__(worker_id)
        self.listeners = list()
        self.reload_event = reload_event

    def stop_listeners(self):
        try:
            for l in self.listeners:
                l.stop(timeout=10)
            for l in self.listeners:
                l.wait()
        except Exception as e:
            LOG.exception(e)

    def start_listeners(self):
        self.listeners = get_listeners()
        for l in self.listeners:
            l.start(timeout=10)

    def reload_on_event(self):
        self.reload_event.wait()
        LOG.info('Reloading %s' % self.pid)
        self.reload()

    def listen_for_reload(self):
        w = threading.Thread(target=self.reload_on_event, name='ReloadEventThread')
        w.daemon = True
        w.start()
        return w

    def run(self):
        LOG.info('Starting %s main process' % self.name)
        self.listen_for_reload()
        self.start_listeners()
        handle_queued_events()

    def reload(self):
        self.stop_listeners()
        super(UpdatedService, self).reload()

    def terminate(self):
        self.stop_listeners()
        sys.exit(42)


class SettingsCheck(cotyledon.Service):
    """Check the SETTINGS_VERSION for modifications and trigger an event"""
    name = "SettingsWatcher"

    def __init__(self, worker_id, reload_event):
        super(SettingsCheck, self).__init__(worker_id)
        self.settings_version = self.get_settings_version()
        self.reload_event = reload_event

    @staticmethod
    def get_settings_version():
        try:
            settings_version = plugin_settings.NOTIFICATIONS_SETTINGS_VERSION
        except Exception as e:
            LOG.exception(e)
            settings_version = 0
        return settings_version

    def run(self):
        while True:
            try:
                if self.settings_version != self.get_settings_version():
                    LOG.info('Settings version changed. Sending reload signal')
                    self.settings_version = self.get_settings_version()
                    self.reload_event.set()
                    self.reload_event.clear()
            except Exception as e:
                LOG.exception(e)
            time.sleep(5)


class OsOperations(cotyledon.Service):
    name = 'OsOperations'

    def __init__(self, worker_id, reload_event):
        super().__init__(worker_id)
        for app_config in apps.apps.get_app_configs():  # type: apps.AppConfig
            if hasattr(app_config, 'initialize_operations') and callable(app_config.initialize_operations):
                app_config.initialize_operations()

        self.reload_event = reload_event

    def run(self):
        while True:
            operations = Operation.objects.filter(completed=False)
            for operation in operations:
                params = json.loads(operation.params)
                operation_class = operations_factory.initialize_class(
                    recurring_operation_type=operation.operation_type, db_operation=operation,
                )
                if operation_class:
                    operation_class.run(**params)
            time.sleep(5)


def run_app():
    # set lock file
    # NOTE: file may already be locked if someone tries to check it's locked status by trying to lock it again,
    #   this is why we try several times to lock the file in case it couldn't lock it
    lock_file_retries = 5
    lock_file_success = False
    error_msg = 'Could not set lock on updated_lock.pid file. Updated status may show as not running in staff panel.'
    while lock_file_retries and lock_file_success is False:
        try:
            fp = open(getattr(django_settings, 'UPDATED_LOCK_FILE', '/var/fleio/updated_lock.pid'), 'a+')
        except FileNotFoundError:
            error_msg = 'Could not create updated_lock.pid file'
            break
        try:
            fcntl.flock(fp.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except IOError:
            lock_file_success = False
        else:
            # locking file succeeded
            lock_file_success = True
        lock_file_retries -= 1
        if lock_file_success is False:
            # wait only if we could not set the lock
            time.sleep(2)
    if not lock_file_success:
        LOG.error(error_msg)

    reload_event = multiprocessing.Event()
    p = cotyledon.ServiceManager()
    p.add(UpdatedService, kwargs={'reload_event': reload_event})
    p.add(SettingsCheck, kwargs={'reload_event': reload_event})
    p.add(OsOperations, kwargs={'reload_event': reload_event})
    p.run()


if __name__ == '__main__':
    run_app()
