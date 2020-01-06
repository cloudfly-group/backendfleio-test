from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class BankConfig(AppConfig):
    name = "fleio.billing.gateways.bank"
    verbose_name = _("Bank Transfer")
    fleio_module_type = 'payment_gateway'
    module_settings = {'capabilities': {
        'can_process_payments': False,
        'returns_fee_information': False
    }}
