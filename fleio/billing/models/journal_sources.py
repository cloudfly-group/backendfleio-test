from django.utils.translation import ugettext_lazy as _


class JournalSources(object):
    """Source and destination choices"""
    credit = 'cr'
    credit_tax = 'tx'
    invoice = 'iv'
    transaction = 'tr'
    staff = 'st'
    settlement = 'se'
    external = 'ex'

    sources_map = {
        credit: _('Client Credit'),
        invoice: _('Invoice'),
        transaction: _('Transaction'),
        staff: _('Staff'),
        settlement: _('Settlement'),
        external: _('External'),
        credit_tax: _('Credit tax'),
    }


SOURCE_CHOICES = (
    (JournalSources.credit, _('Client Credit')),
    (JournalSources.invoice, _('Invoice')),
    (JournalSources.transaction, _('Transaction')),
    (JournalSources.staff, _('Staff')),
    (JournalSources.settlement, _('Settlement')),
    (JournalSources.external, _('External')),
    (JournalSources.credit_tax, _('Credit tax')),
)
