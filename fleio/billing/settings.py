import decimal
from django.utils.translation import ugettext_lazy as _

from fleio.conf.base import ConfigOpts
from fleio.conf import options


class BillingSettings(ConfigOpts):
    credit_limit = options.DecimalOpt(max_digits=14, decimal_places=2, default=0)
    credit_required = options.DecimalOpt(max_digits=14, decimal_places=2, default=0)
    auto_resume_client_on_credit_update = options.BoolOpt(default=False)
    # For Clients with billing agreements
    credit_limit_with_agreement = options.DecimalOpt(max_digits=14, decimal_places=2, default=0)
    credit_required_with_agreement = options.DecimalOpt(max_digits=14, decimal_places=2, default=0)
    # Suspend
    auto_suspend = options.BoolOpt(default=False)
    auto_suspend_delay_hours_enabled = options.BoolOpt(default=False)
    auto_suspend_delay_hours = options.IntegerOpt(default=0, min=0)
    auto_suspend_delay_credit_enabled = options.BoolOpt(default=False)
    auto_suspend_delay_credit = options.DecimalOpt(max_digits=14, decimal_places=2, default=0, min=0)
    auto_suspend_notification_template = options.StringOpt(allow_null=True)
    # Terminate
    auto_terminate = options.BoolOpt(default=False)
    auto_terminate_delay_hours = options.IntegerOpt(default=24)
    suspend_instead_of_terminate = options.BoolOpt(default=True)
    auto_terminate_notification_template = options.StringOpt(allow_null=True)
    # Low
    credit_notifications_enabled = options.BoolOpt(default=False)
    credit_notifications_when_agreement_enabled = options.BoolOpt(default=False)
    first_credit_remaining_hours = options.IntegerOpt(default=72)
    first_credit_notification_template = options.StringOpt(allow_null=True)
    second_credit_remaining_hours = options.IntegerOpt(default=24)
    second_credit_notification_template = options.StringOpt(allow_null=True)
    third_credit_remaining_hours = options.IntegerOpt(default=1)
    third_credit_notification_template = options.StringOpt(allow_null=True)
    # Notification
    sender_email = options.StringOpt(allow_null=True)
    sender_name = options.StringOpt(allow_null=True)
    # Invoicing
    company_info = options.StringOpt(default="My Company")
    # Taxing
    auto_eu_tax_exemption = options.BoolOpt(default=False)
    add_tax_for_credit_invoices = options.BoolOpt(default=True)

    # Billing
    generate_invoices = options.BoolOpt(default=False)
    create_todo_on_invoice_payment = options.BoolOpt(default=False)
    send_notifications_for_unpaid_invoices = options.BoolOpt(default=False)
    auto_settle_usage = options.BoolOpt(default=False)
    auto_pay_invoice_only_when_enough_credit = options.BoolOpt(default=False)
    next_paid_invoice_number = options.IntegerOpt(default=1)
    next_paid_invoice_number_format = options.DjangoStringTemplateOpt(default='INV {{ number }}', allow_null=True)
    minim_uptodate_credit_for_invoice_payment = options.IntegerOpt(default=0, min=0)

    invoicing_option = options.StringOpt(default='fiscal_on_paid',
                                         choices=('only_proforma', 'always_fiscal', 'fiscal_on_paid'))

    limit_billable_seconds_per_month = options.BoolOpt(default=True)
    billable_seconds_per_month = options.IntegerOpt(default=2400000, min=1, max=3000000)

    issue_invoice_before_next_due_date = options.BoolOpt(default=False)
    next_invoice_date_offset = options.IntegerOpt(default=0, min=0, max=30)
    billing_cycle_as_calendar_month = options.BoolOpt(default=False)

    # Signup
    fraud_check = options.BoolOpt(default=False)
    maxmind_manual_review_score = options.IntegerOpt(min=1, max=99, default=30)
    maxmind_fraud_score = options.IntegerOpt(min=1, max=99, default=60)
    enable_maxmind_insights = options.BoolOpt(default=True)
    auto_create_order = options.BoolOpt(default=False)
    auto_order_service = options.IntegerOpt(allow_null=True)
    auto_order_service_cycle = options.IntegerOpt(allow_null=True)
    auto_order_service_params = options.JsonOpt(allow_null=True)
    client_initial_credit = options.IntegerOpt(min=0, default=0)

    class Meta:
        section = 'BILLING'


class ProductType:
    generic = 'generic'
    openstack = 'openstack'
    hosting = 'hosting'
    domain = 'domain'
    reseller = 'reseller'

    choices = [
        (generic, _('Generic')),
        (openstack, 'OpenStack'),
        (hosting, _('Shared Hosting')),
        (domain, _('Domain')),
        (reseller, _('Reseller')),
    ]


class ServiceStatus:
    pending = 'pending'
    active = 'active'
    suspended = 'suspended'
    terminated = 'terminated'
    canceled = 'canceled'
    fraud = 'fraud'
    archived = 'archived'

    status_map = {
        pending: _('Pending'),
        active: _('Active'),
        suspended: _('Suspended'),
        terminated: _('Terminated'),
        canceled: _('Canceled'),
        fraud: _('Fraud'),
        archived: _('Archived'),
    }

    choices = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('terminated', 'Terminated'),
        ('canceled', 'Canceled'),
        ('fraud', 'Fraud'),
        ('archived', 'Archived'),
    ]


class ServiceTask:
    changeInProgress = 'changing'

    status_map = {
        changeInProgress: _('Change in progress'),
    }

    choices = [
        ('changing', 'Changing'),
    ]


class CyclePeriods:
    onetime = 'onetime'
    hour = 'hour'
    month = 'month'
    year = 'year'

    recurring_choices = [(hour, _('Hour')),
                         (month, _('Month')),
                         (year, _('Year'))]

    choices = [(onetime, _('One Time')),
               (hour, _('Hour')),
               (month, _('Month')),
               (year, _('Year'))]

    @staticmethod
    def display_name(cycle, multiplier):
        if cycle == CyclePeriods.onetime:
            return _('One Time')
        elif cycle == CyclePeriods.year:
            if multiplier == decimal.Decimal('1.00'):
                return _('Yearly')
            elif multiplier == decimal.Decimal('2.00'):
                return _('Biennial')
            elif multiplier == decimal.Decimal('3.00'):
                return _('Triennial')
            else:
                return _('Every {} years').format(multiplier)
        elif cycle == CyclePeriods.month:
            if multiplier == decimal.Decimal('1.00'):
                return _('Monthly')
            elif multiplier == decimal.Decimal('3.00'):
                return _('Quarterly')
            elif multiplier == decimal.Decimal('6.00'):
                return _('Semi-Annual')
            else:
                return _('Every {} months').format(multiplier)
        elif cycle == CyclePeriods.hour:
            if multiplier == decimal.Decimal('1.00'):
                return _('Hourly')
            else:
                return _('Every {} hours').format(multiplier)
        else:
            return _('Unknown')


class ProductAutoSetup:
    disabled = 'disabled'
    on_order = 'on_order'
    on_first_payment = 'first_payment'
    manual = 'manual'

    choices = [(disabled, _('Disabled')),
               (on_order, _('When order is placed')),
               (on_first_payment, _('On first payment')),
               (manual, _('When pending order is accepted'))]


class PublicStatuses:
    public = 'public'
    private = 'private'
    retired = 'retired'

    choices = [(public, _('Public')),
               (private, _('Private')),
               (retired, _('Retired'))]


class PricingModel:
    free = 'free'
    fixed_and_dynamic = 'fixed_and_dynamic'
    dynamic_or_fixed = 'dynamic_or_fixed'

    choices = [(free, _('Free')),
               (fixed_and_dynamic, _('Fixed plus dynamic')),
               (dynamic_or_fixed, _('Dynamic but at least fixed'))]


class OrderStatus:
    pending = 'pending'
    verified = 'verified'
    completed = 'completed'
    cancelled = 'cancelled'
    choices = [(pending, _('Pending')),
               (verified, _('Verified')),
               (completed, _('Completed')),
               (cancelled, _('Cancelled'))]


class PaymentStatus:
    unpaid = 'unpaid'
    paid = 'paid'
    canceled = 'canceled'
    refunded = 'refunded'

    choices = [('unpaid', _('Unpaid')),
               ('paid', _('Paid')),
               ('canceled', _('Canceled')),
               ('Refunded', _('Refunded'))]


class ServiceSuspendType:
    SUSPEND_REASON_UNSPECIFIED = _('Unspecified reason')
    SUSPEND_REASON_STAFF = _('Suspended by staff')
    SUSPEND_REASON_OVERDUE = _('Overdue on payment')
    SUSPEND_REASON_USER_REQUESTED = _('Requested by user')
    SUSPEND_REASON_TERMINATE_DISABLED = _('Suspend instead of terminate is enabled')

    staff = 'staff'
    overdue = 'overdue'
    user_requested = 'userrequested'

    choices = [(staff, SUSPEND_REASON_STAFF),
               (overdue, SUSPEND_REASON_OVERDUE),
               (user_requested, SUSPEND_REASON_USER_REQUESTED)]


class BillingItemTypes:
    service = 'service'
    serviceUpgrade = 'serviceUpgrade'
    credit = 'credit'
    setupfee = 'setupfee'
    other = 'other'

    CHOICES = ((service, _('Service')),
               (serviceUpgrade, _('Service Upgrade')),
               (credit, _('Credit Balance')),
               (setupfee, _('Setup Fee')),
               (other, _('Other')))

    def __contains__(self, item):
        return item in [c[0] for c in self.CHOICES]
