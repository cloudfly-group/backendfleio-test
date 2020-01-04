from django.db import models

from .server import Server


class HostingServerSettings(models.Model):
    server = models.OneToOneField(Server, related_name='hosting_server_settings', db_index=True,
                                  on_delete=models.CASCADE)
    hostname = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    api_token = models.TextField(max_length=4096, blank=True, null=True)
    secure = models.BooleanField(default=True, help_text='Use SSL for API url or not')
    port = models.PositiveSmallIntegerField(default=0, help_text='API url port')
    max_accounts = models.IntegerField(default=0, help_text='Max number of accounts to place on this server')
    quality = models.PositiveSmallIntegerField(default=0, help_text='Quality of server for different accounts')
    assigned_ips = models.TextField(max_length=4096, null=True, blank=True)
    status_url = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True, help_text='Optional location for this server')
