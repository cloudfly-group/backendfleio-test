from django.db import models


class RegistrarConnector(models.Model):
    name = models.CharField(max_length=128, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    class_name = models.CharField(max_length=64, unique=True)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name or self.class_name
