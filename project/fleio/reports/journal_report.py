import datetime
import decimal
import logging

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models.functions import Coalesce

from fleio.billing.models import Invoice, Service
from fleio.billing.models import Journal
from fleio.billing.models.journal_sources import JournalSources
from fleio.billing.modules.factory import module_factory
from fleio.billing.settings import BillingItemTypes, ProductType
from fleio.billing.usage_settings import UsageSettings
from fleio.billing.utils import cdecimal
from fleio.core.features import staff_active_features
from fleio.core.models import Client
from fleio.billing import utils

LOG = logging.getLogger(__name__)


class JournalReport:
    @staticmethod
    def get_default_location():
        return getattr(settings, 'REPORTING_DEFAULT_LOCATION')

    @staticmethod
    def get_invoice_items_percent(invoice: Invoice):
        items_percent = {}
        for item in invoice.items_with_taxes_amount():
            item_total = item.taxes_amount + item.amount
            item_taxes_amount = item.taxes_amount
            if item_total == 0:
                item_percent = 0
            else:
                item_percent = item_total * 100 / invoice.total
            if invoice.total == 0:
                tax_percent = 0
            else:
                tax_percent = item_taxes_amount * 100 / invoice.total
            if item_percent < 0:
                # Always make the percent positive
                item_percent *= -1
            items_percent[item.id] = {'percent': cdecimal(item_percent, q='.01'),
                                      'taxes_amount': cdecimal(item.taxes_amount, q='.01'),
                                      'taxes_percent': cdecimal(tax_percent, q='.01')}
        return items_percent

    @staticmethod
    def get_percent_per_location(location_cost: dict, total_revenue: decimal.Decimal):
        revenue_per_location = {}  # dict {location_name: {cost: x, percent: y, alloted: z}}
        number_of_locations = len(location_cost.keys())
        if number_of_locations > 0:
            location_percent = cdecimal(100 / number_of_locations, q='0.01')
        else:
            location_percent = 100
        for location, cost in location_cost.items():
            if location not in revenue_per_location:
                revenue_per_location[location] = {'cost': cost,
                                                  'percent': decimal.Decimal('0.00'),
                                                  'alloted': decimal.Decimal('0.00')}
            revenue_per_location[location]['percent'] = location_percent
            alloted = location_percent / 100 * total_revenue
            alloted = cdecimal(alloted, q='0.01')
            revenue_per_location[location]['alloted'] = alloted
        return revenue_per_location

    @staticmethod
    def _calculate_amount_for_services(client, services_report, report, total_still_required_cost,
                                       client_available_credit, total_debt, total_credit_alloted, end_date):
        try:
            from fleio.osbilling.bin.collectorlib import service_usage
            from fleio.osbilling.bin.collectorlib import add_pricing
            from fleio.osbilling.bin.collectorlib import collect_project_metrics
            from fleio.osbilling.bin.collectorlib import collect_internal_usage
        except ImportError:
            return services_report, report
        total_credit_alloted_for_os = decimal.Decimal('0.00')
        for service_id, service_report in services_report.items():
            cost_still_required = service_report['cost_still_required']
            service_required_cost = service_report['service_required_cost']
            if service_required_cost != 0:
                if total_still_required_cost > 0:
                    sr_percent = ((service_report['cost_still_required'] * 100) / total_still_required_cost)
                else:
                    sr_percent = 100
                sr_percent = cdecimal(sr_percent, q='.01')
                service_report['cost_required_percent'] = sr_percent

                if service_report.get('service_type', '') == ProductType.openstack:
                    # TODO(low priority): for multiple openstack services/client, debt and revenue should be
                    #  calculated using sr_percent

                    # calculate client_consumed_credit which represents the credit consumed in a month that was
                    # actually paid using the following steps:
                    #   get unpaid usage from last cycle to end_date (firs of month, when report is generated)
                    #   using that information, calculate uptodate credit at that moment:
                    #       (available_credit at that moment - unpaid usage)
                    #   after that, calculate debt using information from above and consumption in that month
                    db_service = Service.objects.filter(id=service_id).first()
                    if not db_service:
                        unpaid_usage = decimal.Decimal('0.00')
                    else:
                        try:
                            unpaid_usage_dict = service_usage(
                                start_date=service_report['service_last_cycle'],
                                end_date=end_date,
                                service_dynamic_usage=db_service.service_dynamic_usage,
                            )
                            unpaid_usage_dict['metrics_details'] = collect_project_metrics(
                                start=service_report['service_last_cycle'],
                                end=end_date,
                                service_dynamic_usage=db_service.service_dynamic_usage,
                            )
                            if staff_active_features.is_enabled('openstack.instances.traffic'):
                                # TODO: check for feature inside the collect method
                                collect_internal_usage(
                                    usage_data=unpaid_usage_dict,
                                    service_dynamic_usage=db_service.service_dynamic_usage,
                                    start=service_report['service_last_cycle'],
                                    end=end_date,
                                )
                            usage_settings = UsageSettings(billing_settings=client.billing_settings)
                            add_pricing(unpaid_usage_dict, client, usage_settings=usage_settings)
                            unpaid_usage = unpaid_usage_dict.get('price', decimal.Decimal('0.00'))
                        except (Exception, AttributeError):
                            unpaid_usage = decimal.Decimal('0.00')
                    if unpaid_usage is None:
                        LOG.error('Something went wrong when collecting unpaid usage for the period between service '
                                  'last cycle date and the end of month for report ({}). Report for client {} may not '
                                  'reflect reality for that period.'.format(str(end_date), client.id))
                        unpaid_usage = decimal.Decimal('0.00')

                    client_utd_credit_at_the_moment = client_available_credit - unpaid_usage
                    client_consumed_credit = client_available_credit - client_utd_credit_at_the_moment
                    # calculations for debt then revenue
                    if client_utd_credit_at_the_moment < 0:
                        service_debt = client_utd_credit_at_the_moment * (-1)
                    elif client_consumed_credit >= cost_still_required:
                        service_debt = client_consumed_credit - cost_still_required
                    else:
                        service_debt = client_consumed_credit
                        if client_available_credit > 0:
                            service_debt *= (-1)
                else:
                    # handle services not related to openstack
                    service_debt = cost_still_required - service_report['total_revenue']
                    if service_debt > 0:
                        service_debt = cost_still_required  # invoice is not paid, thus service "debt" is cost still req
                # NOTE: service debt will result in:
                # negative value: means an old debt was paid before, will be added to alloted_from_credit (revenue)
                # positive value: means there is debt, for non-os services this will be however zeroed
                # zero value: there is no debt
                partial_debt = cdecimal(service_debt, q='0.01')  # used to calculate revenue (alloted_from_credit)
                if service_debt > 0:
                    # Only take into account positive debt
                    if service_report.get('service_type', '') == ProductType.openstack:
                        service_debt = cdecimal(service_debt, q='0.01')
                    else:
                        # for non-os services, debt does not exist
                        service_debt = decimal.Decimal('0.00')
                else:
                    service_debt = decimal.Decimal('0.00')
                service_report['debt'] = service_debt
                total_debt += service_debt

                alloted_from_credit = cost_still_required - partial_debt
                # recalculate alloted from credit based on other services
                no_of_services_with_cost = 0
                latest_service_with_cost = None

                if service_report.get('service_type', '') == ProductType.openstack:
                    for service_id_helper, service_report_helper in services_report.items():
                        if (service_report_helper.get('usage_details', {}).get(
                                'total_cost', decimal.Decimal('0.00')) > decimal.Decimal('0.00')):
                            latest_service_with_cost = service_id_helper
                            no_of_services_with_cost = no_of_services_with_cost + 1

                    if service_id != latest_service_with_cost:
                        service_percent = cdecimal(str(100 / no_of_services_with_cost / 100), q='.001')
                        alloted_from_credit = alloted_from_credit * service_percent
                    else:
                        alloted_from_credit = alloted_from_credit - total_credit_alloted_for_os  # until now
                    total_credit_alloted_for_os += alloted_from_credit

                service_report['alloted_from_credit'] = cdecimal(alloted_from_credit, q='.01')
                total_credit_alloted += alloted_from_credit
            else:
                service_report['cost_required_percent'] = decimal.Decimal('0.00')
                service_report['alloted_from_credit'] = decimal.Decimal('0.00')
                service_report['debt'] = decimal.Decimal('0.00')
        report['total_debt'] = cdecimal(total_debt, q='.01')
        report['total_alloted_from_credit'] = cdecimal(total_credit_alloted, q='.01')
        return services_report, report

    @staticmethod
    def _get_next_due_date(service, until_date: datetime.datetime):
        """gets service next_due_date but the one before the until_date datetime variable"""
        next_due_date = service.next_due_date
        if not next_due_date:
            return None
        if next_due_date == utils.DATETIME_MAX:
            return next_due_date
        while next_due_date > until_date:
            next_due_date = service.get_previous_due_date(next_due_date=next_due_date)

        return next_due_date

    @staticmethod
    def get_client_revenue(client: Client, start_date: datetime.datetime, end_date: datetime.datetime):
        """Get all client revenue that should be included in the report"""
        services_report = {}
        report = {'client': client.id,
                  'client_display_name': client.long_name,
                  'services_report': services_report,
                  'credit_in': decimal.Decimal('0.00'),
                  'credit_out': decimal.Decimal('0.00'),
                  'credit_available': decimal.Decimal('0.00')}
        client_main_credit_account = client.credits.filter(currency=client.currency).first()

        if client_main_credit_account:
            # set the last available credit for the given period
            last_journal_entry = Journal.objects.filter(
                Q(date_added__lt=end_date) & (Q(client_credit=client_main_credit_account) | Q(invoice__client=client))
            ).order_by('date_added').last()
            if (last_journal_entry and last_journal_entry.client_credit_left and
                    last_journal_entry.client_credit_left_currency.code == client_main_credit_account.currency.code):
                report['credit_available'] = last_journal_entry.client_credit_left
            else:
                # TODO(manu): This conditional branch will not work when re-generating for older months if a fleio
                #   installation exists from a longer time (there are no journal entries that report the credit_
                #   available after that journal entry). To fix this, calculate client_credit_left for each journal
                #   entry since beginning of time in a migration
                report['credit_available'] = client_main_credit_account.amount
        # Add each service to the report and it's usage details given by it's billing module
        # if available.
        for service in client.services.filter(Q(terminated_at__isnull=True) |
                                              Q(terminated_at__lt=end_date)):
            fixed_monthly_price = cdecimal(service.get_fixed_price(), q='.01')  # returns fixed or overriden price
            services_report[service.id] = {'service_name': service.display_name,
                                           'service_id': service.id,
                                           'service_type': service.product.product_type,
                                           'service_last_cycle': JournalReport._get_next_due_date(
                                               service=service, until_date=end_date
                                           ),
                                           'entries': [],
                                           'fixed_monthly_price': fixed_monthly_price,  # fixed or overriden price
                                           'price_overridden': service.is_price_overridden,
                                           'total_revenue': decimal.Decimal('0.00'),
                                           'total_from_credit': decimal.Decimal('0.00')}

            # Get the report module for each service if it exists, in order to get a detailed location usage
            service_module = module_factory.get_module_instance(service=service)
            services_report[service.id]['usage_details'] = service_module.get_service_report(service,
                                                                                             start_date,
                                                                                             end_date)
        # Gather journal entries and split out credit and direct service payments through invoices
        if client_main_credit_account:
            # All credit entries that need to appear on the report
            credit_qs = Journal.objects.filter(date_added__gte=start_date,
                                               date_added__lt=end_date,
                                               client_credit=client_main_credit_account)
            credit_in_qs = credit_qs.filter(destination=JournalSources.credit,
                                            source__in=[JournalSources.external,
                                                        JournalSources.transaction])
            credit_in_qs = credit_in_qs.aggregate(dest_amount=Coalesce(models.Sum('destination_amount'), 0))
            credit_amount_in = credit_in_qs.get('dest_amount', 0)
            credit_out_qs = credit_qs.filter(source=JournalSources.credit,
                                             destination__in=[JournalSources.external,
                                                              JournalSources.transaction])
            credit_out_qs = credit_out_qs.aggregate(source_amount=Coalesce(models.Sum('source_amount'), 0))
            credit_amount_out = credit_out_qs.get('source_amount', 0)
            report['credit_in'] += credit_amount_in
            report['credit_out'] += credit_amount_out
        # Revenue from invoices:
        invoice_journal_qs = Journal.objects.filter(invoice__client=client,
                                                    date_added__gte=start_date,
                                                    date_added__lt=end_date).order_by('date_added')
        invoice_journal_qs = invoice_journal_qs.filter(Q(source=JournalSources.invoice,
                                                         destination__in=[JournalSources.external,
                                                                          JournalSources.transaction]) |
                                                       Q(destination=JournalSources.invoice,
                                                         source__in=[JournalSources.external,
                                                                     JournalSources.transaction,
                                                                     JournalSources.staff, ])).all()
        for journal_entry in invoice_journal_qs:
            invoice = journal_entry.invoice
            items_percent = JournalReport.get_invoice_items_percent(invoice=invoice)
            for item in invoice.items.all():
                if item.service:
                    if item.service.id in services_report:
                        if items_percent[item.id]['percent'] != 0:
                            amount = items_percent[item.id]['percent'] / 100 * journal_entry.destination_amount
                            taxamt = items_percent[item.id]['taxes_percent'] / 100 * journal_entry.destination_amount
                            amount -= taxamt
                            if journal_entry.destination in [JournalSources.transaction, JournalSources.external]:
                                amount = -1 * amount
                            amount = cdecimal(amount, q='.01')
                            taxamt = cdecimal(taxamt, q='.01')
                            services_report[item.service.id]['entries'].append({'amount': amount,
                                                                                'item_type': item.item_type,
                                                                                'from_credit': False,
                                                                                'taxes_amount': taxamt,
                                                                                'taxes_percent':
                                                                                    items_percent[item.id][
                                                                                        'taxes_percent'],
                                                                                'source': journal_entry.source,
                                                                                'date': str(journal_entry.date_added)})
                            services_report[item.service.id]['total_revenue'] += amount
                    else:
                        amount = items_percent[item.id]['percent'] / 100 * journal_entry.destination_amount
                        taxamt = items_percent[item.id]['taxes_percent'] / 100 * journal_entry.destination_amount
                        amount -= taxamt
                        if journal_entry.destination in [JournalSources.transaction, JournalSources.external]:
                            amount = -1 * amount
                        amount = cdecimal(amount, q='.01')
                        taxamt = cdecimal(taxamt, q='.01')
                        services_report[item.service.id] = {'entries': [{'amount': amount,
                                                                         'item_type': item.item_type,
                                                                         'from_credit': False,
                                                                         'taxes_amount': taxamt,
                                                                         'taxes_percent': items_percent[item.id][
                                                                             'taxes_percent'],
                                                                         'source': journal_entry.source,
                                                                         'date': str(journal_entry.date_added)}],
                                                            'service': item.service.display_name,
                                                            'total_revenue': amount,
                                                            'total_from_credit': decimal.Decimal('0.00')}

        # Credit entries for each service
        cservice_qs = Journal.objects.filter(date_added__gte=start_date,
                                             date_added__lt=end_date,
                                             client_credit=client_main_credit_account)
        cservice_qs = cservice_qs.filter(Q(source=JournalSources.credit,
                                           destination=JournalSources.invoice) |
                                         Q(source=JournalSources.invoice,
                                           destination=JournalSources.credit)).all()

        for journal_entry in cservice_qs:
            invoice = journal_entry.invoice
            items_percent = JournalReport.get_invoice_items_percent(invoice=invoice)
            for item in invoice.items.all():
                if item.service:
                    if item.service.id in services_report:
                        if items_percent[item.id]['percent'] != 0:
                            amount = items_percent[item.id]['percent'] / 100 * journal_entry.destination_amount
                            taxamt = items_percent[item.id]['taxes_percent'] / 100 * journal_entry.destination_amount
                            amount -= taxamt
                            if journal_entry.destination == JournalSources.credit:
                                amount = -1 * amount
                            amount = cdecimal(amount, q='.01')
                            taxamt = cdecimal(taxamt, q='.01')
                            credit_entries = services_report[item.service.id]['entries']
                            credit_entries.append({'amount': amount,
                                                   'item_type': item.item_type,
                                                   'from_credit': True,
                                                   'taxes_amount': taxamt,
                                                   'taxes_percent': items_percent[item.id]['taxes_percent'],
                                                   'source': journal_entry.source,
                                                   'date': str(journal_entry.date_added)})
                            services_report[item.service.id]['total_revenue'] += amount
                            services_report[item.service.id]['total_from_credit'] += (amount + taxamt)
                    else:
                        amount = items_percent[item.id]['percent'] / 100 * journal_entry.destination_amount
                        taxamt = items_percent[item.id]['taxes_percent'] / 100 * journal_entry.destination_amount
                        amount -= taxamt
                        if journal_entry.destination == JournalSources.credit:
                            amount = -1 * amount
                        amount = cdecimal(amount, q='.01')
                        taxamt = cdecimal(taxamt, q='.01')
                        credit_entries = [{'amount': amount,
                                           'item_type': item.item_type,
                                           'from_credit': True,
                                           'taxes_amount': taxamt,
                                           'taxes_percent': items_percent[item.id]['taxes_percent'],
                                           'source': journal_entry.source,
                                           'date': str(journal_entry.date_added)}]
                        services_report[item.service.id] = {'entries': credit_entries,
                                                            'service': item.service.display_name,
                                                            'total_revenue': decimal.Decimal('0.00'),
                                                            'total_from_credit': amount + taxamt}
                elif item.item_type == BillingItemTypes.credit:
                    if journal_entry.destination == JournalSources.invoice:
                        report['credit_out'] += item.amount
                    else:
                        report['credit_in'] += item.amount
        # Gether all credit used by services
        # The credit is split proportional to each service, based on it's usage report
        client_available_credit = report['credit_available']
        total_still_required_cost = decimal.Decimal('0.00')
        total_required_cost = decimal.Decimal('0.00')
        total_debt = decimal.Decimal('0.00')
        total_credit_alloted = decimal.Decimal('0.00')
        for service_id, service_report in services_report.items():
            price_overridden = service_report['price_overridden'] if 'price_overridden' in service_report else False
            total_revenue = service_report['total_revenue']
            if price_overridden:
                # If pirice is overridden, the service total cost is the fixed price one - entries for it
                service_required_cost = service_report['fixed_monthly_price']
                service_report['service_required_cost'] = cdecimal(service_required_cost, q='.01')
                cost_still_required = service_required_cost - total_revenue
                cost_still_required = cdecimal(cost_still_required, q='.01')
                service_report['cost_still_required'] = cost_still_required
            else:
                # Add here logic for dynamic but minimum fixed
                fixed_monthly_price = (service_report['fixed_monthly_price'] if 'fixed_monthly_price' in service_report
                                       else decimal.Decimal('0.00'))
                usage_details = (service_report['usage_details'] if 'usage_details' in service_report
                                 else {})
                service_required_cost = (fixed_monthly_price +
                                         usage_details.get('total_cost', decimal.Decimal('0.00')))
                cost_still_required = service_required_cost - total_revenue
                cost_still_required = cdecimal(cost_still_required, q='.01')
                service_report['service_required_cost'] = cdecimal(service_required_cost, q='.01')
                service_report['cost_still_required'] = cost_still_required
            # Create a total amount so we can deduct from credit available and calculate the percentage
            total_required_cost += service_required_cost
            total_still_required_cost += cost_still_required

        # Calculate the percentage, debts, credit alloted of each service
        services_report, report = JournalReport._calculate_amount_for_services(
            client=client, services_report=services_report, report=report,
            total_still_required_cost=total_still_required_cost, client_available_credit=client_available_credit,
            total_debt=total_debt, total_credit_alloted=total_credit_alloted, end_date=end_date
        )
        # Go through each service to get the totals per region
        revenue_per_location = {}
        default_location = JournalReport.get_default_location()
        for service_id, service_report in services_report.items():
            # Set an equal percent for each location
            usage_details = service_report.get('usage_details', {})
            if type(usage_details) is dict and usage_details.keys():
                # Deal with services that have usage_details
                location_cost = usage_details.get('location_cost')
                total_revenue = service_report['alloted_from_credit']
                service_location_alloted = JournalReport.get_percent_per_location(location_cost, total_revenue)
                for location_name, costs in service_location_alloted.items():
                    if location_name not in revenue_per_location:
                        revenue_per_location[location_name] = decimal.Decimal('0.00')
                    revenue_per_location[location_name] += costs['alloted']
            else:
                if default_location not in revenue_per_location:
                    revenue_per_location[default_location] = decimal.Decimal('0.00')
                total_revenue = service_report['alloted_from_credit']
                revenue_per_location[default_location] += total_revenue
        report['revenue_per_location'] = [{'name': name, 'revenue': cdecimal(revenue, q='.01')}
                                          for name, revenue in revenue_per_location.items()]

        return report
