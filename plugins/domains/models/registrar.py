from django.db import models

from .registrar_connector import RegistrarConnector


class Registrar(models.Model):
    name = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    connector = models.ForeignKey(RegistrarConnector, on_delete=models.PROTECT, related_name='registrars')

    class Meta:
        ordering = ('created_at', )

    def __str__(self):
        return self.name
