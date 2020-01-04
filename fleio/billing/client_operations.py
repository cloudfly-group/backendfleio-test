import logging
from datetime import datetime
from datetime import timedelta
from decimal import Decimal

import celery
from django.conf import settings
from django.utils.timezone import now as utcnow

from fleio.billing.client_operations_summary import ClientOperationsSummary
from fleio.billing.estimated_usage import EstimatedUsage
from fleio.billing.models import Service
from fleio.billing.models import TaxRule
from fleio.billing.models.calcelation_request import CancellationTypes
from fleio.billing.models.service import ServiceStatus
from fleio.billing.modules.factory import module_factory
from fleio.billing.services import tasks as service_tasks
from fleio.billing.settings import ServiceSuspendType
from fleio.billing.settlement_manager import SettlementManager
from fleio.billing.usage_settings import UsageSettings
from fleio.billing.utils import cdecimal
from fleio.core.models import Client
from fleio.core.models import ClientStatus
from fleio.notifications import notifier
from fleio.notifications.models import Notification
from fleio.notifications.utils import reset_current_notification
from fleio.reseller.utils import reseller_suspend_instead_of_terminate

LOG = logging.getLogger(__name__)


class ClientUsage(object):
    def __init__(self, unpaid_usage: Decimal = Decimal(0), estimated_usage: EstimatedUsage = None):
        self.unpaid_usage = unpaid_usage
        self.estimated_usage = estimated_usage if estimated_usage is not None else EstimatedUsage()

    def get_remaining_hours(self, available_credit: Decimal, reference_datetime: datetime):
        return self.estimated_usage.get_hours_left(available_credit, reference_datetime=reference_datetime)


class ClientOperations(object):
    def __init__(self, client: Client, reference_datetime: datetime = None):
        self.client = client
        self.billing_settings = self.client.billing_settings
        self.has_billing_agreement = client.has_billing_agreement
        if self.has_billing_agreement:
            credit_limit = self.billing_settings.credit_limit_with_agreement
            if self.client.billing_settings.credit_notifications_enabled:
                self.credit_notifications_enabled = self.billing_settings.credit_notifications_when_agreement_enabled
            else:
                self.credit_notifications_enabled = False
        else:
            credit_limit = self.client.billing_settings.credit_limit
            self.credit_notifications_enabled = self.billing_settings.credit_notifications_enabled
        self.client_credit_limit = credit_limit
        self.reference_datetime = reference_datetime if reference_datetime is not None else utcnow()

        self.__client_usage = None
        self.summary = ClientOperationsSummary(self.client, self.client.get_uptodate_credit())

    def __compute_client_usage(self) -> ClientUsage:
        # compute total unpaid usage for all services associated with the client
        LOG.debug('Computing total usage for client {}'.format(self.client))
        total_unpaid_usage = Decimal(0)
        total_estimated_usage = EstimatedUsage()
        usage_settings = UsageSettings(billing_settings=self.billing_settings)
        for service in self.client.services.all():
            billing_module = module_factory.get_module_instance(service=service)

            # get unpaid usage from billing module
            unpaid_usage = billing_module.get_unpaid_usage(service)
            total_unpaid_usage += unpaid_usage.total_cost

            if service.status == ServiceStatus.active:
                # get unpaid usage from service
                if service.next_due_date is not None and service.next_due_date < self.reference_datetime:
                    total_unpaid_usage += service.get_fixed_price()

                # see if we need to get estimated usage from billing module
                if not service.is_price_overridden:
                    # get estimated usage from billing module
                    estimated_usage = billing_module.get_estimated_usage(service, usage_settings=usage_settings)
                    total_estimated_usage += estimated_usage

                # add service static price if needed
                if service.get_fixed_price() > 0:
                    service_fixed_usage = EstimatedUsage.create_for_fixed_price(
                        fixed_price=service.get_fixed_price(),
                        cycle_end_date=service.next_due_date,
                        get_next_end_date=lambda previous_end_date, s=service: s.get_next_due_date(previous_end_date),
                        usage_settings=usage_settings
                    )

                    total_estimated_usage += service_fixed_usage

        return ClientUsage(total_unpaid_usage, total_estimated_usage)

    def update_usage(self, skip_collecting: bool = False, skip_compute_current: bool = False):
        if not skip_collecting:
            usage_settings = UsageSettings(billing_settings=self.billing_settings)

            # compute total unpaid usage for all services associated with the client
            LOG.debug('Updating usage for client {}'.format(self.client))
            for service in self.client.services.all():
                billing_module = module_factory.get_module_instance(service=service)
                billing_module.collect_usage(service=service, usage_settings=usage_settings)

        if not skip_compute_current:
            # compute current client usage
            self.__client_usage = self.__compute_client_usage()

        # update uptodate credit for client
        uptodate_credit = cdecimal(
            self.client.get_remaining_credit(self.client_usage.unpaid_usage, self.client.currency.code)
        )
        self.client.set_uptodate_credit(uptodate_credit=uptodate_credit)

        self.update_outofcredit_status()

        # log to summary
        self.summary.update_uptodate_credit(self.uptodate_credit)

    def reset_usage(self):
        # call reset usage for all services
        for service in self.client.services.all():
            billing_module = module_factory.get_module_instance(service=service)
            billing_module.reset_usage(service=service)

        # recalculate usage after reset
        self.update_usage()

    @property
    def client_usage(self) -> ClientUsage:
        if self.__client_usage is None:
            self.update_usage(skip_collecting=True)

        return self.__client_usage

    @client_usage.setter
    def client_usage(self, value: ClientUsage):
        self.__client_usage = value

    @property
    def uptodate_credit(self):
        if not self.client.has_uptodate_credit:
            self.update_usage(skip_collecting=True)

        return self.client.get_uptodate_credit()

    def get_add_credit_url(self):
        """
        :return: URL where customers can add credit to their accounts
        """
        if not settings.ADD_CREDIT_URLS:
            if self.client.reseller_resources:
                return self.client.reseller_resources.enduser_panel_url
            else:
                # if it's empty setting
                return settings.FRONTEND_URL

        if len(settings.ADD_CREDIT_URLS) == 1 or self.client.groups.all().count() <= 1:
            # just one item in dictionary, return it
            return list(settings.ADD_CREDIT_URLS.values())[0]

        group = self.client.groups.all()[0]
        if group.name in settings.ADD_CREDIT_URLS:
            return settings.ADD_CREDIT_URLS[group.name]

        return list(settings.ADD_CREDIT_URLS.values())[0]

    def evaluate_and_send_low_credit_notifications(self):
        LOG.debug('Evaluating and sending low credit notifications for client {}...'.format(self.client))

        remaining_credit = self.uptodate_credit - self.client_credit_limit
        remaining_hours = self.client_usage.get_remaining_hours(remaining_credit, self.reference_datetime)

        # reset the is_current field on out of credit notifications in order to
        # send again notifications in the future
        if remaining_hours > self.billing_settings.third_credit_remaining_hours:
            reset_current_notification(
                client=self.client,
                notification_name=self.billing_settings.third_credit_notification_template,
                priority=Notification.PRIORITY_CRITICAL  # reset third nt which always has critical priority
            )
        if remaining_hours > self.billing_settings.second_credit_remaining_hours:
            reset_current_notification(
                client=self.client,
                notification_name=self.billing_settings.second_credit_notification_template,
                priority=Notification.PRIORITY_HIGH,  # reset second nt which always has high priority
            )
        if remaining_hours > self.billing_settings.first_credit_remaining_hours:
            reset_current_notification(
                client=self.client,
                notification_name=self.billing_settings.first_credit_notification_template,
                priority=Notification.PRIORITY_LOW,  # reset third nt which always has low priority
            )

        self.summary.update_remaining_hours(remaining_hours)

        if not self.credit_notifications_enabled:
            LOG.debug('Credit notifications not enabled, skipping')
            return

        if not self.client.status == ClientStatus.active:
            LOG.warning('Evaluate and send low credit notifications called for inactive client, skipping')
            return

        variables = {
            'add_credit_url': self.get_add_credit_url(),
            'credit_hours_left': remaining_hours,
            'currency': str(self.client.currency),
            'credit': '{0:.2f}'.format(remaining_credit)
        }

        if (self.billing_settings.third_credit_notification_template and
                (self.billing_settings.third_credit_remaining_hours >= remaining_hours)):
            LOG.debug('Sending third low credit notification')
            notifier.send(client=self.client,
                          name=self.billing_settings.third_credit_notification_template,
                          priority=notifier.Notification.PRIORITY_CRITICAL,
                          variables=variables,
                          is_current=True,
                          check_if_already_notified=True,
                          is_current_verification=True, )
        elif (self.billing_settings.second_credit_notification_template and
              (self.billing_settings.second_credit_remaining_hours >= remaining_hours)):
            LOG.debug('Sending second low credit notification')
            notifier.send(client=self.client,
                          name=self.billing_settings.second_credit_notification_template,
                          priority=notifier.Notification.PRIORITY_HIGH,
                          variables=variables,
                          is_current=True,
                          check_if_already_notified=True,
                          is_current_verification=True, )
        elif (self.billing_settings.first_credit_notification_template and
              (self.billing_settings.first_credit_remaining_hours >= remaining_hours)):
            LOG.debug('Sending first low credit notification')
            notifier.send(client=self.client,
                          name=self.billing_settings.first_credit_notification_template,
                          priority=notifier.Notification.PRIORITY_LOW,
                          variables=variables,
                          is_current=True,
                          check_if_already_notified=True,
                          is_current_verification=True, )

    def suspend(self, reason: str = ServiceSuspendType.SUSPEND_REASON_UNSPECIFIED, suspend_type: str = None) -> bool:
        LOG.debug('Suspend called for client {} with suspend type {} and reason {}'.format(
            self.client, suspend_type, reason
        ))

        if self.client.status == ClientStatus.suspended:
            LOG.warning('Suspend called for already suspended client, skipping')
            return False

        LOG.debug('Suspending client')
        suspend_service_tasks = list()
        for service in self.client.services.active():
            if suspend_type == ServiceSuspendType.overdue and service.is_suspend_overridden():
                # do not suspend services with suspend overridden
                continue
            suspend_service_tasks.append(service_tasks.suspend_service.s(
                service.id, reason,
                suspend_type=suspend_type
            ))

        celery.group(suspend_service_tasks).apply_async()

        self.client.status = ClientStatus.suspended
        self.client.suspend_reason = suspend_type
        self.client.save(update_fields=['status', 'suspend_reason'])
        LOG.debug('Client suspended')

        return True

    def resume(self, suspend_type: str = None) -> bool:
        LOG.debug('Resume called for client {} with suspend type {}'.format(self.client, suspend_type))

        if self.client.status == ClientStatus.active:
            LOG.warning('Resume called for already active client, skipping')
            return False

        if not self.client.suspend_reason == suspend_type:
            LOG.debug(
                'Resume called for suspended client with suspend reason other than {}, skipping'.format(
                    self.client.suspend_reason
                )
            )
            return False

        LOG.debug('Resuming client')
        resume_service_tasks = list()
        for service in self.client.services.suspended(suspend_type=suspend_type):
            resume_service_tasks.append(service_tasks.resume_service.s(service.id))

        celery.group(resume_service_tasks).apply_async()

        self.client.status = ClientStatus.active
        self.client.suspend_reason = ClientStatus.active
        self.client.save(update_fields=['status', 'suspend_reason'])
        LOG.debug('Client resumed')

        return True

    def update_outofcredit_status(self):
        if self.uptodate_credit < self.client_credit_limit:
            self.client.set_outofcredit(self.reference_datetime)
        else:
            self.client.clear_outofcredit()

        self.summary.update_outofcredit_status()

    def evaluate_and_suspend_if_overdue(self) -> bool:
        LOG.debug('Evaluate and suspend called for client {}'.format(self.client))

        if self.client.status == ClientStatus.suspended:
            LOG.warning('Client already suspended, skipping')
            return False

        self.update_outofcredit_status()

        if not self.client.is_outofcredit:
            LOG.debug('Client is not overdue, skipping')
            return False

        LOG.debug('Client is overdue, check for suspend delays')
        overdue_hours = self.client.get_hours_since_outofcredit(self.reference_datetime)
        overdue_credit = -(self.uptodate_credit - self.client_credit_limit)
        can_suspend = not (
            self.billing_settings.auto_suspend_delay_hours_enabled or
            self.billing_settings.auto_suspend_delay_credit_enabled
        )

        if can_suspend:
            LOG.debug('Client can be suspended because no suspension delay is active')
        else:
            if self.billing_settings.auto_suspend_delay_hours_enabled:
                if overdue_hours >= self.billing_settings.auto_suspend_delay_hours:
                    LOG.debug('Client can be suspended because hours delay was reached')
                    can_suspend = True
                else:
                    self.summary.update_overdue_hours(
                        overdue_hours,
                        self.billing_settings.auto_suspend_delay_hours
                    )
            if not can_suspend and self.billing_settings.auto_suspend_delay_credit_enabled:
                if overdue_credit >= self.billing_settings.auto_suspend_delay_credit:
                    LOG.debug('Client can be suspended because credit delay was reached')
                    can_suspend = True
                else:
                    self.summary.update_overdue_credit(
                        overdue_credit,
                        self.billing_settings.auto_suspend_delay_credit
                    )

        self.summary.update_suspend_status(can_suspend, self.billing_settings.auto_suspend)

        if not self.billing_settings.auto_suspend:  # Auto suspend disabled
            LOG.debug('Auto suspend not active, skipping')
            return False

        if can_suspend:
            LOG.debug('Suspending client')
            self.suspend(reason=ServiceSuspendType.SUSPEND_REASON_OVERDUE, suspend_type=ServiceSuspendType.overdue)
            if self.billing_settings.auto_suspend_notification_template:
                variables = {'add_credit_url': self.get_add_credit_url()}
                notifier.critical(client=self.client,
                                  name=self.billing_settings.auto_suspend_notification_template,
                                  variables=variables)
            self.summary.update_status(self.client.status)
            return True
        else:
            LOG.debug('Client is overdue, but suspension is delayed, will not suspend')
            return False

    def evaluate_and_resume_if_enough_credit(self) -> bool:
        LOG.debug('Evaluate and resume called for client {}'.format(self.client))

        if self.client.status == ClientStatus.active:
            LOG.warning('Evaluate and resume called for active client, skipping')
            return False

        self.update_outofcredit_status()

        if self.client.is_outofcredit:
            LOG.debug('Client is overdue, skipping')
            return False
        else:
            LOG.debug('Client over limit, resuming')
            self.resume(suspend_type=ServiceSuspendType.overdue)
            LOG.debug('Client resumed')
            self.summary.update_status(self.client.status)

            return True

    def process_services_with_suspend_override(self):
        # only active services for suspended clients should be services with suspend overridden
        # so it should be safe to select only those
        services_to_suspend = Service.objects.filter(
            client=self.client,
            client__status=ClientStatus.suspended,
            status=ServiceStatus.active
        )

        for service in services_to_suspend:
            if not service.is_suspend_overridden():
                service_tasks.suspend_service.delay(
                    service.id, ServiceSuspendType.SUSPEND_REASON_OVERDUE,
                    suspend_type=ServiceSuspendType.overdue
                )
                self.summary.update_suspend_overridden_service_count(1)

    def process_client_suspended_services(self):
        # will set auto terminate date and terminate suspended services that exceeded that date
        if not (self.billing_settings.suspend_instead_of_terminate or reseller_suspend_instead_of_terminate(
            client=self.client,
        )):
            LOG.info('Processing client suspended services')
            terminate_service_tasks = list()
            suspended_services = Service.objects.filter(client=self.client, status=ServiceStatus.suspended)
            now = utcnow()
            termination_date = now + timedelta(hours=self.billing_settings.auto_terminate_delay_hours)
            for service in suspended_services:
                if not service.auto_terminate_date:
                    service.auto_terminate_date = termination_date
                    service.save()
                else:
                    if service.auto_terminate_date < now:
                        terminate_service_tasks.append(service_tasks.terminate_service.s(service.id))
                        if self.billing_settings.auto_terminate_notification_template:
                            variables = {
                                'terminated_service_id': service.id,
                                'terminated_service_display_name': service.display_name,
                            }
                            notifier.critical(client=self.client,
                                              name=self.billing_settings.auto_terminate_notification_template,
                                              variables=variables)

            if len(terminate_service_tasks):
                self.summary.update_auto_terminated_services_count(count=len(terminate_service_tasks))
                celery.group(terminate_service_tasks).apply_async()

    def process_client_services(self):
        LOG.info('Processing client services')
        client_tax_rules = None
        if self.billing_settings.generate_invoices or self.billing_settings.auto_settle_usage:
            client_tax_rules = TaxRule.for_country_and_state(
                country=self.client.country_name,
                state=self.client.state
            )

        if self.billing_settings.generate_invoices:
            """Creates an invoice with all client services that are in their due date."""
            active_services_in_invoice_due = self.client.services.active().recurring().in_invoice_due()
            active_services_in_invoice_due = active_services_in_invoice_due.filter(cancellation_request__isnull=True)

            if active_services_in_invoice_due:
                if SettlementManager.process_services(self.client, active_services_in_invoice_due, client_tax_rules):
                    self.summary.update_invoiced_services_count(active_services_in_invoice_due.count())
        else:
            if self.billing_settings.auto_settle_usage:
                SettlementManager.settle_services_usage_from_client_credit(
                    self.client,
                    self.client.services.active().in_due(),
                    client_tax_rules
                )

    def process_cancellation_requests(self):
        svc_filter = self.client.services.active().non_free()
        cancellable_services = svc_filter.filter(
            cancellation_request__cancellation_type=CancellationTypes.END_OF_CYCLE,
            next_due_date__lte=utcnow()
        )

        for s in cancellable_services:
            if self.billing_settings.suspend_instead_of_terminate or reseller_suspend_instead_of_terminate(
                    client=self.client,
            ):
                service_tasks.suspend_service.delay(
                    s.pk,
                    reason=ServiceSuspendType.SUSPEND_REASON_UNSPECIFIED,
                    suspend_type=ServiceSuspendType.staff
                )
            else:
                service_tasks.terminate_service.delay(s.pk, cancellation_request_id=s.cancellation_request.pk)
            self.summary.update_cancelled_services_count(1)
