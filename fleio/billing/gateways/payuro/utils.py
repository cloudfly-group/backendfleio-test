import hmac
import hashlib
import urllib.parse

from django.utils.timezone import now as utcnow

from .conf import conf


class PayURoUtils:
    @staticmethod
    def calculate_signature(params):
        string = ''
        for param in params:
            if isinstance(param, list):
                for sub_param in param:
                    string = '{}{}{}'.format(string, len(sub_param), sub_param)
            else:
                string = '{}{}{}'.format(string, len(param), param)
        return hmac.new(conf.secret_key, string.encode('utf-8'), hashlib.md5).hexdigest().encode('utf-8')

    @staticmethod
    def verify_hash(params):
        params = params.decode('utf-8')
        params = urllib.parse.unquote_plus(params)
        params = params.split('&')
        received_hash = ''
        string = ''
        for param in params:
            to_append = param.split('=')
            key = to_append[0]
            value = to_append[1] if to_append[1] else None
            if key != 'HASH':
                if value == '' or value is None:
                    string = '{}{}'.format(string, '0')
                else:
                    string = '{}{}{}'.format(string, len(value), value)
            else:
                received_hash = value

        hash_from_params = hmac.new(conf.secret_key, string.encode('utf-8'), hashlib.md5).hexdigest().encode('utf-8')
        if received_hash == str(hash_from_params, encoding='utf-8'):
            return True
        return False

    @staticmethod
    def build_ipn_response(params):
        now = utcnow().strftime('%Y%m%d%H%M%S')
        params = params.decode('utf-8')
        params = urllib.parse.unquote_plus(params)
        params = params.split('&')
        hash_string = ''
        hash_fields = ['IPN_PID[]', 'IPN_PNAME[]', 'IPN_DATE']
        already_collected_hash_fields = {}
        for param in params:
            to_append = param.split('=')
            key = to_append[0]
            value = to_append[1] if to_append[1] else None
            if key in hash_fields and already_collected_hash_fields.get(key, None) is None:
                hash_string = '{}{}{}'.format(
                    hash_string,
                    len(value),
                    value,
                )
                already_collected_hash_fields[key] = True
        hash_string = '{}{}{}'.format(hash_string, len(now), now)
        response_hash = hmac.new(conf.secret_key, hash_string.encode('utf-8'), hashlib.md5).hexdigest().encode('utf-8')
        return '<EPAYMENT>{}|{}</EPAYMENT>'.format(now, str(response_hash, encoding='utf-8'))
