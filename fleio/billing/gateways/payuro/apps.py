from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class PayURoConfig(AppConfig):
    name = "fleio.billing.gateways.payuro"
    verbose_name = _("PayU Ro")
    fleio_module_type = 'payment_gateway'
    module_settings = {'capabilities': {
        'can_process_payments': True,
        'returns_fee_information': False,
        'supports_recurring_payments': True,
    }}
