from django.db import models
from django.utils.timezone import now

from django.utils.translation import ugettext_lazy as _

from fleio.core.terms_of_service.exceptions import AgreedTOSDestroyException
from fleio.core.terms_of_service.tos_settings import TermsOfServiceSettingsConfig
from fleio.core.models import AppUser
from fleio.core.utils import RandomId


class TermsOfService(models.Model):
    id = models.BigIntegerField(unique=True, default=RandomId('core.TermsOfService'), primary_key=True)
    title = models.CharField(max_length=10240, null=False, blank=False)
    content = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(default=now)
    version = models.CharField(max_length=32, null=False, blank=False)
    draft = models.BooleanField(default=False)

    objects = models.Manager

    def __str__(self):
        if self.version:
            return '{} - {}'.format(self.title, self.version)
        return self.title

    def delete(self, using=None, keep_parents=False):
        if TermsOfService.objects.filter(draft=False).count() == 1:
            # if we delete the only one tos that is not draft left, de-activate agreement request settings
            conf = TermsOfServiceSettingsConfig(raise_if_required_not_set=False)
            if conf.require_end_users_to_agree_with_latest_tos:
                conf.forbid_access_after = ''
                conf.require_end_users_to_agree_with_latest_tos = False
                conf.save()
        if TermsOfServiceAgreement.objects.filter(terms_of_service=self, agreed=True).count() > 0:
            raise AgreedTOSDestroyException(_('You cannot delete a terms of service that a user agreed with.'))
        return super().delete(using=using, keep_parents=keep_parents)


class TermsOfServiceAgreement(models.Model):
    id = models.BigIntegerField(unique=True, default=RandomId('core.TermsOfServiceAgreement'), primary_key=True)
    terms_of_service = models.ForeignKey(TermsOfService, null=False, blank=False, on_delete=models.CASCADE)
    user = models.ForeignKey(AppUser, null=False, blank=False, on_delete=models.CASCADE)
    agreed = models.BooleanField(default=False)
    agreed_at = models.DateTimeField(blank=True, null=True, default=None)
    ip = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        unique_together = ('terms_of_service', 'user')

    def __str__(self):
        return '{} - {}'.format(self.terms_of_service.title, self.user.username)
