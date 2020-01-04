import logging
from django import apps
from django.utils.translation import ugettext_lazy as _
from importlib import import_module

from fleio.activitylog.formatting import logclass_text

LOG = logging.getLogger(__name__)

logclass_text['cron process clients'] = _('Processing clients from cron.')

logclass_text['paypal payment'] = _('Invoice {invoice_id} was paid using paypal.')
logclass_text['paypal payment refund'] = _('A refund was made for {invoice_id} using paypal.')

logclass_text['romcard payment'] = _('Invoice {invoice_id} was paid using romcard.')
logclass_text['romcard payment refund'] = _('A refund was made for {invoice_id} using romcard.')

logclass_text['payu payment'] = _('Invoice {invoice_id} was paid using payU.')
logclass_text['payu payment refund'] = _('A refund was made for {invoice_id} using payU.')

logclass_text['stripe payment'] = _('Invoice {invoice_id} was paid using stripe.')
logclass_text['stripe payment refund'] = _('A refund was made for {invoice_id} using stripe.')

logclass_text['payuro payment'] = _('Invoice {invoice_id} was paid using PayU RO.')
logclass_text['payuro payment refund'] = _('A refund was made for {invoice_id} using PayU RO.')


class AppConfig(apps.AppConfig):
    name = 'fleio.billing'
    verbose_name = 'Fleio Billing App'

    def ready(self):
        try:
            import_module('fleio.billing.signals.handlers')
            import_module('fleio.billing.signals.signals')
            import_module('fleio.billing.permissions')
        except ImportError as e:
            LOG.exception(e)
