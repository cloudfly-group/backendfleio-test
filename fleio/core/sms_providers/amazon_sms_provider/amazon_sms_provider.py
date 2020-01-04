import boto3
import phonenumbers

from botocore.exceptions import BaseEndpointResolverError

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from fleio.core.sms_providers.sms_base_provider import SmsBaseProvider

from fleio.celery import app
from fleio.core.exceptions import APIBadRequest


class AmazonSmsProvider(SmsBaseProvider):
    settings_dict_name = 'AMAZON_SMS_PROVIDER_SETTINGS'

    def __init__(self, provider_name=settings_dict_name):
        super().__init__(provider_name=provider_name)
        self.client = self._get_client()

    def _get_client(self) -> boto3.client:
        if not self.client:
            try:
                self.client = boto3.client(
                    service_name='sns',
                    aws_access_key_id=self.settings.get('aws_access_key_id'),
                    aws_secret_access_key=self.settings.get('aws_secret_access_key'),
                    region_name=self.settings.get('region_name'),
                    verify=self.settings.get('verify'),
                )
            except BaseEndpointResolverError as e:
                raise APIBadRequest(_('Incorrect Amazon SNS settings: {}').format(str(e)))
            except Exception as e:
                raise APIBadRequest(str(e))
        return self.client

    @staticmethod
    def _get_phone_number_format():
        return phonenumbers.PhoneNumberFormat.E164

    def send_sms(self, phone_number: str, message: str, subject: str = None, *args, **kwargs):
        if not self._check_phone_number_is_valid(phone_number=phone_number):
            raise APIBadRequest(_('Phone number is invalid.'))
        parsed_phone = self._get_parsed_phone(phone_number=phone_number)
        formatted_phone_number = phonenumbers.format_number(
            numobj=parsed_phone, num_format=self._get_phone_number_format()
        )
        send_sms_as_task.delay(
            aws_access_key_id=self.settings.get('aws_access_key_id', ''),
            aws_secret_access_key=self.settings.get('aws_secret_access_key', ''),
            region_name=self.settings.get('region_name', ''),
            verify=self.settings.get('verify', True),
            phone_number=formatted_phone_number,
            message=message if message else '',
            subject=subject if subject else '',
        )

    def get_sms_attributes(self):
        return self.client.get_sms_attributes()


@app.task(bind=True, max_retries=settings.TASK_RETRIES, autoretry_for=(Exception, ),
          name='Send sms', resource_type='Notification')
def send_sms_as_task(self, aws_access_key_id, aws_secret_access_key, region_name, verify, phone_number, message,
                     subject):
    client_params = {
        'service_name': 'sns',
        'aws_access_key_id': aws_access_key_id,
        'aws_secret_access_key': aws_secret_access_key,
        'region_name': region_name,
    }
    if verify:
        client_params['verify'] = verify
    content_params = {
        'PhoneNumber': phone_number,
        'Message': message,
    }
    if subject:
        content_params['Subject'] = subject
    try:
        boto3.client(**client_params).publish(**content_params)
    except Exception as e:
        raise e


def get_sms_provider_class() -> AmazonSmsProvider:
    return AmazonSmsProvider()
