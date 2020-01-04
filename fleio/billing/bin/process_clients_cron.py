import fcntl
import logging
from os import environ
from os.path import abspath, dirname
import sys

import django

current_path = dirname(abspath(__file__))
fleio_path = dirname(dirname(dirname(current_path)))

sys.path.append(fleio_path)
environ.setdefault("DJANGO_SETTINGS_MODULE", "fleio.settings")
django.setup()

LOG = logging.getLogger('cron')

from django.conf import settings  # noqa
from django.utils.timezone import now as utcnow  # noqa
from fleio.activitylog.utils.activity_helper import activity_helper  # noqa

from fleio.billing.client_operations import ClientOperations  # noqa
from fleio.billing.exchange_rate_manager import ExchangeRateManager  # noqa
from fleio.billing.modules.factory import module_factory  # noqa

from fleio.core.features import staff_active_features  # noqa
from fleio.core.models import Client  # noqa
from fleio.core.models import ClientStatus  # noqa
from fleio.core.plugins.plugin_loader import plugin_loader  # noqa


def run():
    lock_file = getattr(settings, 'PROCESS_CLIENT_CRON_LOCK_FILE', '/var/fleio/process_client_cron_lock_file.pid')
    try:
        fp = open(lock_file, 'a+')
    except FileNotFoundError:
        LOG.error('Could not create or open {} lock file'.format(lock_file))
        return
    try:
        fcntl.flock(fp.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError:
        LOG.error('**Process clients cron is already running**')
        return

    if settings.UPDATE_RELATIVE_PRICES_BEFORE_PROCESSING_CLIENTS:
        ExchangeRateManager.update_relative_prices()

    activity_helper.start_generic_activity(
        category_name='cron',
        activity_class='cron process clients',
    )

    resellers_enabled = staff_active_features.is_enabled('billing.reseller')

    for client in Client.objects.all():  # type: Client
        try:
            LOG.debug('Processing client {}'.format(client))

            reference_datetime = utcnow()
            client_operations = ClientOperations(client, reference_datetime=reference_datetime)

            if client.status == ClientStatus.active:
                client_operations.process_client_services()

            client_operations.process_cancellation_requests()

            # update client usage
            client_operations.update_usage()

            # the client is assigned to a suspended reseller, skip some processing
            skip = resellers_enabled and client.reseller_resources
            skip = skip and client.reseller_resources.service.client.status == ClientStatus.suspended

            if not skip:
                if client.status == ClientStatus.suspended:
                    # check if client should be resumed
                    if client_operations.evaluate_and_resume_if_enough_credit():
                        LOG.debug('Client resumed')
                elif client.status == ClientStatus.active:
                    # check if client should be suspended
                    if client_operations.evaluate_and_suspend_if_overdue():
                        LOG.debug('Client suspended')
                    else:
                        client_operations.evaluate_and_send_low_credit_notifications()

            if not skip:
                # if client suspended process possible services with suspend override
                if client.status == ClientStatus.suspended:
                    client_operations.process_services_with_suspend_override()

                client_operations.process_client_suspended_services()

            for message in client_operations.summary.get_formatted_summary():
                LOG.info(message)

        except Exception as e:
            LOG.exception('Error processing client {} - {}'.format(client, e))

    activity_helper.end_activity()


if __name__ == '__main__':
    plugin_loader.refresh_plugins()
    module_factory.refresh_modules()
    run()
