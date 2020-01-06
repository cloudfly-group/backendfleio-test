# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.dispatch import receiver

from fleio.activitylog.operations import add_request_log, fetch_log_category
from .signals import (staff_altered_user_data, staff_altered_user_password, staff_confirmed_password,
                      staff_forgot_password, staff_log_in_failed, staff_log_in_inactive, staff_log_in_non_existent,
                      staff_logged_in, staff_logged_out, user_impersonated, user_log_in_denied)


@receiver(staff_logged_out, dispatch_uid='log_staff_logged_out')
def log_staff_logged_out(sender, **kwargs):
    add_request_log(fetch_log_category('core'), 'staff_logged_out', 'info', **kwargs)


@receiver(staff_logged_in, dispatch_uid='log_staff_logged_in')
def log_staff_logged_in(sender, **kwargs):
    add_request_log(fetch_log_category('core'), 'staff_logged_in', 'info', **kwargs)


@receiver(staff_log_in_failed, dispatch_uid='log_staff_log_in_failed')
def log_staff_log_in_failed(sender, **kwargs):
    add_request_log(fetch_log_category('core'), 'staff_log_in_failed', 'error', **kwargs)


@receiver(staff_log_in_non_existent, dispatch_uid='log_staff_log_in_non_existent')
def log_staff_log_in_non_existent(sender, **kwargs):
    add_request_log(fetch_log_category('core'), 'staff_log_in_non_existent', 'error', **kwargs)


@receiver(user_log_in_denied, dispatch_uid='log_user_login_denied')
def log_user_login_denied(sender, **kwargs):
    add_request_log(fetch_log_category('core'), 'user_log_in_denied', 'error', **kwargs)


@receiver(staff_log_in_inactive, dispatch_uid='log_staff_login_inactive')
def log_staff_login_inactive(sender, **kwargs):
    add_request_log(fetch_log_category('core'), 'staff_log_in_inactive', 'error', **kwargs)


@receiver(staff_confirmed_password, dispatch_uid='log_staff_confirmed_password')
def log_staff_confirmed_password(sender, **kwargs):
    add_request_log(fetch_log_category('core'), 'staff_confirmed_password', 'info', **kwargs)


@receiver(staff_forgot_password, dispatch_uid='log_staff_forgot_password')
def log_staff_forgot_password(sender, **kwargs):
    add_request_log(fetch_log_category('core'), 'staff_forgot_password', 'info', **kwargs)


@receiver(staff_altered_user_data, dispatch_uid='log_staff_altered_user_data')
def log_staff_altered_user_data(sender, **kwargs):
    add_request_log(fetch_log_category('core'), 'staff_altered_user_data', 'info', **kwargs)


@receiver(staff_altered_user_password, dispatch_uid='log_staff_altered_user_password')
def log_staff_altered_user_password(sender, **kwargs):
    add_request_log(fetch_log_category('core'), 'staff_altered_user_password', 'info', **kwargs)


@receiver(user_impersonated, dispatch_uid='log_user_impersonated')
def log_user_impersonated(sender, **kwargs):
    add_request_log(fetch_log_category('core'), 'user_impersonated', 'info', **kwargs)
