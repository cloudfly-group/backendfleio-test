from datetime import datetime
from decimal import Decimal
import logging

from fleio.billing.exceptions import ModuleNotFoundException
from fleio.billing.models import Invoice
from fleio.billing.models import InvoiceItem
from fleio.billing.models import Service
from fleio.billing.modules.factory import module_factory

from fleio.billing.utils import cdecimal

LOG = logging.getLogger(__name__)


class InvoiceUtils(object):
    @staticmethod
    def get_dynamic_price_for_service(service: Service, end_datetime: datetime) -> Decimal:
        LOG.info('Getting dynamic price for service {}'.format(service))
        try:
            billing_module = module_factory.get_module_instance(service=service)
            unsettled_usage = billing_module.get_unsettled_usage(service, end_datetime)
            return cdecimal(unsettled_usage.total_cost)
        except ModuleNotFoundException:
            return Decimal(0)

    @staticmethod
    def settle_dynamic_price_for_service(service: Service, issue_date: datetime):
        try:
            billing_module = module_factory.get_module_instance(service=service)
            billing_module.settle_usage(service, issue_date)
        except ModuleNotFoundException:
            pass

    @staticmethod
    def settle_dynamic_price_for_invoice(invoice: Invoice):
        LOG.info('Settling invoice services for invoice {}'.format(invoice.id))
        for invoice_item in invoice.items.all():  # type: InvoiceItem
            assert type(invoice_item) is InvoiceItem
            if invoice_item.service is not None:
                InvoiceUtils.settle_dynamic_price_for_service(invoice_item.service, invoice.due_date)
