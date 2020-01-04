from django.dispatch import Signal

user_log_in_denied = Signal(providing_args=['user', 'request'])

user_impersonated = Signal(providing_args=['user', 'request'])

staff_logged_in = Signal(providing_args=['user', 'request'])
staff_logged_out = Signal(providing_args=['user', 'request'])

staff_log_in_failed = Signal(providing_args=['user', 'username', 'request'])
staff_log_in_non_existent = Signal(providing_args=['username', 'request'])
staff_log_in_inactive = Signal(providing_args=['user', 'request'])

staff_altered_user_data = Signal(providing_args=['user', 'request'])
staff_altered_user_password = Signal(providing_args=['user', 'request'])

staff_forgot_password = Signal(providing_args=['user', 'request'])
staff_confirmed_password = Signal(providing_args=['user', 'request'])

staff_delete_client = Signal(providing_args=['user', 'username', 'request'])
staff_delete_user = Signal(providing_args=['user', 'username', 'request'])
