from django.db import models

from fleio.conf.utils import fernet_decrypt, fernet_encrypt
from fleio.core.models import Client


class RecurringPayments(models.Model):
    client = models.OneToOneField(
        Client, on_delete=models.CASCADE, db_index=True, related_name='+'
    )
    active = models.BooleanField(default=False)
    # custom to stripe
    stripe_customer_id = models.CharField(max_length=1024, null=True)
    stripe_payment_method = models.CharField(max_length=1024, null=True)

    objects = models.Manager

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.stripe_customer_id = fernet_encrypt(self.stripe_customer_id)
        self.stripe_payment_method = fernet_encrypt(self.stripe_payment_method)
        return super().save(force_insert=force_insert, force_update=force_update, using=using,
                            update_fields=update_fields)

    def get_secret_data(self) -> dict:
        return dict(
            stripe_customer_id=fernet_decrypt(self.stripe_customer_id),
            stripe_payment_method=fernet_decrypt(self.stripe_payment_method),
        )
