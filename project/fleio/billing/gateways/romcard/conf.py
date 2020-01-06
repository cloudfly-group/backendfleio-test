from django.conf import settings


class Conf(object):
    def __init__(self):
        self.romcard_settings = getattr(settings, 'ROMCARD_SETTINGS', {})
        self.merchant_name = self.romcard_settings.get('merchant_name')
        self.merchant_url = self.romcard_settings.get('merchant_url')
        self.merchant_no = self.romcard_settings.get('merchant_no')
        self.terminal = self.romcard_settings.get('terminal')
        self.email = self.romcard_settings.get('email')
        self.callback_url = self.romcard_settings.get('callback_url')
        self.encryption_key = self.romcard_settings.get('encryption_key')
        self.recur_days = self.romcard_settings.get('recurring_payments_frequency', 28)
        self.recur_exp = self.romcard_settings.get('recurring_payments_expiration_days', 1460)
        self.test_mode = self.romcard_settings.get('test_mode')
        if self.test_mode:
            self.url = 'https://www.activare3dsecure.ro/teste3d/cgi-bin/'
        else:
            self.url = 'https://www.secure11gw.ro/portal/cgi-bin/'


conf = Conf()
