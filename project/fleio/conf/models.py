from typing import Optional

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


class ConfigurationQueryset(models.QuerySet):
    def default(self, reseller_resources: Optional = None):
        return self.get(is_default=True, reseller_resources=reseller_resources)


@python_2_unicode_compatible
class Configuration(models.Model):
    name = models.CharField(max_length=24)
    description = models.CharField(max_length=255, default='')
    is_default = models.BooleanField(default=False)
    reseller_resources = models.ForeignKey(
        'reseller.ResellerResources',
        on_delete=models.PROTECT,
        related_name='configurations',
        default=None,
        null=True,
        blank=True,
    )

    objects = ConfigurationQueryset.as_manager()

    class Meta:
        unique_together = ['name', 'reseller_resources']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.is_default:  # NOTE(tomo): Try to prevent multiple defaults
            try:
                other_default = Configuration.objects.default(reseller_resources=self.reseller_resources)
                if self != other_default:
                    other_default.is_default = False
                    super(Configuration, other_default).save(update_fields=['is_default'])
            except Configuration.DoesNotExist:
                # NOTE: self.default is already True
                pass
            except Configuration.MultipleObjectsReturned:
                # NOTE(tomo): Something went wrong and multiple objects are default, auto fix this
                Configuration.objects.filter(is_default=True).update(is_default=False)
        else:
            try:
                other_default = Configuration.objects.default(reseller_resources=self.reseller_resources)
            except Configuration.DoesNotExist:
                # If there is no other default, mark this as default
                self.is_default = True
            except Configuration.MultipleObjectsReturned:
                # If there is another default, pass since self.default is False
                pass
            else:
                # If there is no other default, do not allow removing the default flag
                if self == other_default:
                    self.is_default = True
        super(Configuration, self).save(*args, **kwargs)


@python_2_unicode_compatible
class Option(models.Model):
    configuration = models.ForeignKey(Configuration, null=True, blank=True, on_delete=models.CASCADE)
    section = models.CharField(max_length=64)
    field = models.CharField(max_length=128)
    value = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('configuration', 'section', 'field',)

    def __str__(self):
        return "{0} - {1}".format(self.section, self.field)
