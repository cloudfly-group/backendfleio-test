import hashlib

from django.conf import settings
from django.utils.crypto import constant_time_compare, salted_hmac
from django.utils.http import base36_to_int, int_to_base36

from datetime import date


class RememberSfa:
    secret = settings.SECRET_KEY
    key_salt = settings.SSO_SALT

    def __init__(self, user):
        self.user = user

    def make_token(self):
        return self._make_token_with_timestamp(self.user, self._get_timestamp())

    def _make_token_with_timestamp(self, user, timestamp):
        ts_b36 = int_to_base36(timestamp)
        hash_value = salted_hmac(
            self.key_salt,
            self._make_hash_value(user, timestamp),
            secret=self.secret,
        ).hexdigest()
        return '{}-{}'.format(ts_b36, hash_value)

    def check_token(self, token):
        if not (self.user and token):
            return False
        # Parse the token
        try:
            ts_b36, hash_value = token.split("-")
        except ValueError:
            return False

        try:
            ts = base36_to_int(ts_b36)
        except ValueError:
            return False

        # Check that the timestamp/uid has not been tampered with
        if not constant_time_compare(self._make_token_with_timestamp(self.user, ts), token):
            return False

        # Check the timestamp is within 60 days limit
        if (self._get_timestamp() - ts) > getattr(settings, 'REMEMBER_SECOND_FACTOR_AUTH_DAYS', 60):
            return False

        return True

    @staticmethod
    def _make_hash_value(user, timestamp):
        # use user pk for hash as users don't know it
        # use number of days since 2001-1-1 to the date of token generation, other users won't know it either
        #   because they most likely don't know when the token was first generated
        to_hash = (str(user.pk) + str(timestamp)).encode('utf-8')
        return hashlib.sha512(to_hash).hexdigest()

    @staticmethod
    def _get_timestamp():
        # timestamp is number of days since 2001-1-1.  Converted to
        # base 36, this gives us a 3 digit string until about 2121
        return (date.today() - date(2001, 1, 1)).days
