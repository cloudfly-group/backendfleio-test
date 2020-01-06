import hashlib
import logging
import re
import sys
import traceback
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional

from django.utils.translation import ugettext_lazy as _

LOG = logging.getLogger(__name__)


class OSAuthCache(object):
    """Allows caching of auth_ref obtained on successful authentication."""

    def __init__(self, request_session, main_key='openstack'):
        """
        :param request_session: the request session object
        :type request_session: rest_framework.request.request.session
        """
        request_session.setdefault(main_key, {})
        self.main_key = main_key
        self.cache = request_session[self.main_key]
        self.request_session = request_session

    def get(self, item, default):
        try:
            return self.__getitem__(item)
        except KeyError:
            return default

    def __getitem__(self, item):
        return self.cache.get(item)

    def __setitem__(self, key, value):
        self.cache[key] = value
        if hasattr(self.request_session, 'modified'):
            self.request_session.modified = True


def newlines_substract(data):
    return re.compile(r"\r|\n").sub("", data)


def md5_hash(text):
    return hashlib.md5(b'{0}'.format(text)).hexdigest()


def valid_uuid(uuid):
    regex = re.compile(r'^[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}\Z', re.I)
    match = regex.match(uuid)
    return bool(match)


def import_class(str_import):
    """Import a class from a string"""
    str_mod, sep, str_class = str_import.rpartition('.')
    __import__(str_mod)
    try:
        return getattr(sys.modules[str_mod], str_class)
    except AttributeError:
        raise ImportError('Class %s cannot be found (%s)' %
                          (str_class,
                           traceback.format_exception(*sys.exc_info())))


USERDATA_FORMATS = {
    '#!': 'text/x-shellscript',
    '#include': 'text/x-include-url',
    '#cloud-config': 'text/cloud-config',
    '#upstart-job': 'text/upstart-job',
    '#cloud-boothook': 'text/cloud-boothook',
    '#part-handler': 'text/part-handler',
}


def get_userdata_content_type(user_data) -> Optional[str]:
    for key, value in USERDATA_FORMATS.items():
        if user_data.startswith(key):
            return value
    raise Exception(_('Invalid user data.'))


def parse_user_data_mime(user_data_passwd_template: Optional[str], user_supplied_user_data: Optional[str],
                         ssh_keys_set_template: Optional[str], keys_content: Optional[dict], additional_userdata=None,
                         ) -> Optional[MIMEMultipart]:
    compose_user_data = MIMEMultipart()
    if user_data_passwd_template:
        password_set_txt = MIMEText(_text=user_data_passwd_template)
        password_set_txt.add_header('Content-Type:', 'text/cloud-config')
        compose_user_data.attach(password_set_txt)
    if keys_content:
        for key, value in keys_content.items():
            ssh_keys_set_template += '    - {}\n'.format(value)
        keys_set_txt = MIMEText(_text=ssh_keys_set_template)
        keys_set_txt.add_header('Content-Type:', 'text/cloud-config')
        compose_user_data.attach(keys_set_txt)
    if user_supplied_user_data:
        userdata_txt = MIMEText(_text=user_supplied_user_data)
        userdata_txt.add_header('Content-Type:', get_userdata_content_type(user_data=user_supplied_user_data))
        compose_user_data.attach(userdata_txt)
    if additional_userdata:
        additional_userdata_txt = MIMEText(_text=additional_userdata)
        additional_userdata_txt.add_header(
            'Content-Type:', get_userdata_content_type(user_data=additional_userdata)
        )
        compose_user_data.attach(additional_userdata_txt)
    if (not user_data_passwd_template and not keys_content and not user_supplied_user_data and
            not additional_userdata):
        return None
    return compose_user_data.as_string()
