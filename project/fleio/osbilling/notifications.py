import copy
from decimal import Decimal
import logging

from fleio.billing.estimated_usage import EstimatedUsage
from fleio.billing.estimated_usage import UsageCycle
from fleio.billing.models import Service
from fleio.billing.usage_settings import UsageSettings

from . import utils

LOG = logging.getLogger(__name__)


def get_active_resources(usage, accounting_end):
    """
    Returns a list of all active resources histories.
    The list includes the active modifiers for each resource.
    An active resource is a resource that has the end datetime equal
    to the usage last update datetime.
    :type usage: dict, entire usage dict from a ClientBilling
    :type accounting_end: datetime.datetime object, when the usage was last updated
    """
    active_resources = []
    for usage_detail in usage.get('usage_details', []):
        for usage in usage_detail.get('usage', []):
            for resource_history in usage['history']:
                if resource_history['end'] == accounting_end:
                    # The end for this resource is accounting_end, meaning it is active
                    active_resource_history = copy.deepcopy(resource_history)
                    # Keep active modifiers only
                    active_modifiers = []
                    for modifier in active_resource_history.get('modifiers', []):
                        if modifier['end'] == accounting_end:
                            active_modifiers.append(modifier)
                    active_resource_history['modifiers'] = active_modifiers
                    active_resources.append(active_resource_history)
    return active_resources


def get_estimated_usage(service: Service, usage_settings: UsageSettings) -> EstimatedUsage:
    try:
        service_dynamic_usage = service.service_dynamic_usage
    except Exception as e:
        del e
        LOG.error('Get estimated usage called for client without client billing {0}, aborting'.format(service.client))
        return EstimatedUsage()

    if service_dynamic_usage is None:
        LOG.error('Get estimated usage called for client without client billing {0}, aborting'.format(service.client))
        return EstimatedUsage()

    active_resources = get_active_resources(
        usage=service_dynamic_usage.get_usage(),
        accounting_end=service_dynamic_usage.updated_at
    )

    usage_cycle = UsageCycle(
        Decimal(0),
        service_dynamic_usage.end_date,
        service_dynamic_usage.get_next_billing_date,
        usage_settings=usage_settings
    )

    for active_resource in active_resources:
        # we are only interested in resources that apply for a billing cycle
        if active_resource['price_details']['time_unit'] == 'bc':
            usage_cycle.add_fixed_price(Decimal(active_resource['price']))
        else:
            unit_price = active_resource['price_details']['unit_price']
            quantity = active_resource['attribute_value']
            price_seconds = utils.time_unit_seconds(active_resource['price_details']['time_unit'])
            start_time = active_resource['start']
            price_per_second = utils.cdecimal(
                unit_price * quantity / price_seconds,
                q='0.00000000000001',
                rounding='ROUND_DOWN'
            )
            usage_cycle.add_dynamic_resource(
                price_per_second=price_per_second,
                price_per_unit=unit_price * quantity,
                seconds_per_unit=price_seconds,
                start_datetime=start_time)

            # Calculate modifiers prices also
            for modifier in active_resource.get('modifiers', []):
                mod_time_unit = modifier['price_details']['time_unit']
                if mod_time_unit == 'bc':
                    usage_cycle.add_fixed_price(Decimal(modifier['price']))
                else:
                    mod_price_seconds = utils.time_unit_seconds(mod_time_unit)
                    mod_unit_price = modifier['price_details']['unit_price']
                    mod_price_per_second = utils.cdecimal(
                        mod_unit_price / mod_price_seconds,
                        q='0.00000000000001',
                        rounding='ROUND_DOWN'
                    )
                    usage_cycle.add_dynamic_resource(
                        price_per_second=mod_price_per_second,
                        price_per_unit=mod_unit_price,
                        seconds_per_unit=mod_price_seconds,
                        start_datetime=start_time)

    # add price per second
    estimated_usage = EstimatedUsage()
    estimated_usage.add_usage_cycle(usage_cycle)

    return estimated_usage
