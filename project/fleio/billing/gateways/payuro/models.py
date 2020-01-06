from django.db import models

from fleio.conf.utils import fernet_decrypt, fernet_encrypt
from fleio.core.models import Client


class RecurringPayments(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE, db_index=True, related_name='+')
    active = models.BooleanField(default=False)
    # custom to romcard
    token_hash = models.CharField(max_length=255, null=False, blank=False)
    ipn_cc_mask = models.CharField(max_length=255, null=False, blank=False)
    ipn_cc_exp_date = models.CharField(max_length=255, null=False, blank=False)

    objects = models.Manager

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.token_hash = fernet_encrypt(self.token_hash)
        if self.ipn_cc_mask:
            self.ipn_cc_mask = fernet_encrypt(self.ipn_cc_mask)
        if self.ipn_cc_exp_date:
            self.ipn_cc_exp_date = fernet_encrypt(self.ipn_cc_exp_date)
        return super().save(force_insert=force_insert, force_update=force_update, using=using,
                            update_fields=update_fields)

    def get_secret_data(self) -> dict:
        return dict(
            token_hash=fernet_decrypt(self.token_hash),
            ipn_cc_mask=fernet_decrypt(self.ipn_cc_mask) if self.ipn_cc_mask else None,
            ipn_cc_exp_date=fernet_decrypt(self.ipn_cc_exp_date) if self.ipn_cc_exp_date else None,
        )
