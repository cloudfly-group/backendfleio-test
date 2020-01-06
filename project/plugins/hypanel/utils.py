import requests

from fleio.servers.models import Server

from fleio.conf.utils import fernet_decrypt


def get_hypanel_server_settings(server: Server):
    decrypted_password = fernet_decrypt(server.settings['password'])
    return {
        'url': server.settings['url'],
        'username': server.settings['username'],
        'password': decrypted_password
    }


def send_hypanel_request(hypanel_server_settings: dict, method: str, params):
    return requests.post(url=hypanel_server_settings['url'], json={
        'id': 30,
        'method': method,
        'params': [hypanel_server_settings['username'], hypanel_server_settings['password'], params]
    })
