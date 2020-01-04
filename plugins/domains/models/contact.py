import pycountry
from django.db import models

from fleio.core.models import Client


class Contact(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    client = models.ForeignKey(Client, related_name='contacts', on_delete=models.CASCADE)

    first_name = models.CharField(max_length=127)
    last_name = models.CharField(max_length=127)
    company = models.CharField(max_length=127, blank=True, null=True)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=127)
    country = models.CharField(max_length=2, db_index=True, choices=[(country.alpha_2, country.name)
                                                                     for country in pycountry.countries])
    state = models.CharField(max_length=127, blank=True, null=True)
    zip_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=64)
    fax = models.CharField(max_length=64, blank=True, null=True)
    email = models.EmailField(max_length=127)
    date_created = models.DateTimeField(db_index=True, auto_now_add=True)
    vat_id = models.CharField(null=True, max_length=32, blank=True)

    @property
    def name(self):
        if not self.first_name:
            return self.company
        else:
            return self.first_name + ' ' + self.last_name

    def __str__(self):
        return self.name
