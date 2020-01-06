import pycountry
from django.db import IntegrityError
from django.db import models
from django.utils.timezone import now as utcnow
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class TaxRuleManager(models.QuerySet):
    def for_country(self, country):
        return self.filter(country=country)


class TaxRule(models.Model):
    LEVELS = (1, 'Level 1'), (2, 'Level 2')
    level = models.PositiveSmallIntegerField(choices=LEVELS, default=1)
    name = models.CharField(max_length=32)
    state = models.CharField(max_length=255, null=True, blank=False)
    country = models.CharField(max_length=80, db_index=True, choices=[(country.name, country.name)
                                                                      for country in pycountry.countries])
    rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)

    objects = TaxRuleManager.as_manager()

    @staticmethod
    def for_country_and_state(country, state=None):
        tax_rules = TaxRule.objects.for_country(country=country).all()
        applicable_tax_rules = []
        current_date = utcnow().date()

        for tax_rule in tax_rules:
            if tax_rule.state and not tax_rule.state == state:
                continue

            if tax_rule.start_date > current_date:
                continue

            if tax_rule.end_date and tax_rule.end_date < current_date:
                continue

            applicable_tax_rules.append(tax_rule)

        return applicable_tax_rules

    def __str__(self):
        return '{} {} {} {} {} {}%'.format(self.name, self.country, self.state, self.start_date,
                                           self.end_date, self.rate)

    def save(self, *args, **kwargs):
        # prevent from overlapping with existing tax rules from same country, state, name and level
        # exclude self (if updating)
        conflicting_tax_rules = TaxRule.objects.filter(country=self.country, state=self.state,
                                                       name=self.name, level=self.level).exclude(pk=self.pk)
        conflicting_tax_rules_list = list()
        for tax_rule in conflicting_tax_rules:
            if self.end_date:
                # Existing rule ---start------------end----------
                # Current rule  ----------start-----------end----
                if tax_rule.start_date <= self.start_date and tax_rule.end_date and self.start_date < tax_rule.end_date:
                    conflicting_tax_rules_list.append(str(tax_rule))
                # Existing rule ---------------s---------e-------
                # Current rule  ----------s-----------e----------
                elif self.start_date < tax_rule.start_date < self.end_date:
                    conflicting_tax_rules_list.append(str(tax_rule))
            # Existing rule ---------------s-----------------
            # Current rule  ----------s----------------------
            elif tax_rule.start_date > self.start_date:
                conflicting_tax_rules_list.append(str(tax_rule))

        if conflicting_tax_rules_list:
            raise IntegrityError(
                _('Tax rule {} start and/or end date are conflicting with existing tax rules: {}'.
                  format(self, conflicting_tax_rules_list)))

        # end rules that don't have an end date set and began before the current tax rate
        # Existing rules ------s--------------------------
        # Current rules  ----------s-----------e----------
        pre_rules = TaxRule.objects.filter(country=self.country, state=self.state, name=self.name, level=self.level,
                                           start_date__lte=self.start_date, end_date__isnull=True)
        # Existing rules ------s---e----------------------
        # Current rules  ----------s-----------e----------
        pre_rules.update(end_date=self.start_date)
        super(TaxRule, self).save()
