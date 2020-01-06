import bleach

from django.db import models

from fleio.core.models import AppUser
from plugins.tickets.models.department import Department


class StaffSignature(models.Model):
    content = models.CharField(max_length=10240)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.content:
            self.content = bleach.clean(self.content, strip=True)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Staff signatures'
        unique_together = ('user', 'department')

    def __str__(self):
        return '{} signature'.format(self.user)
