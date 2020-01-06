import json
import logging
import sys
from multiprocessing import Process, Queue
from os import environ
from os.path import abspath, dirname

import django
import requests

current_path = dirname(abspath(__file__))
fleio_path = dirname(dirname(current_path))
sys.path.append(fleio_path)

environ.setdefault("DJANGO_SETTINGS_MODULE", "fleio.settings")
django.setup()

from fleiostaff.core.views import _set_license
from fleio.conf.models import Option
from fleio.conf.utils import fernet_decrypt, fernet_encrypt
from queue import Empty

LOG = logging.getLogger(__name__)


def get_license_key(q):
    """Get already set license key."""
    try:
        key = Option.objects.get(section='LICENSE', field='key')
        license_key = fernet_decrypt(key.value)
        LOG.info('License key: {}'.format(license_key))
        q.put(license_key)
    except Option.DoesNotExist:
        try:
            from fleio.core import loginview
            license_info = json.loads(loginview.get_license_info())
            license_key = license_info['License key']
            LOG.info('License key: {}'.format(license_key))
            q.put(license_key)
        except ImportError as e:
            LOG.error(e)
            q.put(None)
        return None


def reset_license(license_key, path='.'):
    try:
        if license_key is None:
            LOG.error('License not found. You must set the license first to use this script.')
            return 1
        content, status = _set_license(license_key, path)
        if status != 200:
            LOG.error(content)
            return status
        else:
            Option.objects.update_or_create(section='LICENSE', field='key',
                                            defaults={'value': fernet_encrypt(license_key)})
            LOG.info('License updated')
            return 0
    except requests.ConnectionError:
        LOG.error("Can't connect to server. Please check your internet connection and retry.")


def update_license(path='.'):
    q = Queue()
    p = Process(target=get_license_key, args=(q,))
    p.start()
    try:
        license_key = q.get(timeout=60)
    except Empty:
        license_key = None
    p.join()
    return reset_license(license_key, path)


if __name__ == '__main__':
    sys.exit(update_license())
