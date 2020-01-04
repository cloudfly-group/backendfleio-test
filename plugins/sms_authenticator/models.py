from django.db import models

from fleio.conf.utils import fernet_decrypt, fernet_encrypt
from fleio.core.models.second_factor_auth import SecondFactorAuthMethod


class SMSAuthenticatorData(models.Model):
    method = models.OneToOneField(SecondFactorAuthMethod, null=False, blank=False, on_delete=models.CASCADE)
    # authentication type custom fields
    secret_key = models.CharField(max_length=1024, null=False, blank=False)
    counter = models.IntegerField(default=0)

    objects = models.Manager

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.secret_key = fernet_encrypt(self.secret_key)
        return super().save(force_insert=force_insert, force_update=force_update, using=using,
                            update_fields=update_fields)

    def get_secret_key(self):
        return fernet_decrypt(self.secret_key)
