from __future__ import unicode_literals

from rest_framework import exceptions as rest_exceptions
from rest_framework import status


class BillingException(rest_exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST


class PaymentException(BillingException):
    pass


class InvoiceException(BillingException):
    pass


class ServiceException(BillingException):
    """Base service module exception"""
    pass


class OrderException(BillingException):
    pass


class CartException(BillingException):
    def __init__(self, detail):
        self.detail = detail

    def __str__(self):
        return self.detail


class CartItemException(CartException):
    pass


class ModuleNotFoundException(BillingException):
    pass
