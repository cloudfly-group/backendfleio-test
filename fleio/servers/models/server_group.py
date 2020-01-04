from django.db import models
from django.utils.translation import ugettext_lazy as _


class GroupPlacementChoices:
    IN_ORDER = 1
    LEAST_FULL = 2

    choices = ((IN_ORDER, _('In order')),
               (LEAST_FULL, _('Least full')))


class ServerGroup(models.Model):
    name = models.CharField(max_length=32, db_index=True)
    description = models.CharField(max_length=255, default='')
    placement = models.PositiveIntegerField(choices=GroupPlacementChoices.choices,
                                            default=1,
                                            help_text='How accounts are created on servers in this group')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
