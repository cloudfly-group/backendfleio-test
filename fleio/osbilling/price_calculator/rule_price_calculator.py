from decimal import Decimal
from typing import Optional, Tuple

import math

from fleio.core.models import Currency
from fleio.osbilling.models import PricingRule
from fleio.osbilling.price_calculator.monetary_amount import MonetaryAmount
from fleio.osbilling.price_calculator.price_tier import PriceTier
from fleio.osbilling.utils import resize_to, time_unit_seconds


class RulePriceCalculator:
    def __init__(self, rule: PricingRule, currency: Currency):
        self.has_conditions = rule.conditions.count() > 0
        self.price_tiers = []
        self.max_price = MonetaryAmount(Decimal(0), currency)
        self.min_price = MonetaryAmount(Decimal(math.inf), currency)
        self.time_unit = rule.pricing['time_unit']
        self.time_unit_seconds = Decimal(time_unit_seconds(self.time_unit))
        self.attribute_unit = rule.pricing['attribute_unit']
        if self.attribute_unit:
            self.attribute_unit_bytes = Decimal(resize_to(1, self.attribute_unit, 'b'))

        pricing_def = rule.get_pricing_def()
        for price_tier in pricing_def:
            price_tier_obj = PriceTier(
                applies_from=price_tier['f'],
                applies_to=price_tier['t'],
                price=price_tier['p'],
                currency=currency,
            )
            if price_tier_obj.price > self.max_price:
                self.max_price = price_tier_obj.price
            if price_tier_obj.price < self.min_price:
                self.min_price = price_tier_obj.price

    def get_multipliers(
            self, time_unit: Optional[str] = None, attribute_unit: Optional[str] = None
    ) -> Tuple[Decimal, Decimal]:
        time_multiplier = Decimal(1)
        attribute_multiplier = Decimal(1)

        if time_unit and time_unit != self.time_unit:
            time_multiplier = Decimal(time_unit_seconds(time_unit)) / self.time_unit_seconds

        if attribute_unit and self.attribute_unit and attribute_unit != self.attribute_unit:
            attribute_multiplier = Decimal(resize_to(1, attribute_unit, 'b')) / self.attribute_unit_bytes

        return time_multiplier, attribute_multiplier

    def get_max_price(
            self, time_unit: Optional[str] = None, attribute_unit: Optional[str] = None,
    ) -> MonetaryAmount:
        time_multiplier, attribute_multiplier = self.get_multipliers(
            time_unit=time_unit,
            attribute_unit=attribute_unit,
        )
        return self.max_price * time_multiplier * attribute_multiplier

    def get_min_price(
            self, time_unit: Optional[str] = None, attribute_unit: Optional[str] = None,
    ) -> MonetaryAmount:
        time_multiplier, attribute_multiplier = self.get_multipliers(
            time_unit=time_unit,
            attribute_unit=attribute_unit,
        )
        return self.min_price * time_multiplier * attribute_multiplier
