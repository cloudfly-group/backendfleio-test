import ast
import logging
import copy
import io
from email import encoders
from email.mime.base import MIMEBase

from typing import Optional

from django.conf import settings

from fleio.core.models import AppUser

LOG = logging.getLogger(__name__)


ATTACHMENT_BUILDER_METHOD = 'fleio.openstack.notification_error_parser.attachment_create'


class NotificationErrorParser:
    """Handles getting info from error notifications received from Openstack to send via email"""

    def __init__(self, payload, event_type: str):
        self.payload = payload
        self.event_type = event_type
        self.SEND_OPENSTACK_ERRORS_ON_EVENTS_SETTINGS = getattr(settings, 'SEND_OPENSTACK_ERRORS_ON_EVENTS', {})

    def get_exception_message(self):
        """returns the exception message from an openstack error notification"""
        error = None
        if not self.payload:
            return error
        if 'exception' in self.payload:
            error = self.payload.get('exception', None)
        elif 'reason' in self.payload:
            error = self.payload.get('reason', None)
        try:
            error_as_dict = ast.literal_eval(error) if error else None
        except (ValueError, Exception):
            error_as_dict = None
        if error_as_dict:
            return error_as_dict.get('message', None)
        LOG.debug('Could not get exception message from openstack notification error: {}'.format(self.event_type))
        return error

    def get_request_args(self):
        """returns arguments or payload received from openstack"""
        if not self.payload:
            return None
        if 'args' in self.payload:
            request_info = self.payload.get('args', None)
        else:
            request_info = self.payload
        full_json = self._get_custom_setting_value(setting='full_json', default=False)
        if full_json is False:
            return self._get_two_levels_deep(request_info)
        return request_info

    def get_notification_receivers(self) -> list:
        final_receivers = list()
        error_receivers_setting = self._get_custom_setting_value(setting='error_receivers', default={})
        if error_receivers_setting.get('staff_users', False):
            for user in AppUser.objects.filter(is_staff=True):
                final_receivers.append(user.email)
        for custom_receiver in error_receivers_setting.get('custom_emails', []):
            final_receivers.append(custom_receiver)
        return final_receivers

    @staticmethod
    def _get_two_levels_deep(old_dict: Optional[dict]) -> dict:
        """returns dictionary with just 2 levels"""
        new_dict = dict()
        if isinstance(old_dict, dict):
            for key, value in old_dict.items():
                new_dict[key] = copy.deepcopy(value)
                if isinstance(old_dict[key], dict):
                    for second_key, second_value in old_dict[key].items():
                        if isinstance(second_value, dict):
                            del new_dict[key][second_key]
        return new_dict

    def _get_custom_setting_value(self, setting: str, default):
        """
        determines a setting value defined by the user in the SEND_OPENSTACK_ERRORS_ON_EVENTS_SETTINGS dictionary
        from django settings file
        :param setting: the name of the dictionary attribute
        :param default: the default value returned if no setting was found for the defined events
        :return:
        """
        if self.event_type in self.SEND_OPENSTACK_ERRORS_ON_EVENTS_SETTINGS:
            if setting in self.SEND_OPENSTACK_ERRORS_ON_EVENTS_SETTINGS[self.event_type]:
                return self.SEND_OPENSTACK_ERRORS_ON_EVENTS_SETTINGS[self.event_type][setting]
        if '*' in self.SEND_OPENSTACK_ERRORS_ON_EVENTS_SETTINGS:
            if setting in self.SEND_OPENSTACK_ERRORS_ON_EVENTS_SETTINGS['*']:
                return self.SEND_OPENSTACK_ERRORS_ON_EVENTS_SETTINGS['*'][setting]
        return default


def attachment_create(formatted_args, event_type):
    # create txt file containing openstack data json about resources
    args_file = io.StringIO(formatted_args)
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(args_file.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= {}.json".format(event_type))
    args_file.close()
    return part
