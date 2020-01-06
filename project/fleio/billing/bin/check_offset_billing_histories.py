from os import environ
from os.path import abspath, dirname
import argparse
import sys
import django
import datetime
import pytz


current_path = dirname(abspath(__file__))
fleio_path = dirname(dirname(dirname(current_path)))
sys.path.append(fleio_path)
environ.setdefault("DJANGO_SETTINGS_MODULE", "fleio.settings")
django.setup()

from fleio.osbilling.models import ServiceDynamicUsageHistory, ClientBillingStates  # noqa
from fleio.billing.models import Service  # noqa
from fleio.billing.settings import ProductType  # noqa


LOG_PATH = '/var/fleio/client_offset_billing_histories.log'


def run(fix=False):
    # TABLE DATA TITLES
    titles = ['ID', 'NAME', 'SERVICE_STATUS', 'STATUS']
    ids = []
    names = []
    service_status = []
    status = []
    count = 0

    services = Service.objects.filter(product__product_type=ProductType.openstack).order_by('next_due_date')
    for service in services:
        if service.next_due_date:
            if ServiceDynamicUsageHistory.objects.filter(
                    service_dynamic_usage__service=service, state=ClientBillingStates.unsettled
            ).count() == 1:
                sduh = ServiceDynamicUsageHistory.objects.filter(
                    service_dynamic_usage__service=service,
                    state=ClientBillingStates.unsettled,
                    end_date__lt=service.next_due_date,
                ).order_by('start_date').last()
                if sduh:
                    count = count + 1
                    ids.append(service.client.id)
                    names.append(service.client.name)
                    service_status.append(service.status)
                    if fix:
                        date_to_localise = datetime.datetime.combine(sduh.end_date, datetime.time(
                            hour=service.next_due_date.hour,
                            minute=service.next_due_date.minute,
                            second=service.next_due_date.second
                        ))
                        date_to_localise = date_to_localise.replace(tzinfo=pytz.utc)
                        service.next_due_date = date_to_localise
                        service.save(update_fields=['next_due_date'])
                        status.append('FIXED')
                    else:
                        status.append('NO ACTION')

    data = [titles] + list(zip(ids, names, service_status, status))
    with open(LOG_PATH, 'w') as log_file:
        for i, d in enumerate(data):
            line = ''.join(str(x).ljust(30) for x in d)
            log_file.write(line)
            log_file.write('\n')
            if i == 0:
                log_file.write('-' * len(line))
                log_file.write('\n')
        log_file.write('THERE ARE {} CLIENTS BEING BILLED DECALATED\n'.format(count))

    sys.exit(LOG_PATH)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--fix', '-f',
        help="If client was determined that he is being billed decalated, decrease his service next due date",
        action='store_true'
    )
    args = parser.parse_args()
    try:
        run(fix=args.fix if args.fix else False)
    except Exception as e:
        sys.exit(str(e))
