import calendar
from datetime import date as date_type

from fleio.billing.settings import BillingSettings


class UsageSettings(object):
    def __init__(self, billing_settings: BillingSettings):
        self.limit_billable_seconds_per_month = billing_settings.limit_billable_seconds_per_month
        self.billable_seconds_per_month = billing_settings.billable_seconds_per_month
        self.billing_cycle_as_calendar_month = billing_settings.billing_cycle_as_calendar_month

    def get_billable_seconds_for_month(self, year: int, month: int) -> int:
        month_days = calendar.monthrange(year=year, month=month)[1]
        month_seconds = month_days * 24 * 3600

        if self.limit_billable_seconds_per_month:
            return min(month_seconds, self.billable_seconds_per_month)
        else:
            return month_seconds

    def get_billable_seconds_for_date(self, date: date_type):
        return self.get_billable_seconds_for_month(year=date.year, month=date.month)
