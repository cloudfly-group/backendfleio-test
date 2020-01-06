import logging
import decimal

from django.db import models

from fleio.core.models import Client, Currency

LOG = logging.getLogger(__name__)


class ClientCreditQueryset(models.QuerySet):
    def deposit(self, client, currency, amount):
        client_credit, created = self.get_or_create(client=client,
                                                    currency=currency,
                                                    defaults={'amount': amount})
        if not created:
            client_credit.deposit(amount)
        return client_credit

    def withdraw(self, client, currency, amount):
        if amount < 0:
            LOG.warning('withdrawing negative amount from {} credit'.format(client.name))
        client_credit, created = self.get_or_create(client=client,
                                                    currency=currency,
                                                    defaults={'amount': -amount})
        if not created:
            client_credit.withdraw(amount)
        return client_credit


class ClientCredit(models.Model):
    # FIXME(tomo): Deleting a client account will delete any existing balance
    # we need to make sure we do not lose track of this. Try to add a journal log for
    # the existing credit
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='credits')
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=14, decimal_places=2, default=decimal.Decimal('0.00'))

    objects = ClientCreditQueryset.as_manager()

    class Meta:
        app_label = 'billing'
        unique_together = ('client', 'currency')

    def deposit(self, amount):
        self.amount += amount
        self.save(update_fields=['amount'])

    def withdraw(self, amount):
        if amount < 0:
            LOG.warning('withdrawing negative amount from {} credit'.format(self.client.name))
        self.amount -= amount
        self.save(update_fields=['amount'])

    def __str__(self):
        return '{} {} {}'.format(self.client.name, self.amount, self.currency.code)
