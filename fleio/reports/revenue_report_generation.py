import datetime
import pytz

from django.utils.translation import ugettext_lazy as _
from django.db import transaction
from django.conf import settings

from fleio.billing.modules.factory import module_factory
from fleio.reports.models import MonthlyRevenueReport
from fleio.reports.tasks import generate_revenue_report as generate_revenue_report_task
from fleio.reports.exceptions import InvalidArgument, ReportIsAlreadyGenerating, RevenueReportTimezoneError


def generate_revenue_report(month_and_year: str):
    if '/' not in month_and_year:
        raise InvalidArgument(_('Invalid argument. Argument should be month/year, eg: 03/2019.'))
    month_and_year = month_and_year.split('/')
    month = month_and_year[0]
    year = month_and_year[1]
    try:
        month = int(month)
        year = int(year)
    except ValueError:
        raise InvalidArgument(_('Invalid argument: month and year have to be digits.'))
    if month < 1 or month > 12:
        raise InvalidArgument(_('Invalid date: month has to be a number between 1 and 12.'))
    today = datetime.datetime.now()
    current_month = today.month
    current_year = today.year
    if (month > current_month and year == current_year) or year > current_year:
        raise InvalidArgument(_('Invalid date: you cannot generate report for months in the future.'))
    module_factory.refresh_modules()

    # set start and end date based on REVENUE_REPORTING_TIMEZONE set in django settings
    revenue_reporting_timezone = getattr(settings, 'REVENUE_REPORTING_TIMEZONE', None)
    if not revenue_reporting_timezone:
        # if above doesn't exist, use the default django TIME_ZONE setting
        revenue_reporting_timezone = getattr(settings, 'TIME_ZONE', None)
    if not revenue_reporting_timezone:
        raise RevenueReportTimezoneError(_('Revenue reporting time zone setting is missing or incorrect.'))
    if revenue_reporting_timezone not in pytz.all_timezones_set:
        raise RevenueReportTimezoneError(_('Revenue reporting time zone setting is missing or incorrect.'))
    tz_info = pytz.timezone(revenue_reporting_timezone)
    if (month + 1) > 12:
        end_month = 1
        end_year = year + 1
    else:
        end_month = month + 1
        end_year = year
    report_end_date = datetime.datetime(
        year=end_year, month=end_month, day=1, hour=0, minute=0, second=0, microsecond=0
    )
    report_end_date_aware = tz_info.localize(report_end_date)
    report_end_date_aware_to_utc = report_end_date_aware.astimezone(pytz.utc)  # represent the aware datetime as UTC

    report_start_date = datetime.datetime(
        year=year, month=month, day=1, hour=0, minute=0, second=0, microsecond=0
    )
    report_start_date_aware = tz_info.localize(report_start_date)
    report_start_date_aware_to_utc = report_start_date_aware.astimezone(pytz.utc)  # represent the aware datetime as UTC
    with transaction.atomic():
        try:
            monthly_report = MonthlyRevenueReport.objects.select_for_update().get(end_date=report_end_date_aware_to_utc)
            if monthly_report.generating is True:
                raise ReportIsAlreadyGenerating(_('Report for the given month is already generating.'))
            monthly_report.generating = True
            monthly_report.save()
        except MonthlyRevenueReport.DoesNotExist:
            monthly_report = MonthlyRevenueReport.objects.create(
                start_date=report_start_date_aware_to_utc, end_date=report_end_date_aware_to_utc, generating=True
            )
    generate_revenue_report_task.delay(monthly_report_id=monthly_report.id)
