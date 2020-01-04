from django.conf import settings


class SMSAuthenticatorSettings:
    def __init__(self):
        self.defined_settings = getattr(settings, 'SMS_AUTHENTICATOR_SETTINGS', {})
        self.provider = self.defined_settings.get('provider', 'AmazonSmsProvider')
        self.message = self.defined_settings.get('message', 'Hello, your Fleio verification code is {}')
        self.subject = self.defined_settings.get('subject', None)


sms_authenticator_settings = SMSAuthenticatorSettings()
