from django.db import models

from fleio.core.models import AppUser


class SecondFactorAuthType(models.Model):
    name = models.CharField(max_length=64, help_text='Second factor authentication type name')
    enabled_to_staff = models.BooleanField(default=False)
    enabled_to_enduser = models.BooleanField(default=False)
    display_name = models.CharField(max_length=255, blank=True)
    help_text = models.CharField(max_length=255, blank=True, null=True)

    objects = models.Manager

    def __str__(self):
        return self.name


class SecondFactorAuthMethod(models.Model):
    user = models.ForeignKey(AppUser, null=False, blank=False, on_delete=models.CASCADE)
    enabled = models.BooleanField(default=False)
    type = models.ForeignKey(SecondFactorAuthType, null=False, blank=False, on_delete=models.CASCADE)
    default = models.BooleanField(default=False)

    objects = models.Manager

    class Meta:
        unique_together = ('user', 'type')
