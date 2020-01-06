import datetime
import decimal

from fleio.billing.utils import cdecimal
from fleio.core.models import Client
from fleio.core.models import get_default_currency
from fleio.reports.journal_report import JournalReport
from fleio.reports.models import MonthlyRevenueReport
from fleio.reports.models import ServiceUsageDetailsReport


class LocationReport:
    def __init__(self, start_date: datetime.datetime, end_date: datetime.datetime):
        self.start_date = start_date
        self.end_date = end_date
        self._report = None

    @staticmethod
    def clients_queryset():
        return Client.objects.active()

    def generate_client_report(self, client):
        return JournalReport.get_client_revenue(client=client, start_date=self.start_date, end_date=self.end_date)

    @staticmethod
    def get_report_currency():
        def_c = get_default_currency()
        if not def_c:
            return 'USD'
        else:
            return def_c.code

    def generate_report(self) -> dict:
        entire_report = {'revenue_report': [],
                         'total_revenue_per_location': [],
                         'total_revenue': decimal.Decimal('0.00'),
                         'currency_code': self.get_report_currency(),
                         'start_date': str(self.start_date),
                         'end_date': str(self.end_date)}
        locations_totals = {}
        for client in self.clients_queryset():
            client_report = self.generate_client_report(client=client)
            entire_report['revenue_report'].append(client_report)
            for revenue_per_location in client_report.get('revenue_per_location'):
                location_name = revenue_per_location.get('name')
                if location_name not in locations_totals:
                    locations_totals[location_name] = revenue_per_location.get('revenue')
                else:
                    locations_totals[location_name] += revenue_per_location.get('revenue')
        for location_name, revenue in locations_totals.items():
            # Go through each location and set the final revenue per location
            # necessary since we used a dict prior to allow for faster calculation of totals
            entire_report['total_revenue_per_location'].append({'name': location_name,
                                                                'revenue': revenue})
            # Calculate the total revenue
            entire_report['total_revenue'] += revenue
        entire_report['total_revenue'] = cdecimal(entire_report['total_revenue'])
        return entire_report

    @property
    def report(self):
        if self._report is None:
            self._report = self.generate_report()
        return self._report

    def save_report(self):
        revenue_report = self.report
        # Create the monthly report object if it doesn't exist
        total_revenue = revenue_report['total_revenue']
        currency_code = revenue_report['currency_code']
        monthly_report = MonthlyRevenueReport.objects.filter(end_date=self.end_date).first()
        monthly_report.total_revenue = total_revenue
        monthly_report.currency_code = currency_code
        monthly_report.save()

        # Add the total revenue per location
        monthly_report.total_revenue_per_location.all().delete()
        for total_rev in revenue_report.get('total_revenue_per_location', []):
            monthly_report.total_revenue_per_location.create(name=total_rev['name'],
                                                             revenue=total_rev['revenue'])
        # Clear any previous client reports:
        monthly_report.revenue_report.all().delete()
        # Add each client's revenue report
        for client_report in revenue_report['revenue_report']:
            c_rev_dict = {'start_date': self.start_date,
                          'end_date': self.end_date,
                          'client_id': client_report['client'],
                          'client_display_name': client_report['client_display_name'],
                          'credit_in': client_report['credit_in'],
                          'credit_out': client_report['credit_out'],
                          'credit_available': client_report['credit_available'],
                          'total_debt': client_report['total_debt'],
                          'total_alloted_from_credit': client_report['total_alloted_from_credit']}
            db_client_report = monthly_report.revenue_report.create(**c_rev_dict)
            # Add revenue per location for each client
            db_client_report.revenue_per_location.all().delete()
            for client_revenue_per_location in client_report['revenue_per_location']:
                db_client_report.revenue_per_location.create(name=client_revenue_per_location['name'],
                                                             revenue=client_revenue_per_location['revenue'])

            # Add each service report for this client
            db_client_report.services_report.all().delete()
            for service_id, service_report in client_report['services_report'].items():
                serv_rep_data = {'service_id': service_report['service_id'],
                                 'service_name': service_report['service_name'],
                                 'service_description': '',
                                 'price_overridden': service_report['price_overridden'],
                                 'fixed_monthly_price': service_report['fixed_monthly_price'],
                                 'total_paid_from_invoices': service_report['total_revenue'],
                                 'total_paid_from_credit': service_report['total_from_credit'],
                                 'cost_still_required': service_report['cost_still_required'],
                                 'cost_required_percent': service_report['cost_required_percent'],
                                 'alloted_from_credit': service_report['alloted_from_credit'],
                                 'debt': service_report['debt']}
                db_serv_rep = db_client_report.services_report.create(**serv_rep_data)
                # Add entries credit and/or invoice
                money_entries = service_report.get('entries', [])
                db_serv_rep.entries.all().delete()
                for mentry in money_entries:
                    db_serv_rep.entries.create(**mentry)

                # Add the service usage details
                s_usage_details = service_report.get('usage_details', {})
                if s_usage_details:
                    s_update_details = {'locations': s_usage_details.get('locations'),
                                        'location_costs': s_usage_details.get('location_cost'),
                                        'total_cost': s_usage_details.get('total_cost', decimal.Decimal('0.00'))}
                    ServiceUsageDetailsReport.objects.update_or_create(service_report=db_serv_rep,
                                                                       defaults=s_update_details)
        monthly_report.generating = False
        monthly_report.save()
        return monthly_report
