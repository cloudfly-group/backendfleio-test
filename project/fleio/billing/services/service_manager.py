import decimal
import datetime

from django.db import transaction
from django.utils.timezone import now as utcnow

from fleio.billing.settings import CyclePeriods
from fleio.billing.settings import OrderStatus
from fleio.billing.settlement_manager import SettlementManager
from fleio.billing import utils
from fleio.billing.models import Order
from fleio.billing.models import Product
from fleio.billing.models import OrderItemTypes
from fleio.billing.models import ProductCycle
from fleio.billing.models import Service


class ServiceManager:
    @staticmethod
    def get_new_cycle_due_date(service: Service, cycle: ProductCycle, start_date):
        """Get the new cycle next due date relative to the current due date"""
        if not cycle or cycle.cycle == CyclePeriods.onetime:
            return start_date
        prev_dd = service.get_previous_due_date()
        # FIXME(tomo): service may be missing next due date. Need to fix this at the source
        next_dd = service.next_due_date or utcnow()
        new_dd = cycle.get_next_due_date(prev_dd, cycle.cycle_multiplier, cycle.cycle)
        if new_dd <= next_dd:
            return new_dd
        else:
            return next_dd

    @staticmethod
    def estimate_new_service_cycle_seconds(service: Service, product: Product, cycle: ProductCycle, start_date):
        """Change the service product and cycle and updates the service and invoice due dates"""
        prev_dd = service.get_previous_due_date()
        # FIXME(tomo): service may be missing next due date. Need to fix this at the source
        next_dd = service.next_due_date or utcnow()
        new_dd = ServiceManager.get_new_cycle_due_date(service, cycle, start_date)
        if start_date < prev_dd:
            # NOTE(tomo): Previous due date was calculated manually and we may have a problem when we add a day to
            # the next due date for cases like Oct 31 to dec 1 for a monthly cycle since Nov does not have 31 days.
            # and so we need to subtract 1 day from prev_dd in this case.
            temp_prev_dd = (prev_dd - datetime.timedelta(days=1))
            old_cycle_used_seconds = int((start_date - temp_prev_dd).total_seconds())
            old_cycle_total_seconds = int((next_dd - temp_prev_dd).total_seconds())
            new_cycle_seconds = int((new_dd - temp_prev_dd).total_seconds())
        else:
            old_cycle_used_seconds = int((start_date - prev_dd).total_seconds())
            old_cycle_total_seconds = int((next_dd - prev_dd).total_seconds())
            new_cycle_seconds = int((new_dd - prev_dd).total_seconds())
        old_cycle_remaining_seconds = int((next_dd - start_date).total_seconds())
        if product.is_free or not cycle or cycle.cycle == CyclePeriods.onetime:
            new_cycle_seconds = 0
            new_cycle_over_seconds = 0
            new_cycle_remaining_seconds = 0
        else:
            new_cycle_remaining_seconds = int((new_dd - start_date).total_seconds())
            new_cycle_over_seconds = int((new_dd - next_dd).total_seconds())
        return {'old_cycle_used_seconds': old_cycle_used_seconds,
                'old_cycle_remaining_seconds': old_cycle_remaining_seconds,
                'old_cycle_seconds': old_cycle_total_seconds,
                'new_cycle_seconds': new_cycle_seconds,
                'new_cycle_remaining_seconds': new_cycle_remaining_seconds,
                'new_cycle_over_seconds': new_cycle_over_seconds}

    @staticmethod
    def estimate_new_config_options_cost(service: Service, cycle: ProductCycle,
                                         configurable_options, seconds_estimate):
        options_upgrade_summary = []
        zero = decimal.Decimal('0.00')
        client = service.client

        for config_option in configurable_options:
            new_option = config_option['option']
            old_option = service.configurable_options.filter(option=new_option).first()
            new_price_set = False
            choice_value = None
            has_price = True
            if config_option['option'].widget == 'text_in':
                has_price = False
            quantity = config_option.get('quantity')
            if config_option['option'].has_choices:
                choice_value = config_option['option_value']
            # filter out all configurable options that do not have the product cycles
            if not config_option['option'].has_cycle(
                    cycle=cycle.cycle,
                    cycle_multiplier=cycle.cycle_multiplier,
                    choice_value=choice_value,
                    currency=client.currency.code,
            ):
                continue
            if not new_price_set and has_price:
                unit_price, price, setupfee = config_option['option'].get_price_by_cycle_quantity_and_choice(
                    cycle_name=cycle.cycle,
                    cycle_multiplier=cycle.cycle_multiplier,
                    currency=client.currency,
                    quantity=quantity,
                    choice_value=choice_value,
                    option_value=config_option['option_value'],
                )
                if seconds_estimate['new_cycle_seconds'] > 0:
                    unit_price_per_second = unit_price / seconds_estimate['new_cycle_seconds']
                    unit_remaining_price = (unit_price_per_second * seconds_estimate['new_cycle_remaining_seconds'])
                    remaining_price = unit_remaining_price * quantity
                else:
                    unit_remaining_price = remaining_price = zero
            else:
                unit_price, price, setupfee = zero, zero, zero  # noqa
                unit_remaining_price = remaining_price = zero

            if old_option:
                if has_price:
                    old_choice_value = old_option.option_value
                    (old_unit_price,
                     old_price,
                     old_setupfee) = new_option.get_price_by_cycle_quantity_and_choice(
                        cycle_name=service.cycle.cycle,
                        cycle_multiplier=service.cycle.cycle_multiplier,
                        currency=client.currency,
                        quantity=old_option.quantity,
                        choice_value=old_choice_value,
                        option_value=old_choice_value,
                    )
                    if seconds_estimate['old_cycle_seconds'] > 0:
                        current_cycle_cost_per_second = old_unit_price / seconds_estimate['old_cycle_seconds']
                        remaining_unit_cost = (current_cycle_cost_per_second *
                                               seconds_estimate['old_cycle_remaining_seconds'])
                        remaining_cost = remaining_unit_cost * old_option.quantity
                    else:
                        remaining_cost = remaining_unit_cost = zero
                    upgrade_unit_cost = utils.cdecimal(unit_remaining_price - remaining_unit_cost, q='.01')
                    upgrade_cost = utils.cdecimal(remaining_price - remaining_cost, q='.01')
                else:
                    upgrade_cost = upgrade_unit_cost = zero
                if config_option['option'].widget == 'yesno' and config_option['option_value'] != 'yes':
                    display_name = '{} => {}: {}'.format(old_option.display,
                                                         old_option.display,
                                                         config_option['option_value'])
                else:
                    display_name = '{} => {}: {}'.format(old_option.display,
                                                         new_option.description,
                                                         config_option['option_value'])
                upgrade_option = {'display_name': display_name,
                                  'is_free': not has_price,
                                  'option': config_option['option'].pk,
                                  'option_value': config_option['option_value'],
                                  'price': upgrade_cost,
                                  'upgrade_cost': upgrade_cost,
                                  'has_price': has_price,
                                  'taxable': True,
                                  'unit_price': upgrade_unit_cost,
                                  'quantity': quantity,
                                  'setupfee': setupfee}
                options_upgrade_summary.append(upgrade_option)
            else:
                options_upgrade_summary.append({'display_name': '{}: {}'.format(new_option.description,
                                                                                config_option['option_value']),
                                                'is_free': not has_price,
                                                'option_value': config_option['option_value'],
                                                'option': config_option['option'].pk,
                                                'price': price,
                                                'upgrade_cost': utils.cdecimal(remaining_price, q='.01'),
                                                'has_price': has_price,
                                                'taxable': True,
                                                'unit_price': unit_price,
                                                'quantity': quantity,
                                                'setupfee': setupfee})
        return options_upgrade_summary

    @staticmethod
    def estimate_new_service_cycle_cost(service: Service, product: Product, cycle: ProductCycle, start_date,
                                        configurable_options=None):
        client = service.client
        zero = decimal.Decimal('0.00')
        opt_sum = []
        seconds_estimate = ServiceManager.estimate_new_service_cycle_seconds(service=service,
                                                                             product=product,
                                                                             cycle=cycle,
                                                                             start_date=start_date)
        if cycle and not product.is_free:
            new_cycle_cost = utils.convert_currency(cycle.fixed_price, cycle.currency, client.currency)
            if seconds_estimate['new_cycle_seconds'] > 0:
                new_cycle_cost_per_second = new_cycle_cost / seconds_estimate['new_cycle_seconds']
                new_cycle_remaining_cost = new_cycle_cost_per_second * seconds_estimate['new_cycle_remaining_seconds']
            else:
                new_cycle_remaining_cost = zero
                new_cycle_cost = zero
        else:
            new_cycle_cost = zero
            new_cycle_remaining_cost = zero
        if service.product.is_free or service.cycle and service.cycle.cycle == CyclePeriods.onetime:
            remaining_cost = zero
        elif not service.product.is_free and service.cycle:
            current_cycle_cost = service.get_fixed_price_without_configurable_options(currency=client.currency)
            if seconds_estimate['old_cycle_seconds'] > 0:
                current_cycle_cost_per_second = current_cycle_cost / seconds_estimate['old_cycle_seconds']
                remaining_cost = current_cycle_cost_per_second * seconds_estimate['old_cycle_remaining_seconds']
            else:
                remaining_cost = zero
            # Handle configurable options
            if configurable_options:
                opt_sum = ServiceManager.estimate_new_config_options_cost(service=service,
                                                                          cycle=cycle,
                                                                          configurable_options=configurable_options,
                                                                          seconds_estimate=seconds_estimate)
        else:
            remaining_cost = zero
        prod_upgrade_cost = utils.cdecimal(new_cycle_remaining_cost - remaining_cost, q='.01')
        total_upgrade_cost = prod_upgrade_cost
        for opt in opt_sum:
            total_upgrade_cost += opt['upgrade_cost']
        taxable = not client.tax_exempt and product.taxable
        total_price, taxes_applied = SettlementManager.calculate_fixed_price_and_taxes(client=client,
                                                                                       price=total_upgrade_cost,
                                                                                       taxable=taxable)
        new_cycle_cost = utils.cdecimal(new_cycle_cost, q='.01')
        remaining_cost = utils.cdecimal(remaining_cost, q='.01')

        return {'service_remaining_cost': remaining_cost,
                'new_product_price': new_cycle_cost,
                'upgrade_price': total_upgrade_cost,
                'product_upgrade_price': prod_upgrade_cost,
                'taxes_applied': taxes_applied,
                'total_due': total_price,
                'service_id': service.pk,
                'product_id': product.pk,
                'cycle_id': cycle.pk,
                'configurable_options': opt_sum,
                'display_name': '{} => {} ({} {} / {})'.format(service.display_name,
                                                               product.name,
                                                               new_cycle_cost,
                                                               client.currency,
                                                               cycle.display_name),
                'currency': client.currency.code}

    @staticmethod
    def create_service_upgrade_order(user, client, service, product, cycle, start_date, configurable_options=None,
                                     metadata=None):
        upgrade_summary = ServiceManager.estimate_new_service_cycle_cost(service=service,
                                                                         product=product,
                                                                         cycle=cycle,
                                                                         start_date=start_date,
                                                                         configurable_options=configurable_options)
        with transaction.atomic():
            order = Order.objects.create(user=user,
                                         client=client,
                                         currency=client.currency,
                                         client_notes='',
                                         metadata=metadata,
                                         status=OrderStatus.pending)
            upgrade_price = upgrade_summary['product_upgrade_price']
            # fixed_price = upgrade_price if upgrade_price > 0 else 0
            taxable = client and not client.tax_exempt and product.taxable
            order_item = order.items.create(item_type=OrderItemTypes.serviceUpgrade,
                                            product=product,
                                            cycle=cycle,
                                            service=service,
                                            taxable=taxable,
                                            setup_fee=decimal.Decimal('0.00'),
                                            fixed_price=upgrade_price,
                                            name=upgrade_summary['display_name'],
                                            description=upgrade_summary.get('description', ''),
                                            cycle_display=cycle.display_name,
                                            plugin_data=None,
                                            quantity=1)
            if upgrade_summary.get('configurable_options'):
                for config_option in upgrade_summary.get('configurable_options'):
                    order_item.configurable_options.create(option_id=config_option['option'],
                                                           option_value=config_option['option_value'],
                                                           quantity=config_option['quantity'],
                                                           has_price=config_option['has_price'],
                                                           taxable=taxable,
                                                           unit_price=config_option['unit_price'],
                                                           price=config_option['upgrade_cost'],
                                                           setup_fee=config_option['setupfee'])

            for tax_name, amount in upgrade_summary.get('taxes_applied', {}).items():
                order_item.taxes.create(name=tax_name,
                                        amount=amount)
            return SettlementManager.process_order(order)
