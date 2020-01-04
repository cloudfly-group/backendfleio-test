from django.conf import settings


class Conf(object):
    def __init__(self):
        self.stripe_settings = getattr(settings, 'STRIPE_SETTINGS', {})
        self.public_key = self.stripe_settings.get('public_key')
        self.secret_key = self.stripe_settings.get('secret_key')
        self.signing_secret = self.stripe_settings.get('signing_secret')
        self.name = self.stripe_settings.get('name')
        self.image_url = self.stripe_settings.get('image_url')
        self.locale = self.stripe_settings.get('locale')
        self.zipcode = self.stripe_settings.get('zipcode')
        self.callback_url = self.stripe_settings.get('callback_url')
        self.test_mode = self.stripe_settings.get('test_mode')


conf = Conf()
