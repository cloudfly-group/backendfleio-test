import logging
import random
import string
import unicodedata

from django.db.models import Count
from django.db.models import Q
from django.db.models import F

from fleio.billing.models import Service
from fleio.conf.utils import fernet_decrypt, fernet_encrypt
from fleio.servers.models import Server, ServerGroup
from fleio.servers.models.server import ServerStatus
from .whmapi import Client

LOG = logging.getLogger(__name__)
PLUGIN_LABEL = 'cpanelserver'


def get_whmclient_from_service(service: Service):
    hosting_account = service.hosting_account
    cpanel_server = hosting_account.server
    server_settings = get_server_settings(cpanel_server)
    return Client(username=server_settings['username'],
                  hostname=server_settings['hostname'],
                  access_hash=server_settings['key'])


def generate_username(domain):
    random_string = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(7))
    ascii_domain = unicodedata.normalize('NFKD', domain).encode('ascii', 'ignore').decode('ascii', 'ignore').lower()
    username = ascii_domain.replace('.', '')
    username = (username + random_string)[0:7]
    if username[0:4] == 'test':
        username = random_string[0:4] + username[4:]
    return username


def decrypt_api_key(key):
    try:
        server_key = fernet_decrypt(key) if key else None
    except Exception as e:
        LOG.exception(e)
        server_key = None
    return server_key


def encrypt_api_key(key):
    try:
        server_key = fernet_encrypt(key)
    except Exception as e:
        LOG.exception(e)
        server_key = None
    return server_key


def get_server_settings(server: Server):
    server_settings = getattr(server, 'hosting_server_settings', None)
    if not server_settings:
        return None
    server_key = decrypt_api_key(server_settings.api_token)
    return {'username': server_settings.username,
            'hostname': server_settings.hostname,
            'key': server_key}


def get_least_full_server(server_group: ServerGroup):
    servers = server_group.servers.filter(status=ServerStatus.enabled,
                                          plugin__app_label=PLUGIN_LABEL).distinct()
    # Add max accounts
    servers = servers.annotate(num_accounts=Count('hosting_accounts'),
                               max_accounts=F('hosting_server_settings__max_accounts'))
    # Filter out full servers (max accounts not reached or set to 0)
    servers = servers.filter(Q(num_accounts__lte=F('max_accounts')) | Q(max_accounts=0))
    return servers.order_by('num_accounts').first()


def get_available_server_in_order(server_group: ServerGroup):
    servers = server_group.servers.filter(status=ServerStatus.enabled,
                                          plugin__app_label=PLUGIN_LABEL).distinct()
    # Add max accounts
    servers = servers.annotate(num_accounts=Count('hosting_accounts'),
                               max_accounts=F('hosting_server_settings__max_accounts'))
    # Filter out full servers (max accounts not reached or set to 0)
    servers = servers.filter(Q(num_accounts__lte=F('max_accounts')) | Q(max_accounts=0))
    return servers.order_by('created_at').first()
