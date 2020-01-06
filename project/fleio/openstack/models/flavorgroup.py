from django.db import models


class FlavorGroup(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=256, null=False, blank=False)
    description = models.CharField(max_length=4096, null=True, blank=True)
    is_default = models.BooleanField(default=False)
    priority = models.IntegerField(default=0)

    reseller_resources = models.ForeignKey(
        'reseller.ResellerResources',
        on_delete=models.PROTECT,
        related_name='flavor_groups',
        default=None,
        null=True,
        blank=True,
    )

    def __str__(self):
        return '{} - {}'.format(self.name, self.description)

    def save(self, *args, **kwargs):
        if self.is_default:
            FlavorGroup.objects.filter(is_default=True).update(is_default=False)
        return super().save(*args, **kwargs)
