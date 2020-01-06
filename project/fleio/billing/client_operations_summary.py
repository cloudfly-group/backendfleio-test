from decimal import Decimal

from fleio.core.models import Client


class ClientOperationsSummary(object):
    def __init__(self, client: Client, uptodate_credit: Decimal):
        self.client = client
        self.configuration_name = client.active_configuration.name
        self.initial_status = client.status
        self.final_status = client.status

        self.invoiced_services_count = 0  # type: int
        self.cancelled_services_count = 0  # type: int
        self.suspended_overridden_services_count = 0  # type: int
        self.auto_terminated_services_count = 0  # type: int

        self.initial_uptodate_credit = uptodate_credit
        self.final_uptodate_credit = uptodate_credit

        self.is_out_of_credit = False

        self.can_suspend = False
        self.auto_suspend = False

        self.can_resume = False

        self.overdue_hours = Decimal(0)
        self.overdue_hours_delay = 0

        self.overdue_credit = Decimal(0)
        self.overdue_credit_delay = Decimal(0)

        self.remaining_hours = Decimal(0)

    def get_formatted_summary(self):
        summary = ['Processed client {}:{}, configuration: {}, status: {} -> {}'.format(
            self.client.id,
            self.client,
            self.configuration_name,
            self.initial_status,
            self.final_status
        )]

        if self.initial_uptodate_credit != self.final_uptodate_credit:
            summary.append('Client {} uptodate credit changed: {} {} -> {} {}'.format(
                self.client,
                self.initial_uptodate_credit,
                self.client.currency,
                self.final_uptodate_credit,
                self.client.currency
            ))

        if self.is_out_of_credit:
            summary.append('Client {} is out of credit, uptodate credit: {} {}'.format(
                self.client,
                self.final_uptodate_credit,
                self.client.currency
            ))
        else:
            summary.append('Client has {} hours left until uptodate credit of {} {} is used up'.format(
                self.remaining_hours,
                self.final_uptodate_credit,
                self.client.currency
            ))

        if self.invoiced_services_count > 0:
            summary.append('Invoiced services count: {}'.format(self.invoiced_services_count))

        if self.cancelled_services_count > 0:
            summary.append('Cancelled services count: {}'.format(self.cancelled_services_count))

        if self.suspended_overridden_services_count > 0:
            summary.append('Suspended {} services with suspend overridden'.format(self.cancelled_services_count))

        if self.auto_terminated_services_count > 0:
            summary.append('Terminated {} services that were suspended'.format(self.auto_terminated_services_count))

        if self.client.is_outofcredit:
            summary.append('Client {} is out of credit'.format(self.client))
        else:
            summary.append('Client {} is not out of credit.'.format(self.client))

        if self.can_suspend:
            if self.auto_suspend:
                summary.append('Client {} was suspended.'.format(self.client))
            else:
                summary.append(
                    'Client {} can be suspended but auto suspend is disabled for configuration {}'.format(
                        self.client,
                        self.configuration_name
                    )
                )
        else:
            if self.overdue_credit < self.overdue_credit_delay:
                summary.append(
                    'Suspend delayed for client {} because overdue credit {} {} did not reached limit {} {}'.format(
                        self.client,
                        self.overdue_credit,
                        self.client.currency,
                        self.overdue_credit_delay,
                        self.client.currency
                    )
                )

            if self.overdue_hours < self.overdue_hours_delay:
                summary.append(
                    'Suspend delayed for client {} because overdue hours {} did not reached limit {}'.format(
                        self.client,
                        self.overdue_hours,
                        self.overdue_hours_delay
                    )
                )

        return summary

    def update_invoiced_services_count(self, count: int):
        self.invoiced_services_count += count

    def update_cancelled_services_count(self, count: int):
        self.cancelled_services_count += count

    def update_auto_terminated_services_count(self, count: int):
        self.auto_terminated_services_count += count

    def update_uptodate_credit(self, uptodate_credit: Decimal):
        self.final_uptodate_credit = uptodate_credit

    def update_status(self, status: str):
        self.final_status = status

    def update_outofcredit_status(self):
        self.is_out_of_credit = self.client.is_outofcredit

    def update_suspend_status(self, can_suspend: bool, auto_suspend: bool):
        self.can_suspend = can_suspend
        self.auto_suspend = auto_suspend

    def update_overdue_hours(self, overdue_hours: Decimal, overdue_hours_delay: int):
        self.overdue_hours = overdue_hours
        self.overdue_hours_delay = overdue_hours_delay

    def update_overdue_credit(self, overdue_credit: Decimal, overdue_credit_delay: Decimal):
        self.overdue_credit = overdue_credit
        self.overdue_credit_delay = overdue_credit_delay

    def update_suspend_overridden_service_count(self, count: int):
        self.suspended_overridden_services_count += count

    def update_remaining_hours(self, remaining_hours: Decimal):
        self.remaining_hours = remaining_hours
