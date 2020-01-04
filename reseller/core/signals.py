from django.dispatch import Signal

reseller_logged_in = Signal(providing_args=['user', 'request'])
reseller_logged_out = Signal(providing_args=['user', 'request'])

reseller_altered_user_data = Signal(providing_args=['user', 'request'])
reseller_altered_user_password = Signal(providing_args=['user', 'request'])

reseller_forgot_password = Signal(providing_args=['user', 'request'])
reseller_confirmed_password = Signal(providing_args=['user', 'request'])

reseller_delete_client = Signal(providing_args=['user', 'username', 'request'])
reseller_delete_user = Signal(providing_args=['user', 'username', 'request'])
