import logging
import string
from typing import Optional

from django.utils.translation import ugettext_lazy as _

# a hash table where keys represent LogClass names and values the text which Logs will format with their parameters
# this is the base table where each application can fill in logs
logclass_text = {}

LOG = logging.getLogger(__name__)

default_activities = {
    'staff': {
        'create': _('Staff user {username} ({user_id}) created {object_name} {object_id}.'),
        'update': _('Staff user {username} ({user_id}) updated {object_name} {object_id}.'),
        'destroy': _('Staff user {username} ({user_id}) deleted {object_name} {object_id}.'),
    },
    'reseller': {
        'create': _('Reseller user {username} ({user_id}) created {object_name} {object_id}.'),
        'update': _('Reseller user {username} ({user_id}) updated {object_name} {object_id}.'),
        'destroy': _('Reseller user {username} ({user_id}) deleted {object_name} {object_id}.'),
    },
    'enduser': {
        'create': _('User {username} ({user_id}) created {object_name} {object_id}.'),
        'update': _('User {username} ({user_id}) updated {object_name} {object_id}.'),
        'destroy': _('User {username} ({user_id}) deleted {object_name} {object_id}.'),
    }
}


class FormatKwargs(dict):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.has_missing_keys = False

    def __missing__(self, key):
        self.has_missing_keys = True
        return '{' + key + '}'


# TODO: move partial formatting functionality outside of activity log app to a shared location
def partial_format(input_string: str, **kwargs) -> (str, bool):
    """
    Formats a string even if not arguments are specified.
    If an argument is not specified it will be replaced with the argument name between {} - other formatting options
    will be lost.

    :param input_string: string to format
    :param kwargs: keyword arguments
    :return: tuple of formatted string and bool variable indicating if all parameters were found
    """
    format_kwargs = FormatKwargs(**kwargs)
    formatter = string.Formatter()
    formatted_string = formatter.vformat(input_string, (), format_kwargs)

    return formatted_string, not format_kwargs.has_missing_keys


def add_default_activities(user_type: str, object_name: str, object_name_plural: str):
    activities = default_activities.get(user_type, None)
    if activities:
        for (activity_name, display_text) in activities.items():
            name = get_log_class_name(
                activity_name=activity_name,
                user_type=user_type,
                object_name=object_name,
            )
            text, ok = partial_format(
                input_string=str(display_text),
                object_name=object_name,
                object_name_plural=object_name_plural,
            )

            logclass_text[name] = text
    else:
        LOG.error('Type {} not found in default action log'.format(user_type))


def add_additional_activities(
        user_type: str, object_name: str, object_name_plural: str,
        additional_activities: Optional[dict],
):
    if additional_activities:
        for (action_name, display_text) in additional_activities.items():
            name = get_log_class_name(
                activity_name=action_name,
                user_type=user_type,
                object_name=object_name,
            )
            text, ok = partial_format(
                input_string=str(display_text),
                object_name=object_name,
                object_name_plural=object_name_plural,
            )

            logclass_text[name] = text


def get_log_class_name(activity_name: str, user_type: str, object_name: str) -> str:
    return '{} {} {}'.format(user_type, activity_name, object_name)
