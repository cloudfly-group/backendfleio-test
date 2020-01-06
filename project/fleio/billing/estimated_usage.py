import calendar
import copy
from datetime import date
from datetime import datetime
from datetime import time
from datetime import timedelta
from decimal import Decimal
import logging
import math
from typing import Callable
from typing import List

from django.utils import timezone

import fleio.billing.utils as billing_utils
from fleio.billing.usage_settings import UsageSettings

LOG = logging.getLogger(__name__)


class DynamicResource(object):
    def __init__(
            self,
            price_per_second: Decimal,
            price_per_unit: Decimal,
            seconds_per_unit: Decimal,
            start_datetime: datetime
    ):
        self.price_per_second = price_per_second
        self.price_per_unit = price_per_unit
        self.seconds_per_unit = seconds_per_unit
        self.start_datetime = start_datetime
        self.end_datetime = billing_utils.DATETIME_MAX

    def compute_end_datetime(self, cycle_end_time: datetime, max_billable_seconds: int):
        seconds_until_end_of_cycle = (cycle_end_time - self.start_datetime).total_seconds()
        if seconds_until_end_of_cycle >= max_billable_seconds:
            self.end_datetime = self.start_datetime + timedelta(seconds=max_billable_seconds)
        else:
            self.end_datetime = cycle_end_time

    def get_price_per_second(self, reference_datetime: datetime):
        if reference_datetime > self.end_datetime or reference_datetime < self.start_datetime:
            return billing_utils.DECIMAL_ZERO
        else:
            return self.price_per_second


class UsageCycle(object):
    def __init__(
            self,
            fixed_price: Decimal,
            cycle_end_date: date,
            get_next_end_date: Callable[[date], date],
            usage_settings: UsageSettings
    ):
        self.fixed_price = fixed_price
        self.cycle_end_date = cycle_end_date
        self.get_next_end_date = get_next_end_date
        self.dynamic_resources = []
        self.cycle_previous_end_date = date.min
        self.usage_settings = usage_settings

    @property
    def cycle_end_datetime(self):
        if self.usage_settings.billing_cycle_as_calendar_month:
            return datetime.combine(self.cycle_end_date, datetime.max.time()).replace(tzinfo=timezone.utc)
        return datetime.combine(
            self.cycle_end_date,
            time(hour=0, minute=0, second=0)
        ).replace(tzinfo=timezone.utc)

    @property
    def cycle_previous_end_datetime(self):
        return datetime.combine(
            self.cycle_previous_end_date,
            time(hour=0, minute=0, second=0)
        ).replace(tzinfo=timezone.utc)

    @property
    def next_end_datetime(self):
        return min(
            [dynamic_resource.end_datetime for dynamic_resource in self.dynamic_resources] +
            [self.cycle_end_datetime]
        )

    def add_dynamic_resource(
            self,
            price_per_second: Decimal,
            price_per_unit: Decimal,
            seconds_per_unit: Decimal,
            start_datetime: datetime
    ):
        dynamic_resource = DynamicResource(
            price_per_second=price_per_second,
            price_per_unit=price_per_unit,
            seconds_per_unit=seconds_per_unit,
            start_datetime=start_datetime
        )
        dynamic_resource.compute_end_datetime(
            self.cycle_end_datetime,
            self.usage_settings.get_billable_seconds_for_date(start_datetime.date())
        )
        self.dynamic_resources.append(dynamic_resource)

    def add_fixed_price(self, fixed_price: Decimal):
        self.fixed_price += fixed_price

    def get_price_per_second(self, reference_datetime: datetime):
        return sum(
            [dynamic_resource.get_price_per_second(reference_datetime) for dynamic_resource in self.dynamic_resources]
        )

    def get_max_price_per_second(self):
        return sum([dynamic_resource.price_per_second for dynamic_resource in self.dynamic_resources])

    @staticmethod
    def increment_cycle_end(cycle_end_date):
        """Used to determine next cycle end when billing cycle as month is active and start_date and end_date hits the
        same date (last day of month)"""
        if cycle_end_date.month < 12:
            date_month = cycle_end_date.month + 1
            date_year = cycle_end_date.year
        else:
            # end of year, next month is the first in the next year
            date_month = 1
            date_year = cycle_end_date.year + 1
        return date(
            year=date_year,
            month=date_month,
            day=calendar.monthrange(date_year, date_month)[1],
        )

    def update_next_datetime(self, reference_datetime: datetime):
        if reference_datetime == self.cycle_end_datetime:
            self.cycle_previous_end_date = self.cycle_end_date
            self.cycle_end_date = self.get_next_end_date(self.cycle_end_date)
            if (self.cycle_previous_end_date == self.cycle_end_date and
                    self.usage_settings.billing_cycle_as_calendar_month):
                self.cycle_end_date = self.increment_cycle_end(cycle_end_date=self.cycle_end_date)
        else:
            for dynamic_resource in self.dynamic_resources:  # type: DynamicResource
                if reference_datetime == dynamic_resource.end_datetime:
                    if dynamic_resource.start_datetime < self.cycle_previous_end_datetime:
                        # dynamic resource is still calculated for last cycle, calculate for current cycle
                        dynamic_resource.start_datetime = self.cycle_previous_end_datetime
                        dynamic_resource.compute_end_datetime(
                            self.cycle_end_datetime,
                            self.usage_settings.get_billable_seconds_for_date(
                                dynamic_resource.start_datetime.date()
                            )
                        )
                    else:
                        # calculate dynamic resource for next cycle
                        next_cycle_end_date = self.get_next_end_date(self.cycle_end_date)
                        next_cycle_end_datetime = datetime.combine(
                            next_cycle_end_date,
                            time(hour=0, minute=0, second=0)
                        ).replace(tzinfo=timezone.utc)
                        dynamic_resource.start_datetime = self.cycle_end_datetime
                        if (next_cycle_end_date == self.cycle_end_date and
                                self.usage_settings.billing_cycle_as_calendar_month):
                            next_cycle_end_date = self.increment_cycle_end(cycle_end_date=self.cycle_end_date)
                            next_cycle_end_datetime = datetime.combine(
                                next_cycle_end_date, datetime.max.time()
                            ).replace(tzinfo=timezone.utc)
                        dynamic_resource.compute_end_datetime(
                            next_cycle_end_datetime,
                            self.usage_settings.get_billable_seconds_for_date(
                                dynamic_resource.start_datetime.date()
                            )
                        )


class EstimatedUsage(object):
    def __init__(self, usage_cycles: List[UsageCycle] = None):
        self.usage_cycles = usage_cycles if usage_cycles is not None else []
        self.cycles_sorted = False
        self.usage_cycles_copy = None

    def __add__(self, other: 'EstimatedUsage') -> 'EstimatedUsage':
        return EstimatedUsage(
            self.usage_cycles + other.usage_cycles,
        )

    def __iadd__(self, other: 'EstimatedUsage') -> 'EstimatedUsage':
        self.usage_cycles += other.usage_cycles

        return self

    @staticmethod
    def create_for_fixed_price(
            fixed_price: Decimal,
            cycle_end_date: date,
            get_next_end_date: Callable[[date], date],
            usage_settings: UsageSettings
    ):
        usage_cycle = UsageCycle(
            fixed_price=fixed_price,
            cycle_end_date=cycle_end_date,
            get_next_end_date=get_next_end_date,
            usage_settings=usage_settings
        )
        return EstimatedUsage(usage_cycles=[usage_cycle])

    def add_usage_cycle(self, usage_cycle: UsageCycle):
        self.usage_cycles.append(usage_cycle)
        self.cycles_sorted = False

    def sort_cycles(self):
        if not self.cycles_sorted:
            self.usage_cycles.sort(key=lambda usage_cycle: usage_cycle.next_end_datetime)
            self.cycles_sorted = True

    def start_estimation(self, reference_datetime: datetime):
        self.usage_cycles_copy = copy.deepcopy(self.usage_cycles)
        for usage_cycle in self.usage_cycles:
            if usage_cycle.next_end_datetime < reference_datetime:
                usage_cycle.update_next_datetime(usage_cycle.next_end_datetime)
        self.sort_cycles()

    def stop_estimation(self):
        self.usage_cycles = self.usage_cycles_copy

    def get_price_per_second(self, reference_datetime: datetime):
        return sum(
            [usage_cycle.get_price_per_second(reference_datetime) for usage_cycle in self.usage_cycles]
        )

    def get_fixed_price(self, reference_datetime: datetime):
        fixed_price = billing_utils.DECIMAL_ZERO
        for usage_cycle in self.usage_cycles:
            if reference_datetime == usage_cycle.cycle_end_datetime:
                fixed_price += usage_cycle.fixed_price

        return fixed_price

    def get_next_cycle_datetime(self):
        if len(self.usage_cycles) == 0:
            return billing_utils.DATETIME_MAX
        else:
            return self.usage_cycles[0].next_end_datetime

    def go_to_next_cycle_datetime(self):
        if len(self.usage_cycles) == 0:
            return

        reference_datetime = self.usage_cycles[0].next_end_datetime
        for usage_cycle in self.usage_cycles:
            if reference_datetime == usage_cycle.next_end_datetime:
                usage_cycle.update_next_datetime(reference_datetime)

        self.cycles_sorted = False
        self.sort_cycles()

    def usage_is_zero_or_less(self):
        amount = sum(
            [usage_cycle.fixed_price + usage_cycle.get_max_price_per_second() for usage_cycle in self.usage_cycles]
        )
        if amount < 0:
            LOG.error('Negative amount per second found: {}'.format(amount))
        return amount <= 0

    def has_dynamic_resources(self):
        for usage_cycle in self.usage_cycles:
            if len(usage_cycle.dynamic_resources) > 0:
                return True

        return False

    def get_hours_left(self, available_credit: Decimal, reference_datetime: datetime) -> Decimal:
        if self.usage_is_zero_or_less():
            if available_credit >= 0:
                # usage is zero and we have credit, assuming credit will last forever
                return billing_utils.DECIMAL_INFINITE
            else:
                # usage is zero and we do no have credit, returning zero hours
                return billing_utils.DECIMAL_ZERO

        if reference_datetime is None:
            LOG.error('Reference datetime is None, a reference date time is needed to compute usage, aborting.')
            raise ValueError('reference_datetime must not be None')

        if reference_datetime.tzinfo is None:
            reference_datetime = reference_datetime.replace(tzinfo=timezone.utc)

        self.start_estimation(reference_datetime=reference_datetime)

        estimated_seconds_left = billing_utils.DECIMAL_ZERO
        has_dynamic_resources = self.has_dynamic_resources()

        while available_credit >= 0:
            next_cycle_datetime = self.get_next_cycle_datetime()
            fixed_price = self.get_fixed_price(next_cycle_datetime)
            price_per_second = self.get_price_per_second(reference_datetime)

            if not has_dynamic_resources and fixed_price > available_credit:
                break

            seconds_until_next_cycle = int((next_cycle_datetime - reference_datetime).total_seconds())
            if price_per_second > 0:
                seconds_until_credit_expires = (available_credit - fixed_price) / price_per_second
            else:
                seconds_until_credit_expires = math.inf

            if seconds_until_next_cycle > seconds_until_credit_expires:
                # we do not have enough credit to reach next cycle, stop estimating
                estimated_seconds_left += seconds_until_credit_expires
                break

            estimated_seconds_left += seconds_until_next_cycle
            available_credit -= seconds_until_next_cycle * price_per_second + fixed_price

            reference_datetime = next_cycle_datetime
            self.go_to_next_cycle_datetime()

        self.stop_estimation()
        return Decimal(round(estimated_seconds_left / billing_utils.SECONDS_PER_HOUR))
