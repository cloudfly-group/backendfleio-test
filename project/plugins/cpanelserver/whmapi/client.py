import requests
from requests.auth import AuthBase

from .exceptions import WHMCredentialsRequired
from .exceptions import WHMCredentialsInvalid
from .exceptions import WHMAPIException


class HashAuth(AuthBase):
    def __init__(self, username, access_hash):
        self.access_hash = access_hash.replace('\n', '')
        self.username = username

    def __call__(self, r):
        r.headers['Authorization'] = 'WHM %s:%s' % (self.username, self.access_hash)
        return r


class Client:

    def __init__(self,
                 username,
                 hostname,
                 password=None,
                 access_hash=None,
                 ssl=True):

        self.username = username
        self.host = hostname
        self.port = 2087 if ssl else 2086
        self.protocol = 'https' if ssl else 'http'

        # check required parameters
        if not access_hash and not password:
            raise WHMCredentialsRequired()
        elif password and access_hash:
            raise WHMCredentialsInvalid()

        if access_hash:
            self.auth = HashAuth(username, access_hash)
        elif password:
            self.auth = (username, password)

    def request(self, command, **kwargs):
        """WHM API request"""
        kwargs['api.version'] = 1
        url = self._url(command)
        response = requests.get(url, params=kwargs, auth=self.auth).json()
        if response.get('status') == 1:
            raise WHMAPIException(response.get('statusmsg', 'An unknown error occured'))
        metadata = response.get('metadata', {})
        if metadata.get('result') == 0:
            raise WHMAPIException(metadata.get('reason', 'An unknown error occured'))
        return response

    def _url(self, f_name):
        return '{}://{}:{:d}/json-api/{}'.format(self.protocol, self.host, self.port, f_name)
