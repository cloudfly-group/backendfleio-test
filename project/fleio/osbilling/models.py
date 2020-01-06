import calendar
import copy
import datetime
import decimal
import logging
import math
import operator
from operator import itemgetter
from typing import Optional

import six
from django.db import models
from django.db import transaction
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from jsonfield import JSONField

from fleio.billing.models import Service
from fleio.core.models import Currency
from fleio.osbilling.utils import convert_currency
from fleio.osbilling.utils import convert_to_type
from fleio.osbilling.utils import resize_to
from fleio.osbilling.utils import time_unit_seconds
from fleio.utils.time import parse_isotime

LOG = logging.getLogger(__name__)

TIME_UNITS = (
    ('s', _('Second')),
    ('m', _('Minute')),
    ('h', _('Hour')),
    ('bc', _('Billing cycle')),
    ('d', _('Day')),
)

VALUE_UNIT_MAP = {'b': 'B', 'k': 'KB', 'm': 'MB', 'g': 'GB', 't': 'TB', 'p': 'PB'}
TIME_UNIT_MAP = {'s': 's', 'm': 'min', 'h': 'h', 'd': 'day', 'bc': 'bc', 'default': 'Time'}

STRING_COMPARATORS = (
    ('eq', _('Equal')),
    ('ne', _('Not equal')),
    ('in', _('In list')),
    ('ni', _('Not in list'))
)

NUMBER_COMPARATORS = (
    ('lt', _('Less than')),
    ('le', _('Less or equal')),
    ('gt', _('Greater than')),
    ('ge', _('Greater or equal')),
)

NUMBER_COMPARATORS += STRING_COMPARATORS

ATTRIBUTE_UNITS = (
    ('u', 'Units'),
    ('b', 'Bytes'),
    ('k', 'Kilobytes'),
    ('m', 'Megabytes'),
    ('g', 'Gigabytes'),
    ('t', 'Terabytes'),
    ('p', 'Petabytes'),
)


def get_display_unit(value_unit, time_unit):
    """Returns a formatted string for display purposes"""
    display_unit = VALUE_UNIT_MAP.get(value_unit, None)
    time_unit_display = TIME_UNIT_MAP.get(time_unit, None) or TIME_UNIT_MAP.get('default')
    if display_unit is None:
        return '{}'.format(time_unit_display.capitalize())
    else:
        return '{}{}'.format(display_unit, time_unit_display)


def convert_attributes(attr_value, match_value, attr_type):
    # Convert the values to be matched to their definition types (datetime, integer, float)
    if type(match_value) is list:
        match_value = [convert_to_type(mv, attr_type) for mv in match_value]
    else:
        match_value = convert_to_type(match_value, attr_type)
    attr_value = convert_to_type(attr_value, attr_type)
    return attr_value, match_value


def attribute_match(attr_value, match_value, attr_type, op, compare_value_size=None, original_value_size=None):
    """
    :type attr_value: basestring or float or datetime, single value
    :type match_value: dict, as: 'primitive or list of primitives'
    :type attr_type: basestring, the value type: string, integer, datetime
    :type compare_value_size: basestring, the attribute_unit: u (from Units), k (from Kilobytes), m, g
    :type original_value_size: basestring, the definition value_size: u (from Units), k (from Kilobytes), m, g
    :type op: basestring or str or unicode
    """
    # Convert the attributes values (some may be strings but they are defined as ints, same for datetimes)
    if op in ('in', 'ni') and attr_type == 'string':
        match_value = [ma_val.strip() for ma_val in match_value.split(',')]
    attr_value, match_value = convert_attributes(attr_value, match_value, attr_type)
    if original_value_size is not None:
        # If the Resource definition has defined a size for this value (k, m, g..) resize it
        # to the proper comparison value (the PriceRule modifiers/conditions may require other sizes)
        try:
            attr_value = resize_to(attr_value, f=original_value_size, to=compare_value_size)
        except (TypeError, ValueError):
            # NOTE(tomo): Just return False when we have a definition and no attributes or wrong types
            LOG.error('Request to resize attribute value of wrong type was ignored')
            return False
        # resize_to returns a float, convert it to attr_type (integer for example)
        attr_value = convert_to_type(attr_value, attr_type)

    try:
        if op == 'in':
            return operator.contains(match_value, attr_value)
        elif op == 'ni':
            return operator.not_(operator.contains(match_value, attr_value))
        else:  # Existing normal operators
            return getattr(operator, op)(attr_value, match_value)
    except TypeError as e:
        LOG.error('{} - {}'.format(e, 'Price rule conditions/modifiers operators may be wrong'))


class PricingPlanManager(models.Manager):
    def get_default_or_any_or_create(self, currency=None, reseller_resources=None):
        queryset = self.filter(reseller_resources=reseller_resources)
        plan = queryset.filter(is_default=True).first() or queryset.first()
        if plan is None:
            if currency is None:
                currency = Currency.objects.filter(is_default=True).first() or Currency.objects.first()
                assert currency is not None, 'No currency is defined'
            return self.create(
                name='default',
                currency=currency,
                reseller_resources=reseller_resources,
                is_default=True,
            )
        else:
            return plan

    def for_reseller(self, reseller_resources=None):
        return self.filter(reseller_resources=reseller_resources)


@python_2_unicode_compatible
class PricingPlan(models.Model):
    """A billing plan for clients."""
    name = models.CharField(max_length=255)
    currency = models.ForeignKey(Currency, null=True, blank=True, on_delete=models.PROTECT)
    is_default = models.BooleanField(default=False)
    reseller_resources = models.ForeignKey(
        'reseller.ResellerResources',
        on_delete=models.PROTECT,
        related_name='pricing_plans',
        default=None,
        null=True,
        blank=True,
    )

    objects = PricingPlanManager()

    def save(self, *args, **kwargs):
        if self.is_default:
            # NOTE(tomo): Remove any other defaults
            PricingPlan.objects.filter(
                is_default=True, reseller_resources=self.reseller_resources
            ).exclude(id=self.id).update(is_default=False)
        return super(PricingPlan, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class ClientBillingStates(object):
    unsettled = 'unsettled'
    invoiced = 'invoiced'
    settled = 'settled'


CLIENT_BILLING_STATES_CHOICES = ((ClientBillingStates.unsettled, 'Unsettled'),
                                 (ClientBillingStates.invoiced, 'Invoiced'),
                                 (ClientBillingStates.settled, 'Settled'),
                                 )


@python_2_unicode_compatible
class ServiceDynamicUsage(models.Model):
    service = models.OneToOneField(
        Service, related_name='service_dynamic_usage', on_delete=models.CASCADE, null=True, blank=True,
    )
    reseller_service = models.OneToOneField(
        Service,
        related_name='reseller_service_dynamic_usage',
        on_delete=models.CASCADE,
        null=True,
        default=None,
        blank=True,
    )
    plan = models.ForeignKey(PricingPlan, related_name='service_dynamic_usage', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=16, decimal_places=4, default=0)
    updated_at = models.DateTimeField(null=True, blank=True)
    usage = JSONField(null=True, blank=True)

    class Meta:
        ordering = ['-updated_at']

    @property
    def active_service(self):
        if self.service:
            return self.service

        if self.reseller_service:
            return self.reseller_service

        LOG.error('Both service and reseller_service are null, ')

    @property
    def first_anniversary_date(self):
        history = self.billing_cycle_history.order_by('start_date').first()
        if history:
            return history.start_date_dt_utc
        else:
            return self.start_date_dt_utc

    @property
    def last_anniversary_date(self):
        return self.end_date_dt_utc

    # TODO - #925: this should be removed, use instead client operations
    @property
    def client_remaining_balance(self):
        return self.active_service.client.get_remaining_credit(self.price, self.active_service.client.currency.code)

    def get_next_billing_date(self, date):
        """
        Get the next month relative to a date
        :type date: datetime.date
        """
        if (self.active_service.client.billing_settings and
                self.active_service.client.billing_settings.billing_cycle_as_calendar_month):
            # same month and year, only the day will be last day of month
            month_days = calendar.monthrange(date.year, date.month)[1]
            return datetime.date(year=date.year, month=date.month, day=month_days)
        billing_day = date.day
        next_month = date.month + 1 if date.month < 12 else 1
        next_year = date.year + 1 if next_month == 1 else date.year
        month_days = calendar.monthrange(next_year, next_month)[1]
        if billing_day > month_days:
            # Next month doesn't have that many days. Change the anniversary day.
            # NOTE(tomo): Switch assignments to progressively change the billing day
            # billing_day = month_days
            billing_day = 28
        return datetime.date(year=next_year, month=next_month, day=billing_day)

    @property
    def start_date_dt_utc(self):
        dt = datetime.datetime
        return dt.combine(self.start_date, dt.min.time()).replace(tzinfo=timezone.utc)

    @property
    def end_date_dt_utc(self):
        dt = datetime.datetime
        if (self.active_service.client.billing_settings and
                self.active_service.client.billing_settings.billing_cycle_as_calendar_month):
            # for cycle as calendar month, last day of month is fully included in the cycle
            return dt.combine(self.end_date, dt.max.time()).replace(tzinfo=timezone.utc)
        return dt.combine(self.end_date, dt.min.time()).replace(tzinfo=timezone.utc)

    def start_new_cycle(self, update_credit_balance=False):
        """Save the current usage to history and start a new cycle"""
        with transaction.atomic():
            if update_credit_balance:
                self.active_service.client.withdraw_credit(self.price, self.plan.currency)

            self.billing_cycle_history.create(start_date=self.start_date,
                                              end_date=self.end_date,
                                              usage=self.usage,
                                              price=self.price,
                                              updated_at=self.updated_at,
                                              state=ClientBillingStates.unsettled)

            self.start_date = self.end_date
            self.end_date = self.get_next_billing_date(self.start_date)
            if (self.start_date == self.end_date and self.active_service.client.billing_settings and
                    self.active_service.client.billing_settings.billing_cycle_as_calendar_month):
                start_date_day = 1
                if self.end_date.month < 12:
                    start_date_month = self.end_date.month + 1
                    start_date_year = self.end_date.year
                else:
                    # end of year, next month is the first in the next year
                    start_date_month = 1
                    start_date_year = self.end_date.year + 1
                self.start_date = datetime.date(
                    year=start_date_year,
                    month=start_date_month,
                    day=start_date_day
                )
                self.end_date = self.get_next_billing_date(self.start_date)
            self.usage = dict(project=None, usage_details=list(), usage_end=self.end_date_dt_utc)
            self.price = decimal.Decimal(0)
            self.updated_at = self.start_date_dt_utc
            self.save(update_fields=['start_date', 'end_date', 'usage', 'price', 'updated_at'])

    def save(self, *args, **kwargs):
        if not self.id:
            # automatically set the start and end dates for new ServiceDynamicUsages
            self.start_date = timezone.now().date()
            self.end_date = self.get_next_billing_date(date=self.start_date)
        return super(ServiceDynamicUsage, self).save(*args, **kwargs)

    def get_usage(self):
        """
        Deserialize the usage by replacing each rule,
        modifier and metric id with actual models.
        """
        # FIXME(tomo): Prices are converted to floats. We need decimals
        if self.usage is None:
            return dict()
        current_usage = copy.deepcopy(self.usage)
        try:
            if not type(current_usage['usage_end']) is datetime.datetime:
                current_usage['usage_end'] = parse_isotime(current_usage['usage_end'])
        except (ValueError, KeyError) as e:
            LOG.exception('Exception {} when parsing times'.format(e))
            return dict()
        for r in current_usage['usage_details']:
            for res in r['usage']:
                for hist in res['history']:
                    # Convert rule to PriceRule object and start and end to datetimes
                    try:
                        hist['rule'] = PricingRule.objects.get(id=hist['rule'])
                    except PricingRule.DoesNotExist:
                        continue
                    try:
                        hist['start'] = parse_isotime(hist['start'])
                        hist['end'] = parse_isotime(hist['end'])
                    except ValueError as e:
                        LOG.exception('Exception {} when parsing times'.format(e))
                        continue
                    for modifier in hist['modifiers']:
                        try:
                            modifier['modifier'] = PricingRuleModifier.objects.get(id=modifier['modifier'])
                        except PricingRuleModifier.DoesNotExist:
                            pass
                        try:
                            modifier['start'] = parse_isotime(modifier['start'])
                            modifier['end'] = parse_isotime(modifier['end'])
                        except ValueError as e:
                            LOG.exception('Exception {} when parsing times'.format(e))
                            continue
        return current_usage

    def set_usage(self, usage):
        usage = copy.deepcopy(usage)
        for r in usage['usage_details']:
            for res in r['usage']:
                for hist in res['history']:
                    hist['rule'] = hist['rule'].id
                    for modifier in hist['modifiers']:
                        modifier['modifier'] = modifier['modifier'].id
        self.usage = usage
        self.price = usage.get('price', decimal.Decimal(0))
        # TODO(tomo): updated_at should never be None and always be defined.
        # TODO(tomo): Investigate if we really need timezone.now() here as a default
        self.updated_at = usage.get('usage_end', timezone.now().replace(tzinfo=timezone.utc, microsecond=0))
        self.save(update_fields=['usage', 'updated_at', 'price'])
        return self.usage

    def get_previous_history(self):
        return self.billing_cycle_history.order_by('-start_date').first()

    def __str__(self):
        display = '{} / {} / {}'.format(self.active_service, self.plan, self.start_date)
        if self.reseller_service:
            display = '{}(for reseller)'.format(display)

        return display


@python_2_unicode_compatible
class ServiceDynamicUsageHistory(models.Model):
    service_dynamic_usage = models.ForeignKey(
        ServiceDynamicUsage, related_name='billing_cycle_history', on_delete=models.CASCADE
    )
    start_date = models.DateField(db_index=True)
    end_date = models.DateField(db_index=True)
    price = models.DecimalField(max_digits=16, decimal_places=4, default=0)
    updated_at = models.DateTimeField(null=True, blank=True)
    usage = JSONField(null=True, blank=True)
    state = models.CharField(max_length=32, db_index=True, choices=CLIENT_BILLING_STATES_CHOICES,
                             default=ClientBillingStates.settled)

    @property
    def start_date_dt_utc(self):
        dt = datetime.datetime
        return dt.combine(self.start_date, dt.min.time()).replace(tzinfo=timezone.utc)

    @property
    def end_date_dt_utc(self):
        dt = datetime.datetime
        return dt.combine(self.end_date, dt.min.time()).replace(tzinfo=timezone.utc)

    def __str__(self):
        return '{}'.format(self.service_dynamic_usage.service.client)


@python_2_unicode_compatible
class BillingResource(models.Model):
    """Describes a billable resource

    display_name: the resource named usable for display
    type: a resource type (ex: service, metric, other)
    name: the resource name, the same as the name in an external service.
            For ex: Gnocchi resources are named: instance, instance_disk, a.s.o.
    definition: the resource definition, containing attributes, metrics and anything useful for billing
    """
    display_name = models.CharField(max_length=255)
    type = models.CharField(max_length=128, db_index=True)
    name = models.CharField(max_length=128, db_index=True)
    definition = JSONField(default=dict())

    class Meta:
        unique_together = ('type', 'name')

    @property
    def attributes(self):
        return self.definition.get('attributes', list())

    def get_attribute_definition(self, name):
        if name is not None:
            for attr in self.attributes:
                if attr.get('name', None) == name:
                    return attr

    def get_attribute_value_size(self, name):
        attr_def = self.get_attribute_definition(name)
        if attr_def:
            return attr_def.get('value_size', None)

    def get_attribute_type(self, name, default='string'):
        attr_def = self.get_attribute_definition(name)
        if attr_def:
            return attr_def.get('type', default)
        return default

    def __str__(self):
        return self.display_name


class PricingRuleManager(models.Manager):
    def get_all_matching_conditions(self, attr_list, plan, additional_filter: Optional[dict] = None):
        """
        Return all PriceRule objects with the highest priority, that match a dict of attributes/traits
        :type attr_list: dict, Ex: [{'name': 'instance_type', 'value': 'm1.tiny', 'type': 'string'},..]
        :type plan: PricingPlan
        :type additional_filter: Optional[dict]
        """
        result = list()
        query = self.filter(plan=plan)
        if additional_filter:
            query = query.filter(**additional_filter)
        for price_rule in query.order_by('priority'):
            if price_rule.conditions_match(attr_list):
                if not len(result):
                    result.append(price_rule)
                else:
                    if result[0].priority == price_rule.priority:
                        result.append(price_rule)
                    elif result[0].priority < price_rule.priority:
                        # No need to check further, we reached rules with lower priorities
                        break
        return result


@python_2_unicode_compatible
class PricingRule(models.Model):
    display_name = models.CharField(max_length=255)
    plan = models.ForeignKey(PricingPlan, related_name='pricing_rules', on_delete=models.CASCADE)
    resource = models.ForeignKey(BillingResource, related_name='pricing_rules', on_delete=models.CASCADE)
    priority = models.IntegerField(default=1, db_index=True)
    pricing = JSONField()

    objects = PricingRuleManager()

    def get_currency(self):
        # TODO(tomo): Remove this function ?
        if self.plan.currency is not None:
            return self.plan.currency
        else:
            return Currency.objects.get_default_or_first()

    def price_in_currency(self, currency):
        # TODO(tomo): Remove this function
        from_currency = self.get_currency()  # PriceRule currency
        # If we have the price rule currency and the new currency is different, convert the price
        return convert_currency(self.price, from_currency, currency) if from_currency else self.price

    def conditions_match(self, attributes_list):
        # TODO(tomo): Remove this function
        # Uncomment this to disable matching of any rule without conditions
        # conditions = self.conditions.all()
        # if not len(conditions):
        #     return False
        for condition in self.conditions.all():
            if not condition.match(attributes_list):
                return False
        return True

    def get_matching_modifiers(self, attributes_list):
        # TODO(tomo): Remove this function
        modifiers = list()
        for modifier in self.modifiers.all():
            if modifier.match(attr_list=attributes_list):
                modifiers.append(modifier)
        return modifiers

    def get_pricing_def(self, currency=None):
        """
        Get and augment the tiers definition to ease further processing.
        The resulting tier definition, sorted by 'f', will be:
        [{'f': 0, 't': 1000, 'p': 0.1}, {'f': 1000, 't': 0, 'p': 0.01}]
        A 't' of 0 means anything above the 'f' value.
        """
        # Convert the values to decimal
        tiers = [dict(f=decimal.Decimal(t['f']),
                      p=decimal.Decimal(t['p'])) for t in self.pricing.get('prices', list())]
        # Sort the list by the "f" field
        sorted_tiers = sorted(tiers, key=itemgetter('f'))
        index = 1
        t_len = len(sorted_tiers)
        for t in sorted_tiers:
            if index < t_len:
                t['t'] = sorted_tiers[index]['f']
            else:
                t['t'] = decimal.Decimal(0)
            # Convert to currency if present
            if currency:
                t['p'] = convert_currency(t['p'], from_currency=self.get_currency(), to_currency=currency)
            index += 1
        return sorted_tiers

    @property
    def price(self):
        # TODO(tomo): Fix this, in cases we don't need tiers but we do have them defined
        pricing_def = self.pricing.get('prices', list())
        if len(pricing_def) == 1:
            return decimal.Decimal(six.text_type(pricing_def[0]['p']))
        elif len(pricing_def) == 0:
            return decimal.Decimal('0')

    @property
    def min_price(self):
        prices = self.pricing.get('prices', list())
        if len(prices) == 0:
            return decimal.Decimal('0')

        min_price = decimal.Decimal(math.inf)
        for price in prices:
            if price['p'] < min_price:
                min_price = price['p']

        return min_price

    @property
    def attribute(self):
        # TODO(tomo): This property is kept for backwards compatibility. Remove it.
        return self.pricing.get('attribute', None)

    @property
    def attribute_unit(self):
        return self.pricing.get('attribute_unit', None)

    @property
    def time_unit(self):
        return self.pricing.get('time_unit', 'bc')

    @property
    def time_unit_seconds(self):
        return time_unit_seconds(self.time_unit, 1)

    @property
    def resource_type(self):
        return self.resource.type

    @property
    def resource_name(self):
        return self.resource.name

    def get_display_unit(self):
        """Returns a formatted string for display purposes"""
        value_unit = self.attribute_unit or self.resource.display_name
        return get_display_unit(value_unit=value_unit, time_unit=self.time_unit)

    def __str__(self):
        return self.display_name


@python_2_unicode_compatible
class PricingRuleCondition(models.Model):
    name = models.CharField(max_length=128, default='condition')
    price_rule = models.ForeignKey(PricingRule, related_name='conditions', on_delete=models.CASCADE)
    attribute = models.CharField(max_length=128, db_index=True)
    attribute_unit = models.CharField(max_length=4, choices=ATTRIBUTE_UNITS, null=True, blank=True)
    operator = models.CharField(max_length=2, choices=NUMBER_COMPARATORS, default=STRING_COMPARATORS[0][0])
    value = JSONField()

    def get_attribute_type(self, default='string'):
        """Get the attribute type from the resource definition or return a default"""
        return self.price_rule.resource.get_attribute_type(self.attribute, default=default)

    def get_attribute_value_size(self):
        return self.price_rule.resource.get_attribute_value_size(name=self.attribute)

    def match(self, attr_list):
        for attr in attr_list:
            if attr.get('name', None) == self.attribute:
                # NOTE(tomo): We overwrite the attribute type with the Resource definition type
                return attribute_match(attr_value=attr.get('value', None),
                                       match_value=self.value,
                                       attr_type=self.get_attribute_type(default=attr.get('type', 'string')),
                                       compare_value_size=self.attribute_unit,
                                       original_value_size=self.get_attribute_value_size(),
                                       op=self.operator)
        return False

    def __str__(self):
        return "{} - {}".format(self.price_rule.display_name, self.name)


@python_2_unicode_compatible
class PricingRuleModifier(models.Model):
    name = models.CharField(max_length=128, default='modifier')
    price_rule = models.ForeignKey(PricingRule, related_name='modifiers', on_delete=models.CASCADE)
    attribute = models.CharField(max_length=128, db_index=True)
    attribute_unit = models.CharField(max_length=4, choices=ATTRIBUTE_UNITS, null=True, blank=True)
    operator = models.CharField(max_length=2, choices=NUMBER_COMPARATORS, default=STRING_COMPARATORS[0][0])
    value = JSONField()
    price = models.DecimalField(max_digits=12, decimal_places=4)
    time_unit = models.CharField(max_length=3, choices=TIME_UNITS)
    price_is_percent = models.BooleanField(default=False, help_text='Weather the price is a percent or an actual price')

    def price_in_currency(self, currency):
        from_currency = self.price_rule.get_currency()  # PricingRule currency
        # If we have the price rule currency and the new currency is different, convert the price
        return convert_currency(self.price, from_currency, currency) if from_currency else self.price

    def get_attribute_type(self, default='string'):
        """Get the attribute type from the resource definition or return a default"""
        return self.price_rule.resource.get_attribute_type(self.attribute, default=default)

    def get_attribute_value_size(self):
        """Resource attributes can have a value_size property defined as b, k, m (Bytes, Kilo,...)"""
        return self.price_rule.resource.get_attribute_value_size(name=self.attribute)

    def get_matching_attribute(self, attr_list):
        for attr in attr_list:
            if attr['name'] == self.attribute:
                # NOTE(tomo): We overwrite the attribute type with the Resource definition type
                if attribute_match(attr_value=attr['value'],
                                   match_value=self.value,
                                   attr_type=self.get_attribute_type(default=attr.get('type', 'string')),
                                   compare_value_size=self.attribute_unit,
                                   original_value_size=self.get_attribute_value_size(),
                                   op=self.operator):
                    return attr
        return None

    def match(self, attr_list):
        """
        Match the self.attribute against a list of attribute definitions.
        An attr_list example: [{'name': 'size', 'value': 2, 'type': 'integer'}...]
        Do note that while the attr_list may contain a type, we usually relay on self.get_attribute_type
        The attr_list is usually the traits list coming from OpenStack directly.
        The attr_list may include a type for an attribute, however, that type may not be a correct type,
        thus we allow type overwrite in the resource attribute definition.
        """
        if self.get_matching_attribute(attr_list) is None:
            return False
        else:
            return True

    @property
    def time_unit_seconds(self):
        return time_unit_seconds(self.time_unit, 1)

    def get_display_unit(self):
        """Returns a formatted string for display purposes"""
        return get_display_unit(value_unit=self.attribute_unit, time_unit=self.time_unit)

    def __str__(self):
        return "{}".format(self.name)


class ResourceUsageLogManager(models.Manager):
    def add_event(self, resource_type, resource_uuid, project_id, user_id, start, end, traits, region=None):
        """
        Add new resource usage data.
        If we already have a resource with .resource_uuid and the same .start, we set the
         previous usage .end to the current data .start.
        """
        same_resource = self.filter(resource_uuid=resource_uuid, start=start).first()
        if same_resource:
            # Resource with start date already exists. We treat this as the same resource
            # We only modify it's end date in case this event has the end date set.
            if same_resource.end is None and end is not None:
                same_resource.end = end
                same_resource.save()
            else:
                if end:
                    same_resource = self.filter(resource_uuid=resource_uuid, start__lt=end).order_by('start').last()
                if same_resource and same_resource.end is None:
                    same_resource.end = end
                    same_resource.save()
            # TODO(tomo): Update relevant traits since a new event can contain modified ones
            #             and we need a way to keep the display_name up to date for example
            return same_resource

        started_before = self.filter(resource_uuid=resource_uuid, start__lt=start).order_by('start').last()
        if started_before:
            if started_before.end and started_before.end > start:
                end = started_before.end
            started_before.end = start
            started_before.save()
        started_after = self.filter(resource_uuid=resource_uuid, start__gt=start).order_by('start').first()
        if started_after and end is None:
            end = started_after.start
        return self.create(resource_type=resource_type,
                           resource_uuid=resource_uuid,
                           project_id=project_id,
                           user_id=user_id,
                           start=start,
                           end=end,
                           region=region,
                           traits=traits)

    def get_active_between(self, start_date, end_date, **kwargs):
        """Get active resources during start_date and end_date"""
        return self.filter(models.Q(start__lt=end_date),
                           models.Q(end__gte=start_date) | models.Q(end__isnull=True), **kwargs)


@python_2_unicode_compatible
class ResourceUsageLog(models.Model):
    """Keeps resources data from events, needed for billing."""
    resource_type = models.CharField(max_length=128)
    resource_uuid = models.UUIDField(db_index=True)
    project_id = models.UUIDField(null=True, blank=True)
    user_id = models.UUIDField(null=True, blank=True)
    # Resource created at
    start = models.DateTimeField(db_index=True)
    # Resource ended at
    end = models.DateTimeField(null=True, blank=True)
    # Resource region if resource is Region bound
    region = models.CharField(max_length=255, null=True, blank=True)
    # Event traits
    traits = JSONField()

    objects = ResourceUsageLogManager()

    class Meta:
        unique_together = ('resource_uuid', 'end')

    def get_trait_value(self, name):
        for trait in self.traits:
            if trait['name'] == name:
                return trait['value']
        return None

    def __str__(self):
        return '{} {} {} {}'.format(self.resource_type, self.resource_uuid, self.end, self.id)


""" New replacement for ResourceUsageLog
class ResourceUsage(models.Model):
    resource = models.ForeignKey(OpenstackResource, related_name='usage', db_index=True, on_delete=models.CASCADE)
    resource_uuid = models.UUIDField(db_index=True, unique=True)
    project_id = models.UUIDField(null=True, blank=True)
    user_id = models.UUIDField(null=True, blank=True)
    # Resource created at
    created_at = models.DateTimeField(db_index=True)
    # Resource ended at
    ended_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('resource', 'resource_uuid')

    def __str__(self):
        return '{} {} {}'.format(self.resource.resource_type, self.resource_uuid, self.ended_at)


class ResourceUsageAttributeManager(models.Manager):
    def create_value(self, **kwargs):
        # FIXME(tomo): Check kwargs['type'] against ATTRIBUTE_TYPES
        value_field_name = '{}_value'.format(kwargs['type'])
        kwargs[value_field_name] = kwargs.pop('value')
        return self.create(**kwargs)

    def add_value(self, **kwargs):
        value_field_name = '{}_value'.format(kwargs.get('type', ATTRIBUTE_TYPE[0][0]))
        kwargs[value_field_name] = kwargs.pop('value')

        same_start = self.filter(resource_usage=kwargs['resource_usage'], name=kwargs['name'],
                                 start=kwargs['start']).first()
        if same_start:
            return same_start

        started_before = self.filter(resource_usage=kwargs['resource_usage'], name=kwargs['name'],
                                     start__lt=kwargs['start']).order_by('start').last()
        if started_before:
            if started_before.get_value() == kwargs[value_field_name]:
                return started_before

        started_after = self.filter(resource_usage=kwargs['resource_usage'], name=kwargs['name'],
                                    start__gt=kwargs['start']).order_by('start').first()
        if started_after:
            if started_after.get_value() == kwargs[value_field_name]:
                started_after.start = kwargs['start']
                started_after.save()
                return started_after

        return self.create(**kwargs)


class ResourceUsageAttribute(models.Model):
    resource_usage = models.ForeignKey(ResourceUsage, related_name='attributes', db_index=True,
     on_delete=models.CASCADE)
    name = models.CharField(max_length=128, db_index=True)
    type = models.CharField(choices=ATTRIBUTE_TYPE, max_length=10)
    string_value = models.CharField(max_length=255, null=True)
    number_value = models.FloatField(null=True)
    datetime_value = models.DateTimeField(null=True)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True)

    objects = ResourceUsageAttributeManager()

    def get_value(self):
        return getattr(self, '{}_value'.format(self.type))

    def __str__(self):
        return '{} {}'.format(self.name, self.type)

"""

"""
class BillableResourceHistoryManager(models.Manager):
    def create_from_details(self, details, project_id, resource_id, **kwargs):
        for res_type, res_hist in iter(details.items()):
            for res in res_hist:
                for hist in res['history']:
                    hist['rule'] = hist['rule'].id
                    for metric in hist['metrics']:
                        metric['metric'] = metric['metric'].id
                    for modifier in hist['modifiers']:
                        modifier['modifier'] = modifier['modifier'].id


class BillableResourceHistory(models.Model):
    project_id = models.CharField(max_length=64, db_index=True)
    resource_type = models.CharField(max_length=128, db_index=True)
    resource_id = models.CharField(max_length=64, db_index=True)
    quantity = models.DecimalField(max_digits=14, decimal_places=2)
    price_rule = models.ForeignKey(PriceRule, related_name='billable_resource_history')
    start = models.DateTimeField()
    end = models.DateTimeField()
    details = JSONField()


class BillableResourceMetricsHistory(models.Model):
    billable_resource_history = models.ForeignKey(BillableResourceHistory, related_name='metrics')
    metric = models.ForeignKey(PriceRuleMetric, related_name='billable_resource_metrics_history')
    value = models.FloatField()


class BillableResourceModifiersHistory(models.Model):
    billable_resource_history = models.ForeignKey(BillableResourceHistory, related_name='modifiers')
    modifier = models.ForeignKey(PriceRuleModifier, related_name='billable_resource_modifiers_history')
    start = models.DateTimeField()
    end = models.DateTimeField()
"""
