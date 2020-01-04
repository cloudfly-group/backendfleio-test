# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.dispatch import Signal

staff_log_in_denied = Signal(providing_args=['user', 'request'])
user_logged_in = Signal(providing_args=['user', 'request'])
user_log_in_failed = Signal(providing_args=['user', 'username', 'request'])
user_log_in_failed_missing_license = Signal(providing_args=['user', 'username', 'request'])
user_log_in_non_existent = Signal(providing_args=['username', 'request'])
user_log_in_inactive = Signal(providing_args=['user', 'request'])
user_logged_out = Signal(providing_args=['user', 'request'])
user_forgot_password = Signal(providing_args=['user', 'request'])
user_confirmed_password = Signal(providing_args=['user', 'request'])

# these are used for both end user and staff
user_update = Signal(providing_args=['user', 'request'])
user_update_password = Signal(providing_args=['user', 'request'])

# client management signals
client_created = Signal(providing_args=[
    'client', 'create_auto_order_service', 'auto_order_service_external_billing_id', 'request_user'
])
