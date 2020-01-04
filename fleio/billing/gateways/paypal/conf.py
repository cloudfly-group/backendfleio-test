from django.conf import settings


class Conf(object):
    def __init__(self):
        self.paypal_settings = getattr(settings, 'PAYPAL_SETTINGS', {})
        self.mode = self.paypal_settings.get('mode')
        self.client_id = self.paypal_settings.get('client_id')
        self.client_secret = self.paypal_settings.get('client_secret')
        self.url_base = self.paypal_settings.get('url_base')


conf = Conf()
