import hashlib

from django.conf import settings
from django.utils.crypto import constant_time_compare, salted_hmac
from django.utils.http import base36_to_int, int_to_base36

from fleio.core.models import AppUser

from datetime import date


class SignUpTokenGenerator:
    secret = settings.SECRET_KEY
    key_salt = settings.SSO_SALT

    def make_token(self, user: AppUser):
        """
        Return a token that can be used once to do an email validation
        """
        return self._make_token_with_timestamp(user, self._get_timestamp())

    def check_token(self, user: AppUser, token):
        """
        Check that an email validation reset token is correct for a given user.
        """
        if not (user and token):
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
        if not constant_time_compare(self._make_token_with_timestamp(user, ts), token):
            return False

        # Check the timestamp is within limit
        if (self._get_timestamp() - ts) > settings.EMAIL_VERIFICATION_TIMEOUT_DAYS:
            return False

        return True

    def _make_token_with_timestamp(self, user, timestamp):
        ts_b36 = int_to_base36(timestamp)
        hash_value = salted_hmac(
            self.key_salt,
            self._make_hash_value(user, timestamp),
            secret=self.secret,
        ).hexdigest()[::2]  # Limit to 20 characters to shorten the URL.
        return '{}-{}'.format(ts_b36, hash_value)

    @staticmethod
    def _make_hash_value(user, timestamp):
        """
        Hash the user's primary key and email_verified field value as this will change
        after an email verification thus we produce a token that's invalidated when it's used
        """
        to_hash = (str(user.pk) + str(user.email_verified) + str(timestamp)).encode('utf-8')
        return hashlib.md5(to_hash).hexdigest()

    @staticmethod
    def _get_timestamp():
        # timestamp is number of days since 2001-1-1.  Converted to
        # base 36, this gives us a 3 digit string until about 2121
        return (date.today() - date(2001, 1, 1)).days


signup_token_generator = SignUpTokenGenerator()
