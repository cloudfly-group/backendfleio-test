from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class PublicKey(models.Model):
    """Holds SSH Public Key."""
    name = models.CharField(max_length=32)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    public_key = models.TextField(max_length=17408)
    created_at = models.DateTimeField(default=timezone.now)
    fingerprint = models.CharField(max_length=128, null=True)

    class Meta:
        unique_together = ('name', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return self.name
