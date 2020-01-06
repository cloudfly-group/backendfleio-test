import binascii
import datetime
import hashlib
import hmac
import time
import uuid

from fleio.billing.models import Invoice


def generate_timestamp():
    return time.strftime("%Y%m%d%H%M%S", time.gmtime())


def generate_recur_timestamp(days=1460):
    return (datetime.datetime.now() + datetime.timedelta(days=days)).strftime('%Y%m%d')


def invoice_id_to_api(invoice_id):
    return str(invoice_id).rjust(6, '0')


def invoice_id_from_api(invoice_id):
    return int(invoice_id)


def generate_nonce():
    """Generate the NONCE required by Romcard"""
    binary_str = str(uuid.uuid1()).encode('utf-8')
    return hashlib.md5(binary_str).hexdigest().upper()


def get_client_by_invoice_id(invoice_id):
    invoice = Invoice.objects.filter(id=invoice_id).first()
    if invoice:
        return invoice.client
    return None


def format_sign_string(val):
    """Format the string according to Romcard requirements
    * null or empty will be replaced with '-'
    * otherwise, compose the string with it's length at the start
    """
    if (val is None) or (val == ''):
        return '-'.encode('utf-8')
    else:
        return ("%d%s" % (len(str(val)), str(val))).encode('utf-8')


def calculate_p_sign(hash_key, *args):
    """Create the signature for the given args"""
    prepared_string = ''.encode('utf-8')
    for arg in args:
        prepared_string += format_sign_string(arg)
    bin_hash_key = binascii.unhexlify(hash_key)
    result = hmac.new(bin_hash_key,
                      msg=prepared_string,
                      digestmod=hashlib.sha1).hexdigest()
    return result.upper()


rc_codes = {
    # Credit card processing error codes from ISO8583
    # Taken from https://www.activare3dsecure.ro/teste3d/error.txt
    '00': 'AUTHORIZED',
    '01': 'REFER TO CARD ISSUER',
    '02': 'REFERRAL-SPECIAL CONDITIONS',
    '03': 'INVALID MERCHANT',
    '04': 'PICK UP CARD',
    '05': 'DO NOT HONOR',
    '06': 'ERROR - RETRY',
    '07': 'PICK UP !! FRAUD !!',
    '08': 'HONOR WITH C/H IDENT',
    '09': 'REQUEST IN PROGRESS',
    '10': 'PARTIALLY APPROVED',
    '11': 'VIP APPROVAL',
    '12': 'INVALID TRANSACTION',
    '13': 'INVALID AMOUNT',
    '14': 'INVALID ACCOUNT NBR',
    '15': 'NO SUCH ISSUER        UNABLE TO ROUTE AT IEM',
    '16': 'APPROVED, UPD TRK 3',
    '19': 'RE-ENTER REQUEST',
    '21': 'NO ACTION TAKEN',
    '22': 'SUSPECT MALFUNCTION',
    '30': 'FORMAT ERROR',
    '31': 'ISSUER SIGNED-OFF',
    '32': 'PARTIALLY COMPLETTED',
    '33': 'EXPIRED CARD',
    '36': 'PICK UP-RESTRICTED',
    '37': 'PICK UP-CALL ACQBANK',
    '38': 'PICK UP-EXC PIN RETRY',
    '39': 'NO CREDIT ACCOUNT',
    '41': 'PICK UP- LOST CARD',
    '43': 'PICK UP- STOLEN CARD',
    '51': 'INSUFFICIENT FUNDS',
    '52': 'NO CHECKING ACCOUNT',
    '53': 'NO SAVINGS ACCOUNT',
    '54': 'EXPIRED CARD',
    '55': 'INCORRECT PIN',
    '57': 'NOT PERMITTED TO C/H',
    '58': 'NOT PERMITTED TO POS',
    '61': 'EXCEEDS AMOUNT LIMIT',
    '62': 'RESTRICTED CARD',
    '63': 'SECURITY VIOLATION',
    '64': 'ORIG.AMT INCORRECT',
    '65': 'ACTIV.COUNT EXCEEDED',
    '75': 'PIN RETRIES EXCEEDED',
    '76': 'DIFFERENT FROM ORIG.  WRONG PIN',
    '79': 'ALREADY REVERSED',
    '80': 'INVALID DATE          NETWORK ERROR',
    '81': 'CRYPTOGTAPHIC ERROR   FOREIGN NETWORK ERR',
    '82': 'INCORRECT CVV         TIMED-OUT AT IEM',
    '83': 'UNABLE TO VERIFY PIN  TRANSACTION FAILED',
    '84': 'PRE-AUTH. TIMED OUT',
    '85': 'ACCOUNT VERIFICATION',
    '86': 'UNABLE TO VERIFY PIN',
    '88': 'CRYPTOGTAPHIC ERROR',
    '91': 'ISSUER UNAVAILABLE',
    '92': 'ROUTER UNAVAILABLE',
    '93': 'CANNOT COMPLETE TXN',
    '94': 'DUPLICATE TXN',
    '95': 'RECONCILE ERROR',
    '96': 'SYSTEM MALFUNCTION',
    '99': 'ABORTED',
    '-6': 'BAD CGI REQUEST (CAMPUL ORDER INCORECT)',
    '-17': 'ACCESS DENIED',
    '-19': 'AUTHENTICATION FAILED',
    '-20': 'SYSTEM ERROR (TIMESTAMP INCORECT)'
}


class RomcardAction(object):
    """
    ACTION value values:
            0 - transaction approved
            1 - duplicate transaction
            2 - transaction rejected
            3 - processing error
    """
    APPROVED = 0
    DUPLICATE_TRANSACTION = 1
    REJECTED = 2
    PROCESSING_ERROR = 3

    LIST_ACTIONS = [0, 1, 2, 3]


class TransactionType(object):
    """
    TRTYPE valid values:
            0 - pre-authorization (just blocking money on credit card)
            21 - sales completion (actually charging money)
            24 - reversal (refunding money on credit card)
            25 - partial refund
            171 - create automatic recurring transaction
    """
    PRE_AUTHORIZATION = 0
    SALES_COMPLETION = 21
    REFUND = 24
    PARTIAL_REFUND = 25
    CANCELLED_FRAUD = 26
    CREATE_RECURRING_TRANSACTION = 171

    LIST_TYPES = [0, 21, 24, 25, 26, 171]
