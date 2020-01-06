from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from fleio.activitylog.formatting import logclass_text
from fleio.activitylog.operations import add_request_log, fetch_log_category
from fleiostaff.core.signals import staff_delete_user
from .signals import (staff_log_in_denied, user_confirmed_password, user_forgot_password, user_log_in_failed,
                      user_log_in_failed_missing_license, user_log_in_inactive, user_log_in_non_existent,
                      user_logged_in, user_logged_out, user_update, user_update_password)


core_log_text = {
    'user_log_in_denied': _('User {username} ({user_id}) tried to log in via the staff panel. '
                            'End users cannot log in to the staff panel'),
    'staff_logged_in': _('Staff user {username} ({user_id}) logged in'),
    'staff_logged_out': _('Staff user {username} ({user_id}) logged out'),
    'staff_log_in_failed': _('Staff user {username} ({user_id}) failed to log in. Invalid password'),
    'staff_log_in_non_existent': _('User {username} failed to log in. User does not exist'),
    'staff_log_in_inactive': _('Staff user {username} ({user_id}) failed to log in. Inactive user'),
    'staff_forgot_password': _('Staff user {username} ({user_id}) submitted a password reset through '
                               'the password reset form'),
    'staff_confirmed_password': _('Staff user {username} ({user_id}) succeeded in obtaining a new password'
                                  ' through the password reset form'),
    'staff_altered_user_data': _('Staff user {username} ({user_id}) updated the following profile '
                                 'attributes for username: {username_changed} ({user_changed_id}) - {updated_data}'),
    'staff_altered_user_password': _('Staff user {username} ({user_id}) successfully changed password for '
                                     '{username_changed} ({user_changed_id})'),
    # staff signals messages above this comment, end user signals messages below
    'staff_log_in_denied': _('Staff user {username} ({user_id}) tried to log in via the end user panel. '
                             'Staff users cannot log in to the end user panel'),
    'user_log_in_non_existent': _('User {username} failed to log in. User does not exist'),
    'user_log_in_failed': _('User {username} ({user_id}) failed to log in. Invalid password'),
    'user_log_in_inactive': _('User {username} ({user_id}) failed to log in. Inactive user'),
    'user_logged_in': _('User {username} ({user_id}) logged in'),
    'user_logged_out': _('User {username} ({user_id}) logged out'),
    'user_forgot_password': _('User {username} ({user_id}) submitted a password reset through '
                              'the password reset form'),
    'user_confirmed_password': _('User {username} ({user_id}) succeeded in obtaining a new password '
                                 'through the password reset form'),
    'user_log_in_failed_missing_license': _('User {username} ({user_id}) failed to login because of missing license'),
    'user_impersonated': _('User {username} ({user_id}) impersonated user {impersonated_user_name} '
                           '({impersonated_user_id})'),
    # common signals for both staff and end users below
    'user_update': _('Account profile modified - {updated_data}'),
    'user_update_password': _('Account password successfully changed'),
    'staff_delete_client': _('User {username} ({user_id}) deleted a client {client_name} ({client_id})'),
    'staff_delete_user': _('User {username} ({user_id}) deleted a user {deleted_user_name} ({deleted_user_id})'),
}

logclass_text.update(core_log_text)


@receiver(user_logged_out, dispatch_uid='log_user_logged_out')
def log_user_logged_out(sender, **kwargs):
    add_request_log(fetch_log_category('core'), 'user_logged_out', 'info', **kwargs)


@receiver(user_log_in_failed, dispatch_uid='log_user_login_failed')
def log_user_login_failed(sender, **kwargs):
    add_request_log(fetch_log_category('core'), 'user_log_in_failed', 'error', **kwargs)


@receiver(user_log_in_non_existent, dispatch_uid='log_user_log_in_non_existent')
def log_user_log_in_non_existent(sender, **kwargs):
    add_request_log(fetch_log_category('core'), 'user_log_in_non_existent', 'error', **kwargs)


@receiver(user_log_in_failed_missing_license, dispatch_uid='log_user_login_failed_missing_license')
def log_user_login_failed_missing_license(sender, **kwargs):
    add_request_log(fetch_log_category('core'), 'user_log_in_failed_missing_license', 'error', **kwargs)


@receiver(staff_log_in_denied, dispatch_uid='log_staff_log_in_denied')
def log_staff_log_in_denied(sender, **kwargs):
    add_request_log(fetch_log_category('core'), 'staff_log_in_denied', 'error', **kwargs)


@receiver(user_log_in_inactive, dispatch_uid='log_user_log_in_inactive')
def log_user_log_in_inactive(sender, **kwargs):
    add_request_log(fetch_log_category('core'), 'user_log_in_inactive', 'error', **kwargs)


@receiver(user_logged_in, dispatch_uid='log_user_logged_in')
def log_user_logged_in(sender, **kwargs):
    add_request_log(fetch_log_category('core'), 'user_logged_in', 'info', **kwargs)


@receiver(user_update, dispatch_uid='log_user_update')
def log_user_update(sender, **kwargs):
    add_request_log(fetch_log_category('core'), 'user_update', 'info', **kwargs)


@receiver(user_update_password, dispatch_uid='log_user_update_password')
def log_user_update_password(sender, **kwargs):
    add_request_log(fetch_log_category('core'), 'user_update_password', 'info', **kwargs)


@receiver(user_confirmed_password, dispatch_uid='log_user_confirmed_password')
def log_user_confirmed_password(sender, **kwargs):
    add_request_log(fetch_log_category('core'), 'user_confirmed_password', 'info', **kwargs)


@receiver(user_forgot_password, dispatch_uid='log_user_forgot_password')
def log_user_forgot_password(sender, **kwargs):
    add_request_log(fetch_log_category('core'), 'user_forgot_password', 'info', **kwargs)


@receiver(staff_delete_user, dispatch_uid='log_staff_delete_user')
def log_staff_delete_user(sender, **kwargs):
    add_request_log(fetch_log_category('core'), 'staff_delete_user', 'info', **kwargs)
