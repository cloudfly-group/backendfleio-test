from django.conf import settings


class Conf(object):
    def __init__(self):
        self.payu_settings = getattr(settings, 'PAYURO_SETTINGS', {})
        self.merchant = self.payu_settings.get('MERCHANT_ID')
        self.url = self.payu_settings.get('URL')
        self.secret_key = self.payu_settings.get('SECRET_KEY')
        self.testorder = self.payu_settings.get('TESTORDER', 'FALSE')


conf = Conf()
