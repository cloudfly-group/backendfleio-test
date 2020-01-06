class GatewayException(Exception):
    """Generic gateway exception"""
    pass


class InvoicePaymentException(GatewayException):
    """Gateway exception raise when an invoice payment fails"""
    def __init__(self, message, invoice_id=None):
        self.message = message
        self.invoice_id = invoice_id
        super(InvoicePaymentException, self).__init__(message.format(invoice_id))
