import phonenumbers

from django.conf import settings


class SmsBaseProvider:
    def __init__(self, provider_name: str):
        self.settings = getattr(settings, provider_name, {})
        self.client = None

    @staticmethod
    def _get_parsed_phone(phone_number):
        try:
            return phonenumbers.parse(phone_number)
        except Exception as e:
            raise e

    def _check_phone_number_is_valid(self, phone_number: str):
        try:
            return phonenumbers.is_valid_number(self._get_parsed_phone(phone_number=phone_number))
        except Exception as e:
            del e  # unused
            return False

    def _get_client(self):
        raise NotImplementedError()

    @staticmethod
    def _get_phone_number_format():
        """The format required by the provider, e.g. phonenumbers.PhoneNumberFormat.E164"""
        raise NotImplementedError()

    def send_sms(self, phone_number: str, message: str, subject: str = None, *args, **kwargs):
        raise NotImplementedError()
