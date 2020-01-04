from django.db import models


class OpenstackRole(models.Model):
    id = models.CharField(max_length=64, unique=True, primary_key=True)
    name = models.CharField(max_length=255, db_index=True)

    objects = models.Manager

    class Meta:
        verbose_name_plural = 'Openstack roles'

    def __str__(self):
        return 'Openstack role: {}'.format(self.name)
