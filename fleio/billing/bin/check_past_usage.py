import copy
import datetime
from os import environ
from os.path import abspath, dirname
import argparse
import sys
import django
import pytz


current_path = dirname(abspath(__file__))
fleio_path = dirname(dirname(dirname(current_path)))
sys.path.append(fleio_path)
environ.setdefault("DJANGO_SETTINGS_MODULE", "fleio.settings")
django.setup()

from fleio.osbilling.models import ServiceDynamicUsageHistory  # noqa
from fleio.billing.usage_settings import UsageSettings  # noqa
from fleio.billing.models import Journal  # noqa
from fleio.billing.models.journal_sources import JournalSources  # noqa
from fleio.conf.models import Configuration  # noqa


LOG_PATH = '/var/fleio/past_usage_checker.log'


class Colors:
    reset = '\033[0m'
    red = '\033[31m'
    green = '\033[32m'
    orange = '\033[33m'


def negative_number(number: str) -> str:
    # colorize negative numbers in red
    return '{}{}{}'.format(Colors.red, number, Colors.reset)


def positive_number(number: str) -> str:
    # colorize positive numbers in green
    return '{}{}{}'.format(Colors.green, number, Colors.reset)


class Status:
    usage_fixed_and_charged = Colors.green + 'USAGE FIXED + CHARGED' + Colors.reset
    usage_fixed = Colors.green + 'USAGE FIXED' + Colors.reset
    no_action = Colors.orange + 'NO ACTION' + Colors.reset


def _localize_and_make_aware_to_utc(date_to_localise):
    if isinstance(date_to_localise, datetime.date):
        # transform to datetime if necessary (required for filtering resource usage logs in client_usage)
        date_to_localise = datetime.datetime.combine(date_to_localise, datetime.datetime.min.time())
    return date_to_localise.replace(tzinfo=pytz.utc)


def run(start, requested_client_ids=None, subtract=False, configurations=None):

    # TABLE DATA TITLES
    titles = ['ID', 'NAME', 'BILLING CYCLE START', 'BILLING CYCLE END', 'DIFFERENCE']
    ids = []
    names = []
    bc_start = []
    bc_end = []
    difference = []
    status = []

    if not start:
        sys.exit('You need to specify start date')
    filter_params = {
        'start_date__gte': start.date()
    }
    if requested_client_ids:
        # only calculate usage differences for clients in this list
        filter_params['service_dynamic_usage__service__client__id__in'] = requested_client_ids
    service_dynamic_usage_histories = ServiceDynamicUsageHistory.objects.filter(**filter_params)
    try:
        from fleio.osbilling.bin.collectorlib import service_usage
        from fleio.osbilling.bin.collectorlib import add_pricing
        from fleio.osbilling.bin.collectorlib import collect_project_metrics
    except ImportError:
        sys.exit('ERROR: Check your license')
    total_diff_to_subtract = 0  # sum of usage that was not calculated in past client billing histories
    for sduh in service_dynamic_usage_histories:
        client = sduh.service_dynamic_usage.service.client
        service_dynamic_usage_settings = client.billing_settings
        calculate_for_client = True
        if configurations:
            # only run for clients in given configurations
            try:
                db_conf = Configuration.objects.get(id=service_dynamic_usage_settings.configuration_id)
            except Configuration.DoesNotExist:
                calculate_for_client = False
            else:
                if not (db_conf.name in configurations):
                    calculate_for_client = False
        if calculate_for_client:
            start_date = _localize_and_make_aware_to_utc(sduh.start_date)
            end_date = _localize_and_make_aware_to_utc(sduh.end_date)
            # start calculating usage
            usage_dict = service_usage(start_date, end_date, sduh.service_dynamic_usage)
            usage_dict['metrics_details'] = collect_project_metrics(
                start_date, end_date, sduh.service_dynamic_usage
            )
            usage_settings = UsageSettings(billing_settings=service_dynamic_usage_settings)
            add_pricing(usage_dict, client, usage_settings=usage_settings)
            # TODO: add traffic and other usage calculations if necessary
            usage_price = usage_dict.get('price', None)
            calculated_diff = usage_price - sduh.price  # now calculated usage - billing history saved one
            charged = False  # variable to remember if we charged the missing money
            usage_fixed = False  # variable to remember if we fixed his usage in this billing history cycle
            client_name = '{} {}'.format(client.first_name, client.last_name)
            if calculated_diff < 0:
                # for now, for differences resulting in negative amounts, we just log them and take no action
                # may actually be suspended clients, or resource usage logs were tampered with
                # those need manual review
                ids.append(client.id)
                names.append(client_name[:28])
                bc_start.append('{}'.format(sduh.start_date))
                bc_end.append('{}'.format(sduh.end_date))
                difference.append(negative_number(str(calculated_diff)))
                status.append(Status.no_action)
            if calculated_diff > 0:
                ids.append(client.id)
                names.append(client_name[:28])
                bc_start.append('{}'.format(sduh.start_date))
                bc_end.append('{}'.format(sduh.end_date))
                difference.append(positive_number(str(calculated_diff)))
                total_diff_to_subtract = total_diff_to_subtract + calculated_diff
                if subtract:
                    # UPDATE THE BILLING HISTORY RECORD
                    usage_to_save = copy.deepcopy(usage_dict)
                    for r in usage_to_save['usage_details']:
                        for res in r['usage']:
                            for hist in res['history']:
                                hist['rule'] = hist['rule'].id
                                for modifier in hist['modifiers']:
                                    modifier['modifier'] = modifier['modifier'].id
                    sduh.usage = usage_to_save
                    sduh.price = usage_price
                    sduh.save()
                    usage_fixed = True
                    if sduh.state != 'unsettled':
                        # charge missing money from client only if his billing history was settled, otherwise the
                        # difference will be settled correctly on next settlement date, or up to date credit for client
                        # will be correctly recalculated in case all of client's billing histories are unsettled when
                        # clients cron runs again
                        if service_dynamic_usage_settings.generate_invoices:
                            # TODO: generate invoice if necessary
                            pass
                        if service_dynamic_usage_settings.auto_settle_usage:
                            # TODO: add tax rules calculations if necessary
                            sduh.service_dynamic_usage.client.withdraw_credit(calculated_diff, client.currency)
                            client_credit_account = client.credits.get(
                                client=sduh.service_dynamic_usage.service.client,
                                currency=sduh.service_dynamic_usage.service.client.currency
                            )
                            Journal.objects.create(client_credit=client_credit_account,
                                                   transaction=None,
                                                   source_currency=client.currency,
                                                   destination_currency=client.currency,
                                                   source=JournalSources.credit,
                                                   destination=JournalSources.settlement,
                                                   source_amount=calculated_diff,
                                                   destination_amount=calculated_diff)
                            charged = True
                # show status for client after running the script
                if charged:
                    status.append(Status.usage_fixed_and_charged)
                elif usage_fixed:
                    status.append(Status.usage_fixed)
                else:
                    status.append(Status.no_action)

    data = [titles] + list(zip(ids, names, bc_start, bc_end, difference, status))
    with open(LOG_PATH, 'w') as log_file:
        for i, d in enumerate(data):
            line = ''.join(str(x).ljust(30) for x in d)
            log_file.write(line)
            log_file.write('\n')
            if i == 0:
                log_file.write('-' * len(line))
                log_file.write('\n')
        log_file.write('\nTOTAL DIFFERENCE TO SUBTRACT: {}\n'.format(positive_number(str(total_diff_to_subtract))))

    sys.exit(LOG_PATH)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--after', '-a',
        help="Check all billing cycles that have ended after this date. Date format is: YYYY-MM-DD.",
        type=str
    )
    parser.add_argument(
        '--clients', '-c',
        help="List of clients, comma separated",
        type=str
    )
    parser.add_argument(
        '--subtract', '-s',
        help="If the re-calculated current costs is higher: update the past billing cycle and subtract the "
             "difference from each client's credit balance if the related billing history was already settled.",
        action='store_true'
    )
    parser.add_argument(
        '--configurations', '-co',
        help="Run the script only for clients in the comma separated list of configurations.",
        type=str
    )
    args = parser.parse_args()
    if len(sys.argv) > 1:
        try:
            date = datetime.datetime.strptime(args.after, '%Y-%m-%d')
            client_ids = args.clients.strip().split(',') if args.clients else None
            if client_ids:
                for client_id in client_ids:
                    db_client = ServiceDynamicUsageHistory.objects.filter(
                        service_dynamic_usage__service__client__id=client_id
                    ).first()
                    if not db_client:
                        sys.exit('Could not find billing histories for client id: {}'.format(client_id))
            run(
                start=_localize_and_make_aware_to_utc(date_to_localise=date),
                requested_client_ids=client_ids,
                subtract=args.subtract,
                configurations=args.configurations.strip().split(',') if args.configurations else None,
            )
        except ValueError as e:
            sys.exit('First argument must be in the YYYY-MM-DD format')
        except Exception as e:
            sys.exit(str(e))
    else:
        sys.exit('First argument must be in the YYYY-MM-DD format')
