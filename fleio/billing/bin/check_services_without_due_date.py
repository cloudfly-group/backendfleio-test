import argparse
import datetime
import logging
import sys
from os import environ
from os.path import abspath, dirname

import django
import pytz

current_path = dirname(abspath(__file__))
fleio_path = dirname(dirname(dirname(current_path)))
sys.path.append(fleio_path)
environ.setdefault("DJANGO_SETTINGS_MODULE", "fleio.settings")
django.setup()

from fleio.billing.models import Service  # noqa
from fleio.osbilling.models import ServiceDynamicUsage  # noqa

LOG_PATH = '/var/fleio/services_without_due_date.log'

LOG = logging.getLogger(__name__)


def run(fix=False):
    titles = ['SERVICE_ID', 'CLIENT_NAME', 'SERVICE_STATUS']
    ids = []
    client_names = []
    service_statuses = []
    qs = Service.objects.filter(next_due_date__isnull=True)
    for service in qs:
        client = service.client
        ids.append(service.id)
        client_names.append(client.name)
        service_statuses.append(service.status)
        if fix:
            try:
                service_dynamic_usage = ServiceDynamicUsage.objects.get(service=service)
            except Exception as err:
                LOG.error('Could not determine client billing for client {}, reason: {}'.format(client.id, str(err)))
            else:
                due_date = datetime.date(
                    year=service_dynamic_usage.start_date.year,
                    month=service_dynamic_usage.start_date.month,
                    day=service_dynamic_usage.start_date.day
                )
                if service.created_at:
                    date_to_localise = datetime.datetime.combine(due_date, datetime.time(
                        hour=service.created_at.hour,
                        minute=service.created_at.minute,
                        second=service.created_at.second
                    ))
                    date_to_localise = date_to_localise.replace(tzinfo=pytz.utc)
                else:
                    date_to_localise = datetime.datetime.combine(due_date, datetime.datetime.max.time())
                    date_to_localise = date_to_localise.replace(tzinfo=pytz.utc)
                service.next_due_date = date_to_localise
                service.save()

    data = [titles] + list(zip(ids, client_names, service_statuses))
    with open(LOG_PATH, 'w') as log_file:
        for i, d in enumerate(data):
            line = ''.join(str(x).ljust(30) for x in d)
            log_file.write(line)
            log_file.write('\n')
            if i == 0:
                log_file.write('-' * len(line))
                log_file.write('\n')
        log_file.write('THERE ARE {} SERVICES WITHOUT DUE DATE\n'.format(qs.count()))

    sys.exit(LOG_PATH)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--fix', '-f',
        help="If service has no due date, set it to first day of client billing",
        action='store_true'
    )
    args = parser.parse_args()
    try:
        run(fix=args.fix if args.fix else False)
    except Exception as e:
        sys.exit(str(e))
