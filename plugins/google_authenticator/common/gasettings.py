from django.conf import settings


class GoogleAuthenticatorSettings:
    def __init__(self):
        self.defined_settings = getattr(settings, 'GOOGLE_AUTHENTICATOR_SETTINGS', {})
        self.issuer_name = self.defined_settings.get('issuer_name', 'Fleio')


google_authenticator_settings = GoogleAuthenticatorSettings()
