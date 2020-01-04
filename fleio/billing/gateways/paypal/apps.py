from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class PaypalConfig(AppConfig):
    name = "fleio.billing.gateways.paypal"
    verbose_name = _("Paypal")
    fleio_module_type = 'payment_gateway'
    module_settings = {'capabilities': {
        'can_process_payments': True,
        'returns_fee_information': True
    }}
