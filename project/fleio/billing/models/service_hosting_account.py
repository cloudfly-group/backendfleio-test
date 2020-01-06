from django.db import models

from fleio.billing.models import Service
from fleio.servers.models import Server


class ServiceHostingAccount(models.Model):
    """Any service account information, for web hosting services mainly"""
    service = models.OneToOneField(Service, db_index=True, on_delete=models.CASCADE,
                                   related_name='hosting_account')
    server = models.ForeignKey(Server, null=True, blank=True, db_index=True,
                               related_name='hosting_accounts', on_delete=models.SET_NULL)
    package_name = models.CharField(max_length=255, db_index=True)
    account_id = models.CharField(max_length=255, db_index=True, help_text='Domain or another way to find an account')
    username = models.CharField(max_length=32, null=True, blank=True)
    password = models.CharField(max_length=255, null=True, blank=True)
    dedicated_ip = models.GenericIPAddressField(null=True, blank=True)
