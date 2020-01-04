from django.db import models


class ProductGroup(models.Model):
    name = models.CharField(max_length=64, db_index=True, unique=True)
    description = models.CharField(max_length=2048)
    visible = models.BooleanField(default=True)

    def __str__(self):
        return self.name
