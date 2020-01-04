import logging
from django.utils.module_loading import import_string
from django.conf import settings

LOG = logging.getLogger(__name__)


class FraudResultStatus:
    """Generic fraud result status for all fraud modules"""
    ACCEPT = 'accept'
    MANUAL_REVIEW = 'review'
    REJECT = 'reject'

    choices = [(ACCEPT, 'Accept'),
               (MANUAL_REVIEW, 'Manual review'),
               (REJECT, 'Reject')]


class FraudResult:
    def __init__(self, status, message, explanations):
        self.status = status
        self.message = message
        self.explanations = explanations


class FleioFraudCheck:
    FRAUD_RESULT_STATUS = FraudResultStatus

    def __init__(self):
        self._fraud_module = getattr(settings, 'ANTI_FARUD_MODULE', 'fleio.core.antifraud.maxmind.FleioMaxMind')
        self._module = None

    def _load_module(self):
        if self._module is None and self._fraud_module:
            try:
                module_class = import_string(self._fraud_module)
                self._module = module_class()
            except ImportError as e:
                if self._fraud_module:
                    LOG.exception(e)

    def check_order(self, order):
        self._load_module()
        if self._module:
            return self._module.check_order(order)
        else:
            return FraudResultStatus.ACCEPT
